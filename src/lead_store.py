import os
import sqlite3
import json
import re
from typing import Optional, Dict, Any, List

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output', 'leads_store.db')

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=30.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            lead_id TEXT PRIMARY KEY,
            email TEXT,
            email_lower TEXT,
            phone TEXT,
            name TEXT,
            role TEXT,
            experience TEXT,
            education TEXT,
            education_level TEXT,
            company_type TEXT,
            previous_org TEXT,
            source TEXT DEFAULT 'CSV_UPLOAD',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            evaluated_json TEXT
        );
    """)
    # Check if education columns need to be added to an existing table
    try:
        cursor.execute("ALTER TABLE leads ADD COLUMN education TEXT;")
    except Exception:
        pass
    try:
        cursor.execute("ALTER TABLE leads ADD COLUMN education_level TEXT;")
    except Exception:
        pass
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_leads_email_lower ON leads(email_lower);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_leads_phone ON leads(phone);")
    conn.commit()
    conn.close()

def save_evaluated_lead(eval_res: Dict[str, Any], source: str = "CRM_WEBHOOK") -> bool:
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    
    p = eval_res.get('person', {})
    lead_id = eval_res.get('lead_id', 'LD-CRM-' + str(abs(hash(p.get('email', ''))))[:8])
    email = p.get('email', '')
    email_lower = email.strip().lower()
    phone = re.sub(r'\D', '', str(p.get('phone', '')))
    education = p.get('education', '')
    education_level = p.get('education_level', 'GRAD_UNKNOWN')
    
    cursor.execute("""
        INSERT INTO leads (lead_id, email, email_lower, phone, name, role, experience, education, education_level, company_type, previous_org, source, evaluated_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(lead_id) DO UPDATE SET
            email = excluded.email,
            email_lower = excluded.email_lower,
            phone = excluded.phone,
            name = excluded.name,
            role = excluded.role,
            experience = excluded.experience,
            education = excluded.education,
            education_level = excluded.education_level,
            company_type = excluded.company_type,
            previous_org = excluded.previous_org,
            source = excluded.source,
            evaluated_json = excluded.evaluated_json;
    """, (
        lead_id,
        email,
        email_lower,
        phone,
        p.get('name', 'Prospective Learner'),
        p.get('role', ''),
        p.get('experience', ''),
        education,
        education_level,
        p.get('company_type', ''),
        p.get('previous_org', ''),
        source,
        json.dumps(eval_res)
    ))
    conn.commit()
    conn.close()
    return True

def bulk_save_evaluated_leads(records: List[Dict[str, Any]], source: str = "CSV_UPLOAD") -> int:
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    
    batch = []
    for r in records:
        p = r.get('person', {})
        lead_id = r.get('lead_id', '')
        email = p.get('email', '')
        email_lower = email.strip().lower()
        phone = re.sub(r'\D', '', str(p.get('phone', '')))
        education = p.get('education', '')
        education_level = p.get('education_level', 'GRAD_UNKNOWN')
        batch.append((
            lead_id,
            email,
            email_lower,
            phone,
            p.get('name', ''),
            p.get('role', ''),
            p.get('experience', ''),
            education,
            education_level,
            p.get('company_type', ''),
            p.get('previous_org', ''),
            source,
            json.dumps(r)
        ))
        
    cursor.executemany("""
        INSERT INTO leads (lead_id, email, email_lower, phone, name, role, experience, education, education_level, company_type, previous_org, source, evaluated_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(lead_id) DO UPDATE SET
            email = excluded.email,
            email_lower = excluded.email_lower,
            phone = excluded.phone,
            name = excluded.name,
            role = excluded.role,
            experience = excluded.experience,
            education = excluded.education,
            education_level = excluded.education_level,
            company_type = excluded.company_type,
            previous_org = excluded.previous_org,
            source = excluded.source,
            evaluated_json = excluded.evaluated_json;
    """, batch)
    conn.commit()
    count = cursor.rowcount
    conn.close()
    return count

def find_lead_by_query(query: str) -> Optional[Dict[str, Any]]:
    init_db()
    q = query.strip()
    if not q:
        return None
        
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Exact email match (case-insensitive)
    q_lower = q.lower()
    cursor.execute("SELECT evaluated_json FROM leads WHERE email_lower = ? LIMIT 1;", (q_lower,))
    row = cursor.fetchone()
    if row:
        conn.close()
        return json.loads(row['evaluated_json'])
        
    # 2. Phone match (normalized digits)
    digits = re.sub(r'\D', '', q)
    if len(digits) >= 7:
        cursor.execute("SELECT evaluated_json FROM leads WHERE phone LIKE ? LIMIT 1;", (f"%{digits}%",))
        row = cursor.fetchone()
        if row:
            conn.close()
            return json.loads(row['evaluated_json'])
            
    # 3. Partial email / lead_id match
    cursor.execute("""
        SELECT evaluated_json FROM leads 
        WHERE email_lower LIKE ? OR lead_id LIKE ? OR name LIKE ?
        LIMIT 1;
    """, (f"%{q_lower}%", f"%{q.upper()}%", f"%{q}%"))
    row = cursor.fetchone()
    conn.close()
    if row:
        return json.loads(row['evaluated_json'])
        
    return None

def get_recent_leads(limit: int = 50) -> List[Dict[str, Any]]:
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT evaluated_json FROM leads ORDER BY created_at DESC LIMIT ?;", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [json.loads(r['evaluated_json']) for r in rows]
