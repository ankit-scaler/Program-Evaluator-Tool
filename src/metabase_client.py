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
    return bool(cfg.get("public_uuid") or (cfg.get("card_id") and (cfg.get("api_key") or cfg.get("username"))))

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

    # 2. Authenticated API Key Endpoint (Metabase v0.46+)
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
    Attempts to look up a specific lead by email or phone from Metabase.
    If full fetch succeeds, filters for the query.
    Returns a normalized lead dict or None.
    """
    if not is_metabase_configured():
        return None

    try:
        df = fetch_leads_from_metabase()
        if df.empty:
            return None

        q_clean = query_str.strip().lower()
        
        # Search across email and phone columns
        for _, row in df.iterrows():
            row_dict = row.to_dict()
            email_val = str(row_dict.get('email', row_dict.get('Email', ''))).strip().lower()
            phone_val = str(row_dict.get('phone', row_dict.get('Phone', ''))).strip()
            name_val = str(row_dict.get('name', row_dict.get('Name', ''))).strip().lower()

            if (q_clean in email_val or 
                q_clean in phone_val or 
                (len(q_clean) >= 4 and q_clean in name_val)):
                return row_dict
    except Exception as e:
        logger.warning(f"Error executing Metabase live lookup for '{query_str}': {e}")
        return None

    return None
