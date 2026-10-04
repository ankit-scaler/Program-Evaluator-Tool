import os
import json
import re
import pandas as pd
import numpy as np

try:
    from .matrix_engine import canonical_persona_key, CANONICAL_PERSONA_NAMES
except ImportError:
    from matrix_engine import canonical_persona_key, CANONICAL_PERSONA_NAMES

DATA_SOURCE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Data_Source', 'Copy of Refunds Funnel - Raw.csv')

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')
MATRIX_JSON_PATH = os.path.join(OUTPUT_DIR, 'retention_matrix.json')
MATRIX_CSV_PATH = os.path.join(OUTPUT_DIR, 'empirical_persona_matrix.csv')

def parse_work_experience(val):
    """
    Standardizes Total Work Experience from mixed formats (months as numbers, years as strings).
    """
    if pd.isna(val):
        return '1 - 3 yrs'
    
    s = str(val).strip().lower()
    
    # Textual presets
    if 'fresher' in s or s == '0' or '0-1' in s or '0-2' in s:
        return '< 1 yr (Early / Fresher)'
    elif '8+' in s or '5-8' in s:
        return '5+ yrs (Senior / Lead)'
    elif '3-5' in s:
        return '3 - 5 yrs (Experienced Mid)'
    elif '2-3' in s or '1-2' in s:
        return '1 - 3 yrs (Junior / Mid)'

    # Numerical extraction (months vs years)
    match = re.search(r'[-+]?\d*\.\d+|\d+', s)
    if match:
        num = float(match.group())
        has_month = any(m in s for m in ['month', 'mo', 'mth'])
        has_year = any(y in s for y in ['year', 'yr'])
        if (has_month and not has_year) or (num > 36 and not has_year):
            years = num / 12.0
        else:
            years = num
            
        if years < 1.0:
            return '< 1 yr (Early / Fresher)'
        elif years <= 3.0:
            return '1 - 3 yrs (Junior / Mid)'
        elif years <= 5.0:
            return '3 - 5 yrs (Experienced Mid)'
        else:
            return '5+ yrs (Senior / Lead)'
            
    return '1 - 3 yrs'

def parse_canonical_persona(raw_persona, raw_role, raw_exact=''):
    """
    Consolidates diverse raw columns into canonical Scaler personas using the global encyclopedic taxonomy.
    """
    combined = f"{str(raw_persona)} {str(raw_role)} {str(raw_exact)}".strip()
    key = canonical_persona_key(combined)
    return CANONICAL_PERSONA_NAMES.get(key, 'Non-Tech / Career Switcher')


def parse_canonical_program(prog_val):
    """
    Standardizes intake/current programs to official catalog program names.
    """
    if pd.isna(prog_val):
        return 'Program 1: Software & AI Engineering (Scaler Academy)'
    s = str(prog_val).strip().lower()
    if 'acad' in s or 'soft' in s or 'swe' in s:
        return 'Program 1: Software & AI Engineering (Scaler Academy)'
    elif 'dsml' in s or 'data' in s:
        return 'Program 2: Modern Data Science & Machine Learning (DSML)'
    elif 'fde' in s or 'forward' in s:
        return 'Program 3: AI Forward Deployed Engineer (FDE)'
    elif 'aiml' in s or 'ai' in s or 'agentic' in s:
        return 'Program 4: AI & Machine Learning with Agentic AI'
    elif 'devop' in s or 'cloud' in s:
        return 'Program 5: DevOps, Cloud & AI Platform Engineering'
    return 'Program 1: Software & AI Engineering (Scaler Academy)'

def run_cleaning_and_build_matrix():
    print(f">> Starting deep analysis on raw funnel data: {DATA_SOURCE_PATH}")
    df = pd.read_csv(DATA_SOURCE_PATH, low_memory=False)
    
    total_raw = len(df)
    print(f">> Total Raw Cohort Rows: {total_raw}")
    
    # 1. Clean Refund Target
    df['is_refunded'] = (
        (df['Refunded'].astype(str).str.strip().str.lower() == 'true') |
        (df['Mentee Status'].astype(str).str.strip().str.lower() == 'refunded')
    )
    
    global_total = len(df)
    global_refunds = int(df['is_refunded'].sum())
    global_retention_rate = round((1 - (global_refunds / global_total)) * 100, 2)
    global_refund_rate = round((global_refunds / global_total) * 100, 2)
    global_prior = 1 - (global_refunds / global_total)

    print(f">> Global Cohort: {global_total} | Retention: {global_retention_rate}% | Refunds: {global_refund_rate}%")

    # 2. Canonical Column Mapping
    p_series = df['crm_persona'].fillna(df['Lead Persona']).fillna(df['Persona'])
    r_series = df.get('role', pd.Series(index=df.index, dtype='object'))
    e_series = df.get('crm_exact_persona', pd.Series(index=df.index, dtype='object'))

    df['clean_persona'] = [parse_canonical_persona(p, r, e) for p, r, e in zip(p_series, r_series, e_series)]
    df['clean_exp'] = df['Total Work Experience'].apply(parse_work_experience)
    df['clean_program'] = df['Intake Program'].apply(parse_canonical_program)

    # 3. Behavioral Early-Warning Flags
    df['onboarding_done'] = df['Filled Onboarding Form'].astype(str).str.strip().str.lower() == 'true'
    df['sat_attempted'] = df['Attempted Sat'].astype(str).str.strip().str.lower() == 'true'

    # Compute Behavioral Risk Factors
    ob_refund = round(df.groupby('onboarding_done')['is_refunded'].mean() * 100, 1).to_dict()
    sat_refund = round(df.groupby('sat_attempted')['is_refunded'].mean() * 100, 1).to_dict()

    print(f">> Onboarding Form Incomplete -> Refund Rate: {ob_refund.get(False)}% vs Completed: {ob_refund.get(True)}%")
    print(f">> Diagnostic SAT Skipped       -> Refund Rate: {sat_refund.get(False)}% vs Completed: {sat_refund.get(True)}%")

    # 4. Multi-Dimensional Aggregation with Bayesian Smoothing
    # Formula: smoothed_rate = (actual_successes + m * prior) / (cohort_size + m)
    # where m = 15 (smoothing weight)
    M_WEIGHT = 15.0

    records = []
    by_program_stats = {}
    by_program_persona_stats = {}
    by_program_persona_exp_stats = {}

    grouped_3d = df.groupby(['clean_program', 'clean_persona', 'clean_exp'])
    for (prog, persona, exp), g in grouped_3d:
        n = len(g)
        refunds = int(g['is_refunded'].sum())
        successes = n - refunds
        raw_retention = (successes / n) * 100
        raw_refund = (refunds / n) * 100

        # Bayesian smoothing
        smoothed_retention = ((successes + M_WEIGHT * global_prior) / (n + M_WEIGHT)) * 100
        smoothed_refund = 100.0 - smoothed_retention

        key_3d = f"{prog}___{persona}___{exp}"
        stat_item = {
            'program': prog,
            'persona': persona,
            'experience': exp,
            'cohort_size': n,
            'refunds': refunds,
            'raw_retention_rate': round(raw_retention, 1),
            'raw_refund_rate': round(raw_refund, 1),
            'smoothed_retention_rate': round(smoothed_retention, 1),
            'smoothed_refund_rate': round(smoothed_refund, 1),
            'risk_level': 'High Retention' if smoothed_retention >= 80 else ('Moderate' if smoothed_retention >= 75 else 'High Risk')
        }
        by_program_persona_exp_stats[key_3d] = stat_item
        records.append(stat_item)

    # 2D Aggregation: Program x Persona
    grouped_2d = df.groupby(['clean_program', 'clean_persona'])
    for (prog, persona), g in grouped_2d:
        n = len(g)
        refunds = int(g['is_refunded'].sum())
        successes = n - refunds
        smoothed_retention = ((successes + M_WEIGHT * global_prior) / (n + M_WEIGHT)) * 100
        smoothed_refund = 100.0 - smoothed_retention
        
        key_2d = f"{prog}___{persona}"
        by_program_persona_stats[key_2d] = {
            'program': prog,
            'persona': persona,
            'cohort_size': n,
            'refunds': refunds,
            'retention_rate': round(smoothed_retention, 1),
            'refund_rate': round(smoothed_refund, 1),
            'risk_level': 'High Retention' if smoothed_retention >= 80 else ('Moderate' if smoothed_retention >= 75 else 'High Risk')
        }

    # Program-level Aggregation
    grouped_prog = df.groupby('clean_program')
    for prog, g in grouped_prog:
        n = len(g)
        refunds = int(g['is_refunded'].sum())
        ret = round(((n - refunds) / n) * 100, 1)
        ref = round((refunds / n) * 100, 1)
        by_program_stats[prog] = {
            'program': prog,
            'cohort_size': n,
            'refunds': refunds,
            'retention_rate': ret,
            'refund_rate': ref
        }

    # Export clean matrix CSV
    matrix_df = pd.DataFrame(records).sort_values(['program', 'cohort_size'], ascending=[True, False])
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    matrix_df.to_csv(MATRIX_CSV_PATH, index=False)
    print(f">> Empirical Matrix CSV saved to: {MATRIX_CSV_PATH} ({len(matrix_df)} cohorts)")

    # Export structured JSON
    full_matrix_dict = {
        'metadata': {
            'total_funnel_records': global_total,
            'global_retention_rate': global_retention_rate,
            'global_refund_rate': global_refund_rate,
            'behavioral_triggers': {
                'onboarding_form_drop_refund': ob_refund.get(False),
                'onboarding_form_done_refund': ob_refund.get(True),
                'diagnostic_sat_skipped_refund': sat_refund.get(False),
                'diagnostic_sat_taken_refund': sat_refund.get(True)
            }
        },
        'by_program': by_program_stats,
        'by_program_persona': by_program_persona_stats,
        'by_program_persona_exp': by_program_persona_exp_stats
    }

    with open(MATRIX_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(full_matrix_dict, f, indent=2)
    print(f">> Structured Matrix JSON saved to: {MATRIX_JSON_PATH}")

    return full_matrix_dict

if __name__ == '__main__':
    run_cleaning_and_build_matrix()
