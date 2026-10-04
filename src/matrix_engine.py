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
    if any(k in s for k in ['fde', 'forward', 'program 3']) or re.search(r'\bp3\b', s):
        return 'P3_FDE'
    elif any(k in s for k in ['aiml', 'agentic', 'deep learning', 'program 4']) or re.search(r'\bp4\b', s):
        return 'P4_AIML'
    elif any(k in s for k in ['dsml', 'data', 'analytics', 'program 2']) or re.search(r'\bp2\b', s):
        return 'P2_DSML'
    elif any(k in s for k in ['devop', 'cloud', 'program 5']) or re.search(r'\bp5\b', s):
        return 'P5_DEVOPS'
    return 'P1_ACADEMY'

# ==============================================================================
# ENCYCLOPEDIC GLOBAL PROFESSION TAXONOMY & DOMAIN CLASSIFIER
# Covers every real-world career domain across healthcare, security, trades,
# education, hospitality, logistics, public sector, retail, corporate, and arts.
# ==============================================================================

CANONICAL_PERSONA_NAMES = {
    'NON_TECH': 'Non-Tech / Career Switcher',
    'QA_SDET': 'QA / SDET / Testing',
    'DATA_ANALYST': 'Data & Analytics',
    'DEVOPS_CLOUD': 'DevOps & Cloud Platform',
    'SYSTEMS_ENG': 'Systems & Embedded Engineering',
    'LEADERSHIP': 'Engineering Leadership / Management',
    'FRONTEND': 'Frontend Engineering',
    'IT_SERVICES': 'General IT Services / Maintenance',
    'SWE_BACKEND': 'Software Engineering (Backend/FullStack)',
}

def match_token(text, token):
    """
    Matches a token safely inside text.
    For short acronyms (<= 3 chars, e.g. swe, sde, qa, ml, ai, ca, hr, bi, ui, ux, pr)
    or collision-prone terms ('defense', 'defence', 'mechanic', 'guard', 'lead', 'cleaner', 'sweeper', 'maid', 'cook'),
    enforces strict regex word boundaries (\b) to prevent false substring collisions
    (e.g., 'sweeper' matching 'swe', or 'waiter' matching 'ai').
    """
    t = str(token).lower()
    s = str(text).lower()
    if len(t) <= 3 or t in ['defense', 'defence', 'mechanic', 'guard', 'lead', 'cleaner', 'sweeper', 'maid', 'cook']:
        return bool(re.search(r'\b' + re.escape(t) + r'\b', s))
    return t in s

def match_any(text, tokens):
    return any(match_token(text, t) for t in tokens)

def classify_world_domain(role_str):
    """
    Identifies the real-world career domain / industry sector for any profession on Earth.
    Covers 19 exhaustive global career families with exact token collision safeguards.
    """
    s = str(role_str).lower().strip()
    
    # 1. Healthcare, Medicine & Clinical Services
    if match_any(s, [
        'nurse', 'nursing', 'doctor', 'physician', 'surgeon', 'dentist', 'dental', 'pharmacist',
        'pharmacy', 'chemist', 'paramedic', 'emt', 'ambulance', 'physiotherapist', 'physiotherapy',
        'radiologist', 'radiology', 'sonographer', 'lab technician', 'pathologist', 'pathology',
        'clinical', 'clinic', 'hospital', 'healthcare', 'health care', 'optometrist', 'ophthalmologist',
        'veterinarian', 'dietitian', 'nutritionist', 'phlebotomist', 'caregiver', 'ward boy', 'orderly',
        'anesthesiologist', 'cardiologist', 'dermatologist', 'pediatrician', 'psychiatrist', 'psychologist',
        'therapist', 'midwife'
    ]):
        return 'Healthcare & Medical Services'

    # 2. Legal, Compliance & Judiciary (Evaluated before defense to catch 'Criminal Defense Lawyer')
    if match_any(s, [
        'lawyer', 'advocate', 'attorney', 'legal', 'paralegal', 'solicitor', 'barrister', 'notary',
        'judge', 'magistrate', 'public prosecutor', 'legal counsel', 'compliance officer', 'law clerk'
    ]):
        return 'Legal, Compliance & Judiciary'

    # 3. Security, Defense & Law Enforcement
    if match_any(s, [
        'security guard', 'security officer', 'guard', 'watchman', 'chowkidar', 'bouncer', 'bodyguard',
        'police', 'cop', 'constable', 'inspector', 'sho', 'law enforcement', 'detective', 'investigator',
        'military', 'army', 'navy', 'air force', 'armed forces', 'defense', 'defence', 'paramilitary',
        'firefighter', 'fireman', 'corrections officer', 'jailer', 'warden', 'border patrol', 'coast guard'
    ]):
        return 'Security & Protective Services'

    # 4. Education, Teaching & Academia
    if match_any(s, [
        'teacher', 'school teacher', 'professor', 'lecturer', 'tutor', 'tuition', 'instructor',
        'educator', 'faculty', 'dean', 'principal', 'headmaster', 'headmistress', 'academic counselor',
        'librarian', 'pedagogy', 'scholar', 'trainer'
    ]):
        return 'Education & Academia'

    # 5. Hospitality, Facility & Cleaning Services (Catches Sweeper, Janitor, Chef, Hotel Staff)
    if match_any(s, [
        'sweeper', 'cleaner', 'janitor', 'housekeeper', 'housekeeping', 'sanitation', 'waste management',
        'maid', 'laundry', 'chef', 'cook', 'baker', 'bakery', 'barista', 'bartender', 'waiter', 'waitress',
        'server', 'steward', 'restaurant', 'cafe', 'hotel', 'hospitality', 'concierge', 'sommelier',
        'tour guide', 'flight attendant', 'cabin crew', 'air hostess'
    ]):
        return 'Hospitality & Facility Services'

    # 6. Traditional Engineering & Physical Sciences (Non-CS) (Evaluated before trades to catch Mechanical Engineer)
    if match_any(s, [
        'mechanical engineer', 'mechanical', 'civil engineer', 'civil', 'chemical engineer', 'chemical',
        'petroleum', 'mining', 'metallurgy', 'aerospace', 'aeronautical', 'biotech', 'biotechnology',
        'biomedical', 'textile', 'automobile engineer', 'automotive engineer', 'environmental engineer',
        'structural engineer', 'physicist', 'chemist', 'geologist'
    ]) or ('electrical' in s and 'hardware' not in s and 'software' not in s):
        return 'Traditional Engineering (Non-CS)'

    # 7. Skilled Trades, Crafts & Construction Maintenance
    if match_any(s, [
        'electrician', 'plumber', 'carpenter', 'welder', 'machinist', 'mechanic', 'auto mechanic',
        'car mechanic', 'motor mechanic', 'fitter', 'turner', 'mason', 'masonry', 'construction',
        'builder', 'painter', 'hvac', 'appliance repair', 'blacksmith', 'locksmith', 'tailor', 'cobbler',
        'weaver', 'factory worker'
    ]):
        return 'Trades, Crafts & Construction'

    # 8. Transportation, Logistics & Aviation
    if match_any(s, [
        'pilot', 'commercial pilot', 'airline pilot', 'mariner', 'sailor', 'merchant navy', 'ship captain',
        'loco pilot', 'train driver', 'truck driver', 'chauffeur', 'driver', 'delivery partner', 'delivery boy',
        'delivery agent', 'courier', 'rider', 'warehouse', 'forklift', 'cargo', 'stevedore', 'logistics', 'supply chain'
    ]):
        return 'Transportation & Logistics'

    # 9. Commerce, Category & Merchandising
    if match_any(s, [
        'category manager', 'category lead', 'category head', 'category', 'catalog', 'pricing', 'e-commerce',
        'ecommerce', 'merchandiser', 'merchandise', 'store associate', 'cashier', 'retail', 'shopkeeper',
        'counter sales', 'store manager'
    ]):
        return 'Commerce, Category & Retail'

    # 10. Sales, Commercial & Real Estate
    if match_any(s, [
        'sales', 'business development', 'bde', 'bda', 'inside sales', 'field sales', 'account executive',
        'realtor', 'real estate', 'broker', 'relationship manager', 'telecaller', 'tele-caller', 'telesales', 'telemarketing'
    ]):
        return 'Sales & Business Development'

    # 11. Marketing, Advertising, PR & Media
    if match_any(s, [
        'marketing', 'seo', 'sem', 'social media', 'content writer', 'copywriter', 'branding', 'pr executive',
        'public relations', 'advertising', 'journalist', 'reporter', 'news anchor', 'video editor', 'photographer',
        'animator', 'graphic designer', 'artist', 'musician', 'author', 'editor'
    ]):
        return 'Marketing, Media & Design'

    # 12. Finance, Banking, Accounting & Audit
    if match_any(s, [
        'accountant', 'accounting', 'chartered accountant', 'ca', 'cpa', 'auditor', 'bookkeeper',
        'taxation', 'tax consultant', 'billing', 'banking', 'bank officer', 'bank teller', 'bank manager',
        'loan officer', 'insurance', 'underwriter', 'actuary', 'investment banker', 'wealth manager'
    ]):
        return 'Finance, Banking & Accounting'

    # 13. Human Resources & Talent Acquisition
    if match_any(s, [
        'hr', 'human resource', 'recruiter', 'recruiting', 'talent acquisition', 'staffing',
        'people partner', 'people ops', 'hrbp', 'payroll'
    ]):
        return 'HR & People Operations'

    # 14. Customer Experience, Support & Operations
    if match_any(s, [
        'customer service', 'customer support', 'customer care', 'call center', 'bpo', 'kpo',
        'receptionist', 'front desk', 'helpdesk', 'service desk', 'customer success', 'csm', 'technical support'
    ]):
        return 'Customer Support & Operations'

    # 15. Product Management & UI/UX Design
    if match_any(s, [
        'product manager', 'associate product manager', 'apm', 'technical product manager', 'tpm',
        'product owner', 'scrum master', 'agile coach', 'ui/ux', 'ux designer', 'product designer',
        'ui designer', 'interaction designer'
    ]):
        return 'Product Management & Design'

    # 16. Consulting, Strategy & General Management
    if match_any(s, [
        'management consultant', 'strategy consultant', 'corporate strategy', 'operations manager',
        'general manager', 'business manager', 'project manager', 'program manager', 'pmo', 'operations lead'
    ]):
        return 'Business Operations & Management'

    # 17. Public Administration, Civil Services & Agriculture
    if match_any(s, [
        'civil servant', 'ias', 'ips', 'upsc', 'government officer', 'govt officer', 'clerk',
        'farmer', 'farming', 'agriculture', 'agronomist', 'horticulturist', 'dairy', 'forestry', 'geologist'
    ]):
        return 'Public Administration & Agriculture'

    # 18. Students, Freshers & Career Transitions
    if match_any(s, [
        'student', 'learner', 'intern', 'fresher', 'non coder', 'non-coder', 'non-tech', 'non tech',
        'zero code', 'career break', 'break', 'sabbatical', 'gap year', 'homemaker', 'housewife', 'restart'
    ]):
        return 'Early Career & Career Transitions'

    # 19. Technical Engineering Domains
    if match_any(s, ['test', 'qa', 'sdet', 'automation tester', 'manual test', 'quality analyst', 'quality assurance']):
        return 'Quality Assurance & SDET'
    elif match_any(s, ['data scientist', 'data analyst', 'data engineer', 'analytics', 'bi', 'business intelligence', 'power bi', 'tableau', 'machine learning', 'ml engineer', 'mle', 'ai engineer', 'deep learning']):
        return 'Data Science & Analytics'
    elif match_any(s, ['devops', 'sre', 'cloud', 'infrastructure', 'docker', 'kubernetes', 'platform engineer', 'terraform', 'sysadmin', 'system administrator', 'security engineer', 'cyber security', 'infosec', 'network engineer']):
        return 'DevOps & Cloud Platform'
    elif match_any(s, ['embedded', 'hardware', 'firmware', 'vlsi', 'iot', 'linux kernel', 'device driver']):
        return 'Systems & Embedded Engineering'
    elif match_any(s, ['frontend', 'front-end', 'ui dev', 'react', 'angular', 'web developer', 'vue']):
        return 'Frontend Engineering'
    elif match_any(s, [
        'engineering manager', 'tech lead', 'technical lead', 'software manager', 'dev manager',
        'technical architect', 'solutions architect', 'enterprise architect', 'cto', 'vp of engineering',
        'director of engineering', 'chief technology officer'
    ]) or (match_any(s, ['manager', 'director', 'founder', 'vp', 'architect', 'lead']) and match_any(s, ['software', 'tech', 'dev', 'engineering', 'platform', 'cloud', 'data'])):
        return 'Engineering Leadership'
    elif match_any(s, ['it service', 'general it', 'app support', 'desktop support', 'production support']):
        return 'IT Services & Maintenance'
    elif match_any(s, ['software', 'developer', 'programmer', 'sde', 'swe', 'backend', 'back-end', 'fullstack', 'full-stack', 'java dev', 'python dev', 'golang', 'node', 'django', 'spring boot']):
        return 'Software Engineering (Backend/FullStack)'

    return 'Non-Tech / General Career Background'

def canonical_persona_key(persona_str):
    """
    Maps ANY job title or persona string in the world to its canonical Scaler taxonomy key.
    Enforces the Golden Principle: unknown roles without explicit software/tech markers
    safely and universally classify as 'NON_TECH', never as 'SWE_BACKEND'.
    """
    raw_str = str(persona_str).strip()
    if raw_str in CANONICAL_PERSONA_NAMES:
        return raw_str
    for k, name in CANONICAL_PERSONA_NAMES.items():
        if raw_str.lower() == name.lower():
            return k
    s = raw_str.lower().replace('_', ' ')


    # --------------------------------------------------------------------------
    # 1. NON-TECH GLOBAL DOMAINS (Explicit Real-World Vocations)
    # --------------------------------------------------------------------------
    if any(k in s for k in [
        # Healthcare & Medicine (Nurse, Doctor, Pharmacist, Lab Tech, etc.)
        'nurse', 'nursing', 'doctor', 'physician', 'surgeon', 'dentist', 'dental', 'pharmacist',
        'pharmacy', 'chemist', 'paramedic', 'emt', 'ambulance', 'physiotherapist', 'physiotherapy',
        'radiologist', 'radiology', 'sonographer', 'lab technician', 'pathologist', 'pathology',
        'clinical', 'clinic', 'hospital', 'healthcare', 'health care', 'optometrist', 'veterinarian', 'dietitian',
        'nutritionist', 'phlebotomist', 'caregiver', 'ward boy', 'orderly', 'anesthesiologist',

        # Security, Defense & Protective Services (Guard, Police, Army, etc.)
        'security guard', 'security officer', 'guard', 'watchman', 'chowkidar', 'bouncer', 'bodyguard',
        'police', 'cop', 'constable', 'inspector', 'sho', 'law enforcement', 'detective', 'military',
        'army', 'navy', 'air force', 'armed forces', 'defense', 'defence', 'paramilitary',
        'firefighter', 'fireman', 'corrections officer', 'jailer', 'warden', 'border patrol',

        # Education, Teaching & Academia
        'teacher', 'school teacher', 'professor', 'lecturer', 'tutor', 'tuition', 'instructor',
        'educator', 'faculty', 'dean', 'principal', 'headmaster', 'headmistress', 'academic counselor',
        'librarian', 'pedagogy',

        # Hospitality, Facility & Cleaning Services
        'sweeper', 'cleaner', 'janitor', 'housekeeper', 'housekeeping', 'sanitation', 'maid', 'laundry',
        'chef', 'cook', 'baker', 'bakery', 'barista', 'bartender', 'waiter', 'waitress', 'server',
        'steward', 'restaurant', 'cafe', 'hotel', 'hospitality', 'concierge',
        'travel agent', 'tour guide', 'flight attendant', 'cabin crew', 'air hostess', 'sommelier',

        # Trades, Crafts & Construction
        'electrician', 'plumber', 'carpenter', 'welder', 'machinist', 'mechanic', 'auto mechanic',
        'fitter', 'turner', 'mason', 'masonry', 'construction', 'builder', 'painter', 'hvac',
        'appliance repair', 'blacksmith', 'locksmith', 'tailor', 'cobbler', 'weaver', 'factory worker',

        # Transportation & Logistics
        'driver', 'chauffeur', 'truck driver', 'delivery boy', 'delivery partner', 'delivery agent',
        'courier', 'rider', 'pilot', 'loco pilot', 'train driver', 'mariner', 'sailor', 'warehouse',
        'forklift', 'cargo', 'stevedore', 'logistics', 'supply chain',

        # Retail, Commerce, Category & Merchandising
        'cashier', 'store associate', 'retail', 'shopkeeper', 'counter sales', 'merchandiser', 'merchandise',
        'category manager', 'category lead', 'category head', 'category', 'catalog', 'pricing', 'e-commerce', 'ecommerce',
        'customer service', 'customer support', 'customer care', 'call center', 'bpo', 'kpo',
        'telecaller', 'tele-caller', 'telemarketing', 'front desk', 'receptionist',

        # Corporate HR, Sales, Marketing, Finance, Legal
        'hr', 'human resource', 'recruiter', 'recruiting', 'talent acquisition', 'staffing',
        'people partner', 'people ops', 'hrbp', 'payroll',
        'sales', 'business development', 'bde', 'bda', 'inside sales', 'field sales', 'account executive',
        'realtor', 'real estate', 'broker', 'relationship manager',
        'marketing', 'seo', 'sem', 'social media', 'content writer', 'copywriter', 'branding', 'pr executive',
        'accountant', 'accounting', 'chartered accountant', 'ca ', 'cpa', 'auditor', 'bookkeeper',
        'taxation', 'tax consultant', 'billing', 'banking', 'bank officer', 'bank teller', 'loan officer',
        'insurance', 'underwriter', 'actuary',
        'lawyer', 'advocate', 'attorney', 'legal', 'paralegal', 'solicitor', 'barrister', 'notary',
        'compliance', 'judge', 'magistrate', 'civil servant', 'ias', 'ips', 'upsc', 'government officer',
        'govt officer', 'clerk',

        # Traditional Engineering (Non-CS)
        'mechanical', 'civil', 'chemical', 'petroleum', 'mining', 'metallurgy',
        'aerospace', 'aeronautical', 'biotech', 'biotechnology', 'biomedical', 'textile', 'automobile engineer',

        # Media, Arts, Agriculture & Gaps
        'graphic designer', 'illustrator', 'photographer', 'videographer', 'video editor', 'animator',
        'interior designer', 'fashion designer', 'artist', 'musician', 'singer', 'actor', 'journalist', 'reporter',
        'farmer', 'farming', 'agriculture', 'agronomist', 'horticulturist', 'dairy', 'forestry', 'geologist',
        'student', 'learner', 'intern', 'fresher', 'non coder', 'non-coder', 'non-tech', 'non tech',
        'zero code', 'career break', 'break', 'sabbatical', 'gap year', 'homemaker', 'housewife', 'restart'
    ]):
        # Protect dual-context roles like "Software Engineer at Hospital" or "Data Analyst in Healthcare"
        has_explicit_tech = any(match_token(s, t) for t in [
            'software engineer', 'software developer', 'backend developer', 'frontend developer',
            'full stack', 'fullstack', 'data analyst', 'data scientist', 'devops engineer',
            'cloud engineer', 'qa engineer', 'sdet', 'systems engineer', 'programmer', 'sde', 'swe',
            'ml engineer', 'machine learning', 'ai engineer', 'cyber security', 'security engineer',
            'security analyst', 'network engineer', 'cloud architect', 'devops', 'sre'
        ])
        if not has_explicit_tech:
            return 'NON_TECH'

    # --------------------------------------------------------------------------
    # 2. TECHNICAL ROLE CLASSIFICATION
    # --------------------------------------------------------------------------
    # QA / SDET / Testing
    if any(match_token(s, k) for k in ['test', 'qa', 'sdet', 'automation tester', 'manual test', 'quality analyst', 'quality assurance']):
        return 'QA_SDET'

    # Data Science & Machine Learning / Analytics
    if any(match_token(s, k) for k in [
        'data scientist', 'data analyst', 'data engineer', 'analytics', 'bi', 'business intelligence',
        'power bi', 'tableau', 'machine learning', 'ml engineer', 'mle', 'ai engineer', 'nlp',
        'computer vision', 'deep learning', 'applied scientist', 'analytics engineer'
    ]):
        return 'DATA_ANALYST'

    # DevOps, Cloud, Security & Infrastructure Platform
    if any(match_token(s, k) for k in [
        'devops', 'sre', 'cloud', 'infrastructure', 'docker', 'kubernetes', 'platform engineer',
        'terraform', 'sysadmin', 'system administrator', 'security', 'cyber security', 'infosec',
        'soc analyst', 'penetration test', 'network engineer', 'cloud architect', 'systems engineer',
        'site reliability', 'it infrastructure'
    ]):
        return 'DEVOPS_CLOUD'

    # Systems & Embedded Engineering
    if any(match_token(s, k) for k in ['embedded', 'hardware', 'firmware', 'vlsi', 'iot', 'linux kernel', 'device driver']):
        return 'SYSTEMS_ENG'

    # Technical Engineering Leadership
    if any(match_token(s, k) for k in [
        'engineering manager', 'tech lead', 'technical lead', 'software manager', 'development manager',
        'technical architect', 'solutions architect', 'enterprise architect', 'cto', 'vp of engineering',
        'director of engineering', 'chief technology officer'
    ]):
        return 'LEADERSHIP'

    # Frontend Engineering
    if any(match_token(s, k) for k in ['frontend', 'front-end', 'ui/ux', 'ui dev', 'react', 'angular', 'web developer']):
        return 'FRONTEND'

    # General IT Services & Maintenance
    if any(match_token(s, k) for k in ['maintenance', 'support', 'it service', 'general it', 'service based', 'production support', 'app support', 'desktop support', 'service desk', 'helpdesk']):
        return 'IT_SERVICES'

    # Core Software Engineering (Backend / Full Stack)
    if any(match_token(s, k) for k in [
        'software', 'developer', 'programmer', 'coding', 'coder', 'sde', 'swe',
        'backend', 'back-end', 'fullstack', 'full-stack', 'java dev', 'python dev',
        'c++', 'c#', '.net', 'golang', 'node', 'django', 'spring boot', 'android', 'ios'
    ]):
        return 'SWE_BACKEND'

    # --------------------------------------------------------------------------
    # 3. UNIVERSAL SAFE FALLBACK
    # If a role has NO verified software or technical engineering keywords,
    # it safely defaults to NON_TECH (Career Switcher), never SWE_BACKEND!
    # --------------------------------------------------------------------------
    return 'NON_TECH'


def canonical_exp_key(exp_str):
    if exp_str is None:
        return 'EXP_1_3'
    s = str(exp_str).strip().lower()
    
    # 1. Check if a 4-digit graduation year is present (e.g. Batch 2025, Batch 2023, Batch 2012)
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

    # 2. Check compound years and months like "5 years 6 months", "3 yrs 4 mos"
    compound = re.search(r'(\d+(?:\.\d+)?)\s*(?:yrs|yr|years?)\s*(?:and\s*)?(\d+(?:\.\d+)?)\s*(?:mos|mo|months?)', s)
    if compound:
        try:
            val = float(compound.group(1)) + float(compound.group(2)) / 12.0
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

    # Numeric extraction for actual YOE (handles 8.0 yrs, 2.5 years, 0 years, 18 months)
    match = re.search(r'[-+]?\d*\.?\d+', s.replace(',', ''))
    if match and match.group():
        try:
            val = float(match.group())
            # Convert months ONLY if text has month indicators AND does NOT have year indicators
            has_month = any(m in s for m in ['month', 'mo', 'mth'])
            has_year = any(y in s for y in ['year', 'yr'])
            if has_month and not has_year:
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

# Helper aliases
normalize_persona = lambda raw_persona, raw_role: canonical_persona_key(f"{raw_persona} {raw_role}")
normalize_experience = lambda exp_val: canonical_exp_key(exp_val)
normalize_program = lambda prog_val: canonical_prog_key(prog_val)
def get_canonical_persona_name(key_or_str):
    if key_or_str in CANONICAL_PERSONA_NAMES:
        return CANONICAL_PERSONA_NAMES[key_or_str]
    norm_key = canonical_persona_key(key_or_str)
    return CANONICAL_PERSONA_NAMES.get(norm_key, 'Non-Tech / Career Switcher')

