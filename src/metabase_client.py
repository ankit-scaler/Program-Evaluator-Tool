import os
import json
import logging
import requests
import pandas as pd
from typing import Optional, Dict, Any, List

logger = logging.getLogger("metabase_client")

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'metabase_config.json')

def load_metabase_config() -> Dict[str, Any]:
    """
    Loads Metabase connection configuration from metabase_config.json or environment variables.
    """
    cfg = {
        "metabase_url": os.getenv("METABASE_URL", "").rstrip("/"),
        "card_id": os.getenv("METABASE_CARD_ID", ""),
        "session_token": os.getenv("METABASE_SESSION_TOKEN", ""),
        "email_parameter_id": os.getenv("METABASE_EMAIL_PARAM_ID", ""),
        "api_key": os.getenv("METABASE_API_KEY", ""),
        "public_uuid": os.getenv("METABASE_PUBLIC_UUID", ""),
        "username": os.getenv("METABASE_USERNAME", ""),
        "password": os.getenv("METABASE_PASSWORD", ""),
        "timeout_seconds": int(os.getenv("METABASE_TIMEOUT", "30"))
    }
    
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                disk_cfg = json.load(f)
                for k, v in disk_cfg.items():
                    if v and not str(v).startswith("https://metabase.yourcompany"):
                        cfg[k] = v
        except Exception as e:
            logger.warning(f"Failed to read metabase_config.json: {e}")
            
    return cfg

def is_metabase_configured() -> bool:
    """
    Checks whether valid Metabase connection parameters have been provided.
    """
    cfg = load_metabase_config()
    url = cfg.get("metabase_url", "")
    if not url or "yourcompany" in url:
        return False
    return bool(cfg.get("public_uuid") or (cfg.get("card_id") and (cfg.get("session_token") or cfg.get("api_key") or cfg.get("username"))))

def get_session_token(base_url: str, username: str, password: str, timeout: int = 20) -> Optional[str]:
    """
    Obtains a Metabase session token via username and password.
    """
    try:
        url = f"{base_url}/api/session"
        res = requests.post(url, json={"username": username, "password": password}, timeout=timeout)
        if res.status_code == 200:
            return res.json().get("id")
    except Exception as e:
        logger.error(f"Metabase session authentication failed: {e}")
    return None

def fetch_leads_from_metabase() -> pd.DataFrame:
    """
    Fetches the full leads dataset from the configured Metabase Question/Card.
    Returns a pandas DataFrame.
    """
    cfg = load_metabase_config()
    base_url = cfg.get("metabase_url", "").rstrip("/")
    api_key = cfg.get("api_key", "").strip()
    session_token = cfg.get("session_token", "").strip()
    card_id = cfg.get("card_id")
    public_uuid = cfg.get("public_uuid", "").strip()
    username = cfg.get("username", "").strip()
    password = cfg.get("password", "").strip()
    timeout = cfg.get("timeout_seconds", 30)

    if not base_url or "yourcompany" in base_url:
        raise ValueError("Metabase URL is not configured. Please update metabase_config.json with your Metabase URL.")

    # 1. Public Card Link (Zero authentication required if Public Sharing is enabled on Metabase)
    if public_uuid:
        url = f"{base_url}/api/public/card/{public_uuid}/query/json"
        res = requests.get(url, timeout=timeout)
        res.raise_for_status()
        data = res.json()
        return pd.DataFrame(data)

    # 2. Authenticated Session Token or API Key Endpoint
    if session_token and card_id:
        url = f"{base_url}/api/card/{card_id}/query/json"
        headers = {
            "X-Metabase-Session": session_token,
            "Content-Type": "application/json"
        }
        res = requests.post(url, headers=headers, json={}, timeout=timeout)
        res.raise_for_status()
        data = res.json()
        return pd.DataFrame(data)

    if api_key and card_id:
        url = f"{base_url}/api/card/{card_id}/query/json"
        headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json"
        }
        res = requests.post(url, headers=headers, json={}, timeout=timeout)
        res.raise_for_status()
        data = res.json()
        return pd.DataFrame(data)

    # 3. Username / Password Session Authentication
    if username and password and card_id:
        token = get_session_token(base_url, username, password, timeout=timeout)
        if not token:
            raise PermissionError("Failed to authenticate with Metabase using provided username/password.")
        url = f"{base_url}/api/card/{card_id}/query/json"
        headers = {
            "X-Metabase-Session": token,
            "Content-Type": "application/json"
        }
        res = requests.post(url, headers=headers, json={}, timeout=timeout)
        res.raise_for_status()
        data = res.json()
        return pd.DataFrame(data)

    raise ValueError("Incomplete Metabase credentials. Set 'public_uuid' OR ('card_id' + 'api_key') in metabase_config.json.")

def fetch_lead_by_email_from_metabase(query_str: str) -> Optional[Dict[str, Any]]:
    """
    Looks up a specific lead by email from Metabase Card 28973 using a parameterized query.
    Returns a normalized dictionary of the lead profile or None if not found.
    """
    if not is_metabase_configured():
        return None

    cfg = load_metabase_config()
    base_url = cfg.get("metabase_url", "").rstrip("/")
    card_id = cfg.get("card_id", "28973")
    session_token = cfg.get("session_token", "").strip()
    param_id = cfg.get("email_parameter_id", "2dcd8f80-e4b6-46cf-936b-2102140cb7f2")
    timeout = cfg.get("timeout_seconds", 30)

    q_clean = query_str.strip().lower()

    # 1. Parameterized Metabase Query (Instant sub-second query execution)
    if session_token and card_id:
        try:
            url = f"{base_url}/api/card/{card_id}/query"
            headers = {
                "Content-Type": "application/json",
                "X-Metabase-Session": session_token
            }
            payload = {
                "parameters": [
                    {
                        "id": param_id,
                        "type": "string/=",
                        "value": [q_clean],
                        "target": ["dimension", ["template-tag", "email"]]
                    }
                ]
            }
            res = requests.post(url, headers=headers, json=payload, timeout=timeout)
            if res.status_code in (200, 202):
                data = res.json()
                rows = data.get("data", {}).get("rows", [])
                cols = data.get("data", {}).get("cols", [])
                col_names = [col.get("display_name", col.get("name", "unknown")) for col in cols]
                if rows:
                    raw_dict = dict(zip(col_names, rows[0]))
                    
                    # Strictly filter and keep only the columns needed by the recommendation engine
                    REQUIRED_COLS = {
                        'email', 'name', 'phone', 'role', 'experience', 'orgname', 'orgyear',
                        'company_type', 'education', 'program_type', 'which_bda_team',
                        'test_launched_flag', 'test_passed_flag', 'event_name', 'event_type',
                        'attended_before_payment_flag', 'duration', 'signed_up_date',
                        'lead_created_at', 'lead_score', 'batch', 'platform', 'country_type',
                        'event_category'
                    }
                    filtered_dict = {k: v for k, v in raw_dict.items() if k in REQUIRED_COLS}
                    return filtered_dict
            elif res.status_code == 401:
                logger.warning("Metabase session token expired (HTTP 401). Please update session_token in metabase_config.json.")
        except Exception as e:
            logger.warning(f"Error executing parameterized Metabase live query for '{q_clean}': {e}")

    # 2. Fallback: Full table search if public or api_key configured
    try:
        df = fetch_leads_from_metabase()
        if not df.empty:
            for _, row in df.iterrows():
                row_dict = row.to_dict()
                email_val = str(row_dict.get('email', row_dict.get('Email', ''))).strip().lower()
                phone_val = str(row_dict.get('phone', row_dict.get('Phone', ''))).strip()
                if q_clean in email_val or q_clean in phone_val:
                    return row_dict
    except Exception as e:
        logger.warning(f"Fallback Metabase fetch error: {e}")

    return None
