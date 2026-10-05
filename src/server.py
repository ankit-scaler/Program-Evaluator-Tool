import os
import io
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
    find_lead_by_query, get_recent_leads
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
        if not any(l['lead_id'] == db_lead['lead_id'] for l in CACHED_LEADS):
            CACHED_LEADS.insert(0, db_lead)
        return {"status": "success", "source": "crm_database", "lead": db_lead}
        
    # 3. Dynamic Fallback: Search live in Metabase via API
    try:
        mb_row = fetch_lead_by_email_from_metabase(q_clean)
        if mb_row:
            eval_res = evaluate_lead_profile(mb_row)
            lead_id = f"LD-MB-{abs(hash(q_clean)) % 100000:05d}"
            eval_res['lead_id'] = lead_id
            eval_res['touchpoints'] = {
                'summary': f"Metabase Ingest - {mb_row.get('event_name', mb_row.get('Program', 'Live Inquiry'))}",
                'event_name': mb_row.get('event_name', mb_row.get('Event Name', 'Metabase Lead Query')),
                'attended': mb_row.get('attended', mb_row.get('Attended', 'Registered')),
                'duration': str(mb_row.get('duration', 'N/A')),
                'sat_status': mb_row.get('set_status', mb_row.get('sat_status', 'SET Pending')),
                'sat_score': str(mb_row.get('set_score', mb_row.get('sat_score', 'N/A'))),
                'set_status': mb_row.get('set_status', mb_row.get('sat_status', 'SET Pending')),
                'set_score': str(mb_row.get('set_score', mb_row.get('sat_score', 'N/A'))),
                'channel': mb_row.get('channel', 'Metabase Data Warehouse'),
                'campaign': mb_row.get('campaign', 'Metabase Query Sync'),
                'platform': "Metabase API",
                'geography': mb_row.get('geography', 'India'),
                'signup_date': str(mb_row.get('signup_date', 'Recent')),
                'lead_score': "Hot (Direct Query)",
                'landing_page': "https://www.scaler.com"
            }
            save_evaluated_lead(eval_res, source="METABASE_LIVE_LOOKUP")
            CACHED_LEADS.insert(0, eval_res)
            return {"status": "success", "source": "metabase_live", "lead": eval_res}
    except Exception as e:
        pass
        
    return {"status": "not_found", "message": f"No lead found in CRM matching '{q}'."}

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

@app.get("/api/export")
async def export_crm_csv():
    if not os.path.exists(EXPORT_CSV_PATH):
        if CACHED_DF is not None:
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            CACHED_DF.to_csv(EXPORT_CSV_PATH, index=False)
        else:
            raise HTTPException(status_code=404, detail="No evaluated leads available to export. Please upload a CSV first.")
    
    return FileResponse(
        path=EXPORT_CSV_PATH,
        filename="crm_evaluated_leads_master.csv",
        media_type="text/csv"
    )

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("Program_Evaluator_Sales.src.server:app", host="127.0.0.1", port=8000, reload=True)
