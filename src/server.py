import os
import io
import json
import pandas as pd
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from .batch_processor import process_leads_dataframe
from .evaluator import evaluate_lead_profile
from .market_intelligence import get_all_curricula_catalog
from .lead_store import (
    init_db, save_evaluated_lead, bulk_save_evaluated_leads,
    find_lead_by_query, get_recent_leads, get_connection
)
import asyncio
from .csv_watcher import (
    sync_watched_csv,
    get_watched_csv_status,
    append_lead_to_csv,
    WATCHED_CSV_PATH
)
from .metabase_client import (
    is_metabase_configured,
    fetch_leads_from_metabase,
    fetch_lead_by_email_from_metabase,
    load_metabase_config
)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
WEB_DIR = os.path.join(BASE_DIR, 'web')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
EXPORT_CSV_PATH = os.path.join(OUTPUT_DIR, 'crm_evaluated_master.csv')

# Initialize SQLite database on startup
init_db()

app = FastAPI(title="Scaler Program Evaluator - Sales Decision Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    # Initial sync from watched CSV
    try:
        res = sync_watched_csv(force=True, memory_cache_ref=CACHED_LEADS)
        print(f">> Watched CSV Initial Sync: {res.get('new_leads_synced', 0)} new leads loaded from {res.get('file_path')}")
    except Exception as e:
        print(f"Warning during initial CSV watcher sync: {e}")
        
    # Start background polling task (checks every 5 seconds for newly added rows)
    async def poll_watched_csv_loop():
        while True:
            await asyncio.sleep(5)
            try:
                sync_res = sync_watched_csv(force=False, memory_cache_ref=CACHED_LEADS)
                new_count = sync_res.get('new_leads_synced', 0)
                if new_count > 0:
                    print(f">> Watched CSV Update Detected: Auto-evaluated and synced {new_count} new leads!")
            except Exception:
                pass
                
    asyncio.create_task(poll_watched_csv_loop())

@app.get("/health")
@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "scaler-program-evaluator",
        "version": "1.0.0"
    }


@app.get("/api/curriculum-catalog")
async def get_curriculum_catalog_endpoint():
    """Returns the complete official Scaler curriculum track modules catalog."""
    return {
        "status": "success",
        "catalog": get_all_curricula_catalog()
    }

@app.get("/scaler_logo.png")
@app.get("/scaler_logo_full.png")
async def serve_scaler_logo():
    logo_path = os.path.join(WEB_DIR, 'scaler_logo.png')
    if os.path.exists(logo_path):
        return FileResponse(logo_path, media_type="image/png")
    raise HTTPException(status_code=404, detail="Logo not found")

@app.get("/avatar_male.png")
async def serve_avatar_male():
    avatar_path = os.path.join(WEB_DIR, 'avatar_male.png')
    if os.path.exists(avatar_path):
        return FileResponse(avatar_path, media_type="image/png")
    raise HTTPException(status_code=404, detail="Male avatar not found")

@app.get("/avatar_female.png")
async def serve_avatar_female():
    avatar_path = os.path.join(WEB_DIR, 'avatar_female.png')
    if os.path.exists(avatar_path):
        return FileResponse(avatar_path, media_type="image/png")
    raise HTTPException(status_code=404, detail="Female avatar not found")

# Global in-memory store of uploaded/evaluated leads (Starts 100% EMPTY)
CACHED_LEADS = []
CACHED_DF = None

class SingleLeadInput(BaseModel):
    name: Optional[str] = "Prospective Learner"
    email: Optional[str] = ""
    phone: Optional[str] = "N/A"
    role: str
    experience: str
    education: Optional[str] = "Graduated / Degree"
    company_type: Optional[str] = "IT Services / Technology"
    previous_org: Optional[str] = "Current Company"
    program: Optional[str] = "Academy"
    set_score: Optional[str] = None
    set_status: Optional[str] = None
    sat_score: Optional[str] = "N/A"
    sat_status: Optional[str] = "SET Not Attempted"

class CRMWebhookLead(BaseModel):
    name: Optional[str] = "Prospective Learner"
    email: str
    phone: Optional[str] = "N/A"
    role: Optional[str] = "Software Engineer"
    experience: Optional[str] = "2 years"
    education: Optional[str] = "Graduated / Degree"
    company_type: Optional[str] = "IT Services / Technology"
    previous_org: Optional[str] = "Current Company"
    program: Optional[str] = "Academy"
    event_name: Optional[str] = "Direct CRM Inbound Registration"
    attended: Optional[str] = "Attended"
    duration: Optional[str] = "N/A"
    set_score: Optional[str] = None
    set_status: Optional[str] = None
    sat_score: Optional[str] = "N/A"
    sat_status: Optional[str] = "SET Attempted"
    channel: Optional[str] = "CRM Webhook / Inbound"

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_path = os.path.join(WEB_DIR, 'index.html')
    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail="Frontend UI not found")
    with open(index_path, 'r', encoding='utf-8') as f:
        return HTMLResponse(
            content=f.read(),
            headers={
                "Cache-Control": "no-cache, no-store, must-revalidate, max-age=0",
                "Pragma": "no-cache",
                "Expires": "0"
            }
        )

@app.post("/api/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    """
    Accepts user-uploaded CSV, evaluates all rows dynamically, stores in database, and returns evaluated leads.
    Includes multi-encoding fallback and memory protection.
    """
    global CACHED_LEADS, CACHED_DF
    try:
        contents = await file.read()
        df = None
        for enc in ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']:
            try:
                df = pd.read_csv(io.BytesIO(contents), encoding=enc, low_memory=False)
                break
            except (UnicodeDecodeError, Exception):
                continue
        if df is None:
            df = pd.read_csv(io.BytesIO(contents), encoding='latin-1', sep=None, engine='python')
        
        evaluated_all, CACHED_DF = process_leads_dataframe(df)
        
        # Build high-performance compact records (removes 1.2 GB of duplicated module text from row payloads)
        compact_records = []
        for r in evaluated_all:
            c = {
                'lead_id': r.get('lead_id'),
                'person': r.get('person'),
                'primary': {k: v for k, v in r.get('primary', {}).items() if k not in ['curriculum_modules', 'market_intelligence']},
                'fallback': {k: v for k, v in r.get('fallback', {}).items() if k not in ['curriculum_modules', 'market_intelligence']},
                'sales_script': r.get('sales_script'),
                'touchpoints': r.get('touchpoints')
            }
            compact_records.append(c)
        
        # Fast bulk save into SQLite database
        try:
            bulk_save_evaluated_leads(compact_records, source=f"CSV: {file.filename}")
        except Exception as db_err:
            print(f"Warning during SQLite persistence: {db_err}")
        
        CACHED_LEADS = compact_records
        
        try:
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            CACHED_DF.to_csv(EXPORT_CSV_PATH, index=False)
        except Exception as csv_err:
            print(f"Warning exporting master CSV: {csv_err}")
        
        # Return compact leads (capped at 10,000 for instant sub-second browser rendering)
        ui_leads = compact_records[:10000]
        
        return {
            "status": "success",
            "filename": file.filename,
            "total": len(evaluated_all),
            "displayed": len(ui_leads),
            "leads": ui_leads,
            "curriculum_catalog": get_all_curricula_catalog()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process CSV: {str(e)}")

@app.post("/api/crm/webhook")
async def crm_webhook(lead: CRMWebhookLead):
    """
    Dynamic Inbound CRM Webhook: Receives a new lead from Salesforce / HubSpot / LeadSquared in real time,
    evaluates program recommendation + track + duration + academic eligibility, captures touchpoints,
    saves to SQLite, and returns full dossier.
    """
    global CACHED_LEADS
    import time
    lead_dict = {
        'name': lead.name or "Prospective Learner",
        'email': lead.email,
        'phone': lead.phone or "N/A",
        'role': lead.role or "Software Professional",
        'experience': lead.experience or "2 years",
        'education': lead.education or "Graduated / Degree",
        'company type': lead.company_type or "IT Services / Technology",
        'previous org name': lead.previous_org or "Current Company",
        'program': lead.program or "Academy",
        'set_score': lead.set_score or lead.sat_score or "N/A",
        'set_status': (lead.set_status or lead.sat_status or "SET Not Attempted").replace('SAT', 'SET').replace('sat', 'set'),
        'sat_score': lead.set_score or lead.sat_score or "N/A",
        'sat_status': (lead.set_status or lead.sat_status or "SET Not Attempted").replace('SAT', 'SET').replace('sat', 'set')
    }
    
    eval_res = evaluate_lead_profile(lead_dict)
    lead_id = f"LD-CRM-{int(time.time() * 1000) % 100000:05d}"
    eval_res['lead_id'] = lead_id
    
    touchpoint_dict = {
        'summary': f"{lead.attended} - {lead.event_name[:40]}",
        'event_name': lead.event_name,
        'attended': lead.attended,
        'duration': lead.duration,
        'sat_status': lead_dict['sat_status'],
        'sat_score': lead_dict['sat_score'],
        'set_status': lead_dict['set_status'],
        'set_score': lead_dict['set_score'],
        'channel': lead.channel,
        'campaign': "Live CRM Inbound",
        'platform': "Web / CRM API",
        'geography': "India / General",
        'signup_date': "Live Just Now",
        'lead_score': "Hot (Live Inbound)",
        'landing_page': "https://www.scaler.com"
    }
    eval_res['touchpoints'] = touchpoint_dict
    
    # Save to SQLite database for instant search
    save_evaluated_lead(eval_res, source="CRM_WEBHOOK")
    
    # Prepend to memory cache so UI live updates
    CACHED_LEADS.insert(0, eval_res)
    
    return {
        "status": "success",
        "message": "Lead ingested, evaluated, and indexed successfully",
        "lead": eval_res
    }

@app.post("/api/evaluate-single")
async def evaluate_single(lead_input: SingleLeadInput):
    """
    Evaluates a single lead entered directly by the sales counselor on the UI.
    """
    global CACHED_LEADS, CACHED_DF
    single_set_status = (lead_input.set_status or lead_input.sat_status or "SET Not Attempted").replace('SAT', 'SET').replace('sat', 'set')
    single_set_score = lead_input.set_score or lead_input.sat_score or "N/A"
    lead_dict = {
        'name': lead_input.name or "Prospective Learner",
        'email': lead_input.email or "unspecified@lead.com",
        'phone': lead_input.phone or "N/A",
        'role': lead_input.role,
        'experience': lead_input.experience,
        'education': lead_input.education or "Graduated / Degree",
        'company type': lead_input.company_type or "IT Services / Technology",
        'previous org name': lead_input.previous_org or "Current Organization",
        'program': lead_input.program or "Academy",
        'set_score': single_set_score,
        'set_status': single_set_status,
        'sat_score': single_set_score,
        'sat_status': single_set_status
    }
    
    eval_res = evaluate_lead_profile(lead_dict)
    lead_id = f"LD-LIVE-{len(CACHED_LEADS) + 1:04d}"
    eval_res['lead_id'] = lead_id
    
    touchpoint_dict = {
        'summary': "Manual Counselor Ingestion",
        'event_name': "Direct Counselor Intake",
        'attended': "Phone Inbound",
        'duration': "N/A",
        'sat_status': single_set_status,
        'sat_score': single_set_score,
        'set_status': single_set_status,
        'set_score': single_set_score,
        'channel': "Sales Inbound Desk",
        'campaign': "Direct Counselor Inquiry",
        'platform': "Counselor Console",
        'geography': "India",
        'signup_date': "Today",
        'lead_score': "Hot",
        'landing_page': "https://www.scaler.com"
    }
    eval_res['touchpoints'] = touchpoint_dict
    
    save_evaluated_lead(eval_res, source="MANUAL_INTAKE")
    CACHED_LEADS.insert(0, eval_res)
    
    return {
        "status": "success",
        "lead": eval_res
    }

@app.get("/api/lookup")
async def lookup_lead(q: str):
    """
    Looks up a lead by email, phone, name, or lead ID across memory, SQLite database,
    and fallback to Metabase API.
    """
    global CACHED_LEADS
    q_clean = q.strip().lower()
    
    # 1. Search in memory cache
    for lead in CACHED_LEADS:
        p = lead['person']
        if (p['email'].strip().lower() == q_clean or
            p['name'].strip().lower() == q_clean or
            lead['lead_id'].strip().lower() == q_clean or
            q_clean in p['email'].lower() or
            q_clean in p['phone']):
            return {"status": "success", "source": "memory_cache", "lead": lead}
            
    # 2. Search in persistent SQLite database
    db_lead = find_lead_by_query(q_clean)
    if db_lead:
        if not any(l.get('lead_id') == db_lead.get('lead_id') for l in CACHED_LEADS if l.get('lead_id')):
            CACHED_LEADS.insert(0, db_lead)
        source_label = "watched_csv" if db_lead.get('source') == 'WATCHED_CSV' else "crm_database"
        return {"status": "success", "source": source_label, "lead": db_lead}
        
    # 3. Dynamic Check: Scan watched CSV file immediately (in case lead was just added moments ago)
    try:
        csv_sync = sync_watched_csv(force=True, memory_cache_ref=CACHED_LEADS)
        if csv_sync.get('new_leads_synced', 0) > 0:
            db_lead = find_lead_by_query(q_clean)
            if db_lead:
                return {"status": "success", "source": "watched_csv", "lead": db_lead}
    except Exception:
        pass

    # 4. Dynamic Fallback: Search live in Metabase via API
    try:
        mb_row = fetch_lead_by_email_from_metabase(q_clean)
        if mb_row:
            eval_res = evaluate_lead_profile(mb_row)
            lead_id = mb_row.get('lead_id') or mb_row.get('Lead ID') or mb_row.get('id') or f"LD-MIS-{abs(hash(q_clean)) % 100000:05d}"
            eval_res['lead_id'] = lead_id
            eval_res['touchpoints'] = {
                'summary': f"Marketing MIS - {mb_row.get('event_name') or mb_row.get('Event Name') or mb_row.get('program') or mb_row.get('Program') or 'Live Inquiry'}",
                'event_name': mb_row.get('event_name') or mb_row.get('Event Name') or 'Direct MIS Query',
                'attended': mb_row.get('attended') or mb_row.get('Attended') or 'Registered',
                'duration': str(mb_row.get('duration') or mb_row.get('Duration') or 'N/A'),
                'sat_status': mb_row.get('set_status') or mb_row.get('sat_status') or mb_row.get('SET Status') or 'SET Not Attempted',
                'sat_score': str(mb_row.get('set_score') or mb_row.get('sat_score') or mb_row.get('SET Score') or 'N/A'),
                'set_status': mb_row.get('set_status') or mb_row.get('sat_status') or mb_row.get('SET Status') or 'SET Not Attempted',
                'set_score': str(mb_row.get('set_score') or mb_row.get('sat_score') or mb_row.get('SET Score') or 'N/A'),
                'channel': mb_row.get('channel') or mb_row.get('Channel') or 'Marketing MIS',
                'campaign': mb_row.get('campaign') or mb_row.get('Campaign') or 'Direct Campaign',
                'platform': mb_row.get('platform') or mb_row.get('Platform') or 'MIS Web API',
                'geography': mb_row.get('geography') or mb_row.get('City') or mb_row.get('Geography') or 'India',
                'signup_date': str(mb_row.get('signup_date') or mb_row.get('Created At') or mb_row.get('Date') or 'Recent'),
                'lead_score': str(mb_row.get('lead_score') or mb_row.get('Lead Score') or 'Active'),
                'landing_page': mb_row.get('landing_page') or mb_row.get('Landing Page') or 'https://www.scaler.com'
            }
            save_evaluated_lead(eval_res, source="METABASE_LIVE_LOOKUP")
            CACHED_LEADS.insert(0, eval_res)
            return {"status": "success", "source": "metabase_live", "lead": eval_res}
    except Exception as e:
        pass
        
    return {"status": "not_found", "message": f"No lead found in CRM matching '{q}'."}

class AppendLeadInput(BaseModel):
    name: str = "Prospective Learner"
    email: str
    phone: Optional[str] = "N/A"
    role: str = "Software Engineer"
    experience: str = "2 years"
    education: Optional[str] = "B.Tech CSE"
    company_type: Optional[str] = "IT Services / Technology"
    previous_org: Optional[str] = "Current Company"
    program: Optional[str] = "Academy"
    set_status: Optional[str] = "Passed"
    set_score: Optional[str] = "80"

@app.get("/api/csv-stream/status")
async def get_csv_stream_status():
    """Returns status and file details for the incoming watched CSV file."""
    return {
        "status": "success",
        "details": get_watched_csv_status()
    }

@app.post("/api/csv-stream/sync")
async def trigger_csv_stream_sync():
    """Forces an immediate sync of the incoming watched CSV file."""
    global CACHED_LEADS
    res = sync_watched_csv(force=True, memory_cache_ref=CACHED_LEADS)
    return res

@app.get("/api/csv-stream/leads")
async def get_csv_stream_leads():
    """
    Returns all evaluated leads stored in the session/database (from CSVs, Marketing MIS lookups,
    and live webhooks) so counselor data is preserved across page refreshes.
    """
    import json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT lead_id, source, evaluated_json FROM leads 
        ORDER BY created_at DESC;
    """)
    rows = cursor.fetchall()
    conn.close()
    
    leads = []
    for r in rows:
        data = json.loads(r['evaluated_json'])
        if 'lead_id' not in data or not data['lead_id']:
            data['lead_id'] = r['lead_id']
        data['source'] = r['source']
        leads.append(data)
        
    return {
        "status": "success",
        "total": len(leads),
        "leads": leads
    }

@app.post("/api/csv-stream/append")
async def append_lead_to_csv_endpoint(lead_input: AppendLeadInput):
    """
    Appends a new lead to the incoming watched CSV file and triggers auto-evaluation.
    """
    res = append_lead_to_csv(lead_input.dict())
    return res

@app.post("/api/metabase/sync")
async def sync_metabase():
    """
    Dynamically pulls latest query results from Metabase API, evaluates all records,
    persists them in SQLite database, updates memory cache, and updates master CSV.
    """
    global CACHED_LEADS, CACHED_DF
    if not is_metabase_configured():
        return {
            "status": "not_configured",
            "message": "Metabase connection is not configured yet. Open metabase_config.json to add your Metabase URL and Card ID or Public UUID."
        }
        
    try:
        df = fetch_leads_from_metabase()
        if df.empty:
            return {"status": "empty", "message": "Metabase query returned 0 rows."}
            
        evaluated_all, CACHED_DF = process_leads_dataframe(df)
        bulk_save_evaluated_leads(evaluated_all, source="METABASE_SYNC")
        CACHED_LEADS = evaluated_all[:25000]
        
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        CACHED_DF.to_csv(EXPORT_CSV_PATH, index=False)
        
        return {
            "status": "success",
            "total_synced": len(evaluated_all),
            "message": f"Successfully pulled and evaluated {len(evaluated_all)} leads from Metabase.",
            "leads": CACHED_LEADS
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Metabase sync failed: {str(e)}")

@app.get("/api/metabase/status")
async def metabase_status():
    cfg = load_metabase_config()
    configured = is_metabase_configured()
    return {
        "configured": configured,
        "metabase_url": cfg.get("metabase_url", ""),
        "card_id": cfg.get("card_id", ""),
        "has_public_uuid": bool(cfg.get("public_uuid")),
        "has_api_key": bool(cfg.get("api_key"))
    }

from fastapi.responses import Response

@app.get("/api/export")
async def export_crm_data(format: str = "csv"):
    """
    Exports evaluated leads directly from SQLite database.
    Supports ?format=csv or ?format=xlsx (Excel).
    Never locks files and always reflects the most up-to-date evaluated leads.
    """
    format_clean = format.lower().strip()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT evaluated_json, source, created_at FROM leads ORDER BY created_at DESC;")
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        raise HTTPException(status_code=404, detail="No evaluated leads available in database to export.")
        
    records = []
    for row in rows:
        try:
            r_json = row['evaluated_json']
            src = row['source']
            dt = row['created_at']
            data = json.loads(r_json)
            p = data.get('person', {})
            prim = data.get('primary', {})
            fall = data.get('fallback', {})
            tp = data.get('touchpoints', {})
            records.append({
                'Lead ID': data.get('lead_id', ''),
                'Candidate Name': p.get('name', ''),
                'Email': p.get('email', ''),
                'Phone': p.get('phone', ''),
                'Current Role': p.get('role', ''),
                'Total Experience': p.get('experience', ''),
                'Education': p.get('education', ''),
                'Company Type': p.get('company_type', ''),
                'Previous Organization': p.get('previous_org', ''),
                'Enquired Program': p.get('enquired_program', p.get('program', 'N/A')),
                'Primary Program': prim.get('program', ''),
                'Primary Track': prim.get('track', ''),
                'Primary Fit Tier': prim.get('fit_tier', ''),
                'Primary Duration': prim.get('duration', ''),
                'Retention Rate (%)': prim.get('retention_rate', ''),
                'Refund Risk (%)': prim.get('refund_rate', ''),
                'Fallback Program': fall.get('program', ''),
                'Fallback Track': fall.get('track', ''),
                'Diagnostic SET Status': tp.get('set_status', tp.get('sat_status', 'SET Not Attempted')),
                'Diagnostic SET Score': tp.get('set_score', tp.get('sat_score', 'N/A')),
                'Ingestion Source': src,
                'Evaluated At': dt
            })
        except Exception:
            continue
            
    df_export = pd.DataFrame(records)
    
    if format_clean in ['xlsx', 'excel']:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_export.to_excel(writer, index=False, sheet_name='Evaluated Leads')
        output.seek(0)
        return Response(
            content=output.getvalue(),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=scaler_evaluated_leads_master.xlsx"}
        )
    else:
        # Default CSV export with UTF-8 BOM for Microsoft Excel compatibility
        csv_buffer = io.StringIO()
        df_export.to_csv(csv_buffer, index=False, encoding='utf-8')
        return Response(
            content=csv_buffer.getvalue().encode('utf-8-sig'),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=scaler_evaluated_leads_master.csv"}
        )

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("Program_Evaluator_Sales.src.server:app", host="127.0.0.1", port=8000, reload=True)
