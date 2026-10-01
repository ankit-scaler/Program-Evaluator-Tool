import os
import json
import re
import pandas as pd

DATA_SOURCE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Data_Source', 'Copy of Refunds Funnel - Raw.csv')
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')
MATRIX_JSON_PATH = os.path.join(OUTPUT_DIR, 'retention_matrix.json')

DEFAULT_FALLBACK = {
    'program': 'Scaler Academy',
    'persona': 'General Tech Professional',
    'total': 13180,
    'cohort_size': 13180,
    'refunds': 2872,
    'retention_rate': 78.2,
    'refund_rate': 21.8,
    'risk_level': 'High Retention'
}

def canonical_prog_key(prog_str):
    s = str(prog_str).lower()
    if 'fde' in s or 'forward' in s:
        return 'P3_FDE'
    elif 'aiml' in s or 'agentic' in s or 'deep learning' in s:
        return 'P4_AIML'
    elif 'dsml' in s or 'data' in s:
        return 'P2_DSML'
    elif 'devop' in s or 'cloud' in s:
        return 'P5_DEVOPS'
    return 'P1_ACADEMY'

def canonical_persona_key(persona_str):
    s = str(persona_str).lower()
    if any(k in s for k in [
        'hr', 'human resource', 'recruiter', 'talent', 'staffing', 'people partner', 'people ops', 'hrbp',
        'marketing', 'seo', 'growth', 'content', 'copywriter', 'branding', 'digital marketing',
        'sales', 'business development', 'bde', 'bda', 'account executive', 'inside sales', 'telecaller',
        'finance', 'accounting', 'accountant', 'auditor', 'taxation', 'banking', 'insurance',
        'operations', 'admin', 'administration', 'consultant', 'legal', 'lawyer', 'procurement', 'logistics', 'supply chain',
        'bpo', 'kpo', 'customer', 'support', 'call center',
        'mechanical', 'civil', 'chemical', 'electrical', 'biotech',
        'student', 'learner', 'intern', 'fresher', 'non coder', 'non-coder', 'non-tech', 'non tech'
    ]):
        return 'NON_TECH'
    elif any(k in s for k in ['test', 'qa', 'sdet', 'automation']):
        return 'QA_SDET'
    elif any(k in s for k in ['data', 'analyst', 'analytics', 'bi ', 'business intelligence', 'power bi', 'tableau']):
        return 'DATA_ANALYST'
    elif any(k in s for k in ['devops', 'sre', 'cloud', 'infrastructure', 'docker', 'kubernetes']):
        return 'DEVOPS_CLOUD'
    elif any(k in s for k in ['system', 'embedded', 'hardware', 'linux', 'firmware']):
        return 'SYSTEMS_ENG'
    elif any(k in s for k in ['management', 'manager', 'leadership', 'director', 'founder', 'vp', 'architect', 'head of']) or ('lead' in s and 'sdet' not in s):
        return 'LEADERSHIP'
    elif any(k in s for k in ['frontend', 'front-end', 'ui/ux', 'ui dev', 'react', 'angular', 'web developer']):
        return 'FRONTEND'
    elif any(k in s for k in ['maintenance', 'support', 'it service', 'general it', 'service based', 'production support', 'app support']):
        return 'IT_SERVICES'
    return 'SWE_BACKEND'

def canonical_exp_key(exp_str):
    if exp_str is None:
        return 'EXP_1_3'
    s = str(exp_str).strip().lower()
    
    # 1. Check if a 4-digit graduation year is present (e.g. Batch 2025, Batch 2023, Batch 2012)
    import re
    year_match = re.search(r'\b(19\d\d|20\d\d)\b', s.replace(',', ''))
    if year_match:
        grad_year = int(year_match.group(1))
        current_year = 2026
        if grad_year >= 2025:
            return 'EXP_0_1'
        diff = max(0, current_year - grad_year)
        if diff < 1:
            return 'EXP_0_1'
        elif diff < 3:
            return 'EXP_1_3'
        elif diff < 5:
            return 'EXP_3_5'
        else:
            return 'EXP_5_PLUS'

    # 2. Numeric extraction for actual YOE (handles 8.0 yrs, 2.5 years, 0 years)
    match = re.search(r'[-+]?\d*\.?\d+', s.replace(',', ''))
    if match and match.group():
        try:
            val = float(match.group())
            # Convert months if explicitly indicated in text (e.g. 24 months = 2 years)
            if any(m in s for m in ['month', 'mo', 'mth']):
                val = val / 12.0
            if val < 1.0:
                return 'EXP_0_1'
            elif val < 3.0:
                return 'EXP_1_3'
            elif val < 5.0:
                return 'EXP_3_5'
            else:
                return 'EXP_5_PLUS'
        except Exception:
            pass

    # 3. Keyword matching for non-numeric strings
    if any(k in s for k in ['fresher', 'student', 'intern', 'college', 'beginner', '< 1', '0-1']):
        return 'EXP_0_1'

    if any(k in s for k in ['1 - 3', '1-2', '2-3', '1 year', '2 year', '1 yr', '2 yr']):
        return 'EXP_1_3'
    elif any(k in s for k in ['3 - 5', '3-5', '3 year', '4 year', '3 yr', '4 yr']):
        return 'EXP_3_5'
    return 'EXP_5_PLUS'

_MATRIX_CACHE = None

def load_matrix():
    global _MATRIX_CACHE
    if _MATRIX_CACHE is not None:
        return _MATRIX_CACHE
    if os.path.exists(MATRIX_JSON_PATH):
        try:
            with open(MATRIX_JSON_PATH, 'r', encoding='utf-8') as f:
                _MATRIX_CACHE = json.load(f)
                return _MATRIX_CACHE
        except Exception:
            pass
    _MATRIX_CACHE = {}
    return _MATRIX_CACHE

def get_cohort_stats(program, persona, experience=None, matrix_data=None):
    """
    Defensively retrieves retention and refund rates with canonical key matching and Bayesian fallback.
    Guaranteed NEVER to return None.
    """
    if matrix_data is None:
        matrix_data = load_matrix()

    p_key = canonical_prog_key(program)
    pers_key = canonical_persona_key(persona)
    exp_key = canonical_exp_key(experience) if experience else 'EXP_1_3'

    # Search in structured JSON
    # 1. 3D search by exact dimensions in by_program_persona_exp
    exp_dict = matrix_data.get('by_program_persona_exp', {})
    for k, stat in exp_dict.items():
        parts = k.split('___')
        if len(parts) == 3:
            k_prog, k_pers, k_exp = parts[0], parts[1], parts[2]
            if (canonical_prog_key(k_prog) == p_key and 
                canonical_persona_key(k_pers) == pers_key and 
                canonical_exp_key(k_exp) == exp_key):
                ret = stat.get('smoothed_retention_rate', stat.get('raw_retention_rate', stat.get('retention_rate', 78.2)))
                ref = stat.get('smoothed_refund_rate', stat.get('raw_refund_rate', stat.get('refund_rate', 21.8)))
                tot = stat.get('cohort_size', stat.get('total', 100))
                return {
                    'retention_rate': ret,
                    'refund_rate': ref,
                    'total': tot,
                    'cohort_size': tot,
                    'risk_level': 'High Retention' if ret >= 80 else ('Moderate' if ret >= 75 else 'High Risk')
                }

    # 2. 2D search in by_program_persona
    pers_dict = matrix_data.get('by_program_persona', {})
    for k, stat in pers_dict.items():
        parts = k.split('___')
        if len(parts) >= 2:
            k_prog, k_pers = parts[0], parts[1]
        else:
            k_prog, k_pers = k, k
        if canonical_prog_key(k_prog) == p_key and canonical_persona_key(k_pers) == pers_key:
            ret = stat.get('retention_rate', stat.get('smoothed_retention_rate', 78.2))
            ref = stat.get('refund_rate', stat.get('smoothed_refund_rate', 21.8))
            tot = stat.get('cohort_size', stat.get('total', 100))
            return {
                'retention_rate': ret,
                'refund_rate': ref,
                'total': tot,
                'cohort_size': tot,
                'risk_level': 'High Retention' if ret >= 80 else ('Moderate' if ret >= 75 else 'High Risk')
            }

    # 3. 1D search in by_program
    prog_dict = matrix_data.get('by_program', {})
    for k, stat in prog_dict.items():
        if canonical_prog_key(k) == p_key:
            ret = stat.get('retention_rate', 78.2)
            ref = stat.get('refund_rate', 21.8)
            tot = stat.get('cohort_size', stat.get('total', 500))
            return {
                'retention_rate': ret,
                'refund_rate': ref,
                'total': tot,
                'cohort_size': tot,
                'risk_level': 'High Retention' if ret >= 80 else ('Moderate' if ret >= 75 else 'High Risk')
            }

    # Guaranteed Default Fallback
    return dict(DEFAULT_FALLBACK)

# Helper alias
normalize_persona = lambda raw_persona, raw_role: canonical_persona_key(f"{raw_persona} {raw_role}")
normalize_experience = lambda exp_val: canonical_exp_key(exp_val)
normalize_program = lambda prog_val: canonical_prog_key(prog_val)
