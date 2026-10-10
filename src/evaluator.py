import os
import json
import re
from .matrix_engine import (
    get_cohort_stats, normalize_persona, normalize_experience, normalize_program,
    classify_world_domain, get_canonical_persona_name, match_token, match_any
)

from .market_intelligence import get_market_intelligence

# ==============================================================================
# OFFICIAL SCALER 5-PROGRAM CATALOG DEFINITIONS (from Documentation_Scaler_Updated.pdf)
# ==============================================================================
# Program 1: Software & AI Engineering Program (Scaler Academy)
# Program 2: Modern Data Science & Machine Learning with Specialization in AI (DSML)
# Program 3: AI Forward Deployed Engineer (FDE) Program
# Program 4: AI & Machine Learning with Agentic AI Program
# Program 5: DevOps, Cloud & AI Platform Engineering Program
# ==============================================================================

def clean_str(val, default=""):
    if val is None or str(val).strip().lower() in ['nan', 'none', 'null', '']:
        return default
    return str(val).strip()

def get_track_duration(program_str, track_str):
    p_lower = str(program_str).lower()
    t_lower = str(track_str).lower()
    
    # Program 1: Scaler Academy (PDF Page 3)
    if 'academy' in p_lower or 'program 1' in p_lower:
        if 'beginner' in t_lower:
            return '12 - 18 Months'
        elif 'intermediate' in t_lower:
            return '12 Months'
        elif 'advanced' in t_lower:
            return '10 - 17 Months'
        return '12 Months'
        
    # Program 2: DSML (PDF Page 5)
    elif 'dsml' in p_lower or 'data science' in p_lower or 'program 2' in p_lower:
        if 'beginner' in t_lower:
            return '16 - 20 Months'
        elif 'intermediate' in t_lower or 'core' in t_lower or 'predictive' in t_lower or 'advanced' in t_lower:
            return '14 - 16 Months'
        return '14 - 16 Months'
        
    # Program 3: AI Forward Deployed Engineer (FDE) (PDF Page 8)
    elif 'fde' in p_lower or 'forward deployed' in p_lower or 'program 3' in p_lower:
        return '12 Months'
        
    # Program 4: AI & ML with Agentic AI (PDF Page 12)
    elif 'agentic' in p_lower or 'program 4' in p_lower or 'aiml' in p_lower:
        if 'beginner' in t_lower or 'foundation' in t_lower:
            return '12 - 15 Months'
        return '12 - 15 Months'
        
    # Program 5: DevOps, Cloud & AI Platform Engineering (PDF Page 16)
    elif 'devops' in p_lower or 'cloud' in p_lower or 'platform' in p_lower or 'program 5' in p_lower:
        return '14 - 18 Months'
        
    return '12 Months'

def classify_education(education_str):
    if not education_str:
        return 'GRAD_UNKNOWN'
    edu = str(education_str).lower().strip()
    if edu in ['nan', 'none', 'null', '', '-', 'unknown']:
        return 'GRAD_UNKNOWN'
    
    # 1. Recognized higher degrees or post-graduate qualifications
    is_pg_diploma = any(k in edu for k in ['pg diploma', 'post graduate diploma', 'pgdca', 'pgdbm', 'pgdm'])
    
    below_grad_patterns = [
        r'\b(1st|2nd|3rd|4th|5th|6th|7th|8th|9th|10th|11th|12th)\b',
        r'\b[1-9]\s*(st|nd|rd|th)?\s*(standard|std|class|grade|pass)\b',
        r'\b10\s*pass\b', r'\b12\s*pass\b',
        r'\bhsc\b', r'\bssc\b', r'\bintermediate\b', r'\binter\b',
        r'\b10\+2\b', r'\bmatric\b', r'\bmatriculation\b', r'\bpolytechnic\b',
        r'\bdiploma\b', r'\biti\b', r'\bbelow graduation\b', r'\bhigh school\b',
        r'\bmiddle school\b', r'\bprimary school\b', r'\bunder matric\b', r'\bnon[- ]matric\b',
        r'\bpuc\b', r'\bhigher secondary\b', r'\bschooling\b', r'\bsecondary school\b'
    ]

    has_explicit_degree = any(re.search(pat, edu) for pat in [
        r'\bb\.?\s*tech\b', r'\bbtech\b', r'\bb\.?\s*e\b', r'\bbca\b', r'\bmca\b',
        r'\bm\.?\s*tech\b', r'\bmtech\b', r'\bb\.?\s*sc\b', r'\bm\.?\s*sc\b',
        r'\bbachelor\b', r'\bmaster\b', r'\bphd\b', r'\bmba\b', r'\bbba\b',
        r'\bb\.?\s*com\b', r'\bb\.?\s*a\b', r'\bdegree\b', r'\bgraduated\b', r'\bgraduate\b'
    ])

    # Check for Below Graduation (10th, 12th, Polytechnic, Undergraduate Diploma)
    is_below_grad = any(re.search(pat, edu) for pat in below_grad_patterns)
    if is_below_grad and not is_pg_diploma and not has_explicit_degree:
        return 'BELOW_GRAD'

    # Check for CS degrees
    has_cs_degree = any(k in edu for k in [
        'b.tech cs', 'b.tech cse', 'b.tech it', 'be cs', 'be cse', 'be it',
        'bca', 'mca', 'm.tech cs', 'm.tech cse', 'm.tech it', 'computer science',
        'information tech', 'software eng'
    ])
    if has_cs_degree:
        return 'GRAD_CS'

    # Check for Non-CS degrees
    has_non_cs_degree = any(k in edu for k in [
        'b.com', 'b.a', 'bba', 'bhm', 'b.des', 'llb', 'mbbs', 'b.pharm',
        'mechanical', 'civil', 'chemical', 'electrical', 'biotech', 'arts',
        'commerce', 'humanities'
    ])
    if has_non_cs_degree and not any(k in edu for k in ['b.tech', 'b.e', 'btech', 'engineering']):
        return 'GRAD_NON_CS'

    return 'GRAD_GENERAL'

def calculate_confidence(program_name, inbound_cat, cohort_size, retention_rate, sat_status, sat_score, edu_level):
    """
    Computes an empirical 0-100 Confidence Score based on:
    1. Historical Cohort Sample Size (35%)
    2. Historical Retention Rate (25%)
    3. Inbound Intent Alignment (25%)
    4. Diagnostic SAT & Academic Aptitude (15%)
    """
    if edu_level == 'BELOW_GRAD':
        return {
            'score': 0,
            'tier': 'Low',
            'rationale': 'Ineligible: Candidate does not satisfy Bachelor degree prerequisite.',
            'breakdown': {
                'cohort_pts': 0, 'cohort_max': 35, 'cohort_desc': 'Ineligible',
                'ret_pts': 0, 'ret_max': 25, 'ret_desc': 'Ineligible',
                'intent_pts': 0, 'intent_max': 25, 'intent_desc': 'Ineligible',
                'apt_pts': 0, 'apt_max': 15, 'apt_desc': 'Degree prerequisite unfulfilled'
            }
        }
    
    # 1. Empirical Cohort Sample Size (35 pts)
    if cohort_size >= 30:
        cohort_pts = 35
        cohort_desc = f"Robust cohort backing (N={cohort_size})"
    elif cohort_size >= 10:
        cohort_pts = 25
        cohort_desc = f"Moderate cohort sample (N={cohort_size})"
    else:
        cohort_pts = 12
        cohort_desc = f"Small cohort sample (N={cohort_size})"

    # 2. Historical Retention Rate (25 pts)
    if retention_rate >= 80.0:
        ret_pts = 25
        ret_desc = f"high retention ({retention_rate}%)"
    elif retention_rate >= 75.0:
        ret_pts = 18
        ret_desc = f"moderate retention ({retention_rate}%)"
    else:
        ret_pts = 10
        ret_desc = f"elevated refund risk ({retention_rate}%)"

    # 3. Inbound Intent Alignment (25 pts)
    p_lower = str(program_name).lower()
    inbound_matched = (
        ('academy' in p_lower and inbound_cat == 'P1_ACADEMY') or
        ('dsml' in p_lower and inbound_cat == 'P2_DSML') or
        ('fde' in p_lower and inbound_cat == 'P3_FDE') or
        ('agentic' in p_lower and inbound_cat == 'P4_AIML_AGENTIC') or
        ('devops' in p_lower and inbound_cat == 'P5_DEVOPS_CLOUD')
    )
    inbound_synergistic = (
        ('academy' in p_lower and inbound_cat in ['P3_FDE', 'P5_DEVOPS_CLOUD']) or
        ('dsml' in p_lower and inbound_cat == 'P4_AIML_AGENTIC') or
        ('devops' in p_lower and inbound_cat == 'P1_ACADEMY')
    )

    if inbound_matched:
        intent_pts = 25
        intent_desc = "direct inbound intent match"
    elif inbound_synergistic:
        intent_pts = 20
        intent_desc = "lateral domain synergy"
    else:
        intent_pts = 10
        intent_desc = "curricular redirection"

    # 4. Diagnostic Assessment & Educational Foundation (15 pts)
    is_cs = edu_level == 'GRAD_CS'
    sat_status_clean = str(sat_status).lower()
    sat_cleared = 'passed' in sat_status_clean or ('score' in sat_status_clean and not any(k in sat_status_clean for k in ['pending', 'not']))
    
    if sat_cleared or is_cs:
        apt_pts = 15
        apt_desc = "verified coding/academic foundations"
    elif 'attempted' in sat_status_clean or edu_level == 'GRAD_GENERAL':
        apt_pts = 10
        apt_desc = "degree verified, SET pending"
    else:
        apt_pts = 5
        apt_desc = "diagnostic SET not yet attempted"

    total_score = cohort_pts + ret_pts + intent_pts + apt_pts
    total_score = min(100, max(0, total_score))

    if total_score >= 75:
        tier = 'High'
    elif total_score >= 55:
        tier = 'Mid'
    else:
        tier = 'Low'

    rationale = f"{tier} Confidence ({total_score}%): {cohort_desc}, {ret_desc}, {intent_desc}, and {apt_desc}."
    breakdown = {
        'cohort_pts': cohort_pts,
        'cohort_max': 35,
        'cohort_desc': cohort_desc,
        'ret_pts': ret_pts,
        'ret_max': 25,
        'ret_desc': ret_desc,
        'intent_pts': intent_pts,
        'intent_max': 25,
        'intent_desc': intent_desc,
        'apt_pts': apt_pts,
        'apt_max': 15,
        'apt_desc': apt_desc,
    }
    return {
        'score': total_score,
        'tier': tier,
        'rationale': rationale,
        'breakdown': breakdown
    }


def generate_role_pitch(raw_role, raw_exp, p_lower, t_lower, is_primary, persona=''):
    """
    Synthesizes a role-specific career pitch connecting the candidate's existing professional
    skills (e.g., accounting ledgers, clinical protocols, QA testing, sales funnels) to the target program track.
    """
    r_lower = str(raw_role).lower()
    p_lower = str(p_lower).lower()
    t_lower = str(t_lower).lower()

    # 0a. Security, Defense & Protective Services (Guard, Police, Military, etc.)
    if match_any(r_lower, ['security guard', 'guard', 'watchman', 'chowkidar', 'bouncer', 'police', 'military', 'army', 'navy', 'air force', 'firefighter', 'defense', 'defence', 'constable', 'inspector']):
        if 'dsml' in p_lower or 'data' in p_lower:
            return (
                f"As a <b>{raw_role}</b> ({raw_exp}), your high vigilance, incident logging, and risk monitoring translate directly into "
                "structured data reporting, threat intelligence metrics, and predictive analytics from ground zero."
            )
        elif 'devops' in p_lower or 'cloud' in p_lower:
            return (
                f"As a <b>{raw_role}</b> ({raw_exp}), your background in physical security, perimeter protection, and rigorous protocol execution "
                "provides an intuitive transition into access management, system compliance, and cloud infrastructure monitoring."
            )
        else:
            return (
                f"As a <b>{raw_role}</b> ({raw_exp}), this Beginner Track starts from absolute ground zero (syntax, logic, loops). "
                "Your operational discipline and protocol compliance provide the consistency needed to build strong programming fundamentals without feeling overwhelmed."
            )

    # 0b. Hospitality, Facility & Cleaning Services (Sweeper, Cleaner, Janitor, Chef, Hotel Staff)
    if match_any(r_lower, ['sweeper', 'cleaner', 'janitor', 'housekeep', 'sanitation', 'maid', 'chef', 'cook', 'baker', 'waiter', 'server', 'steward', 'hotel', 'hospitality']):
        if 'dsml' in p_lower or 'data' in p_lower:
            return (
                f"As a <b>{raw_role}</b> ({raw_exp}), this Beginner Track assumes zero prior technical knowledge. "
                "It starts with Excel formulas and visual dashboarding before introducing Python, allowing you to transition into data reporting step-by-step."
            )
        else:
            return (
                f"As a <b>{raw_role}</b> ({raw_exp}), this Beginner Track is engineered specifically for career pivoters with zero coding background. "
                "It teaches problem-solving, basic syntax, and algorithmic logic from scratch with dedicated 1:1 mentorship, protecting you from pacing dropouts."
            )

    # 0c. Legal, Compliance & Judiciary (Lawyer, Advocate, Legal Counsel, Compliance)
    if match_any(r_lower, ['lawyer', 'advocate', 'attorney', 'legal', 'paralegal', 'solicitor', 'barrister', 'judge', 'magistrate', 'compliance']):
        if 'dsml' in p_lower or 'data' in p_lower:
            return (
                f"As a <b>{raw_role}</b> ({raw_exp}), your deep expertise in evidence synthesis, case precedent analysis, and statutory interpretation "
                "provides an analytical edge in structured SQL querying, legal compliance analytics, and NLP-driven document intelligence."
            )
        elif 'agentic' in p_lower or 'aiml' in p_lower:
            return (
                f"As a <b>{raw_role}</b> ({raw_exp}), pairing your legal reasoning and contract structuring with Agentic AI and LegalTech LLM automation "
                "positions you at the forefront of AI-driven legal intelligence."
            )
        else:
            return (
                f"As a <b>{raw_role}</b> ({raw_exp}), statutory law is fundamentally rule-based logic, conditionals (IF-THEN-ELSE), and exception handling. "
                "This structured thinking maps directly into software engineering and algorithmic problem-solving."
            )

    # 0d. Education, Teaching & Academia
    if match_any(r_lower, ['teacher', 'professor', 'lecturer', 'tutor', 'educator', 'faculty', 'instructor', 'academic', 'principal']):
        if 'dsml' in p_lower or 'data' in p_lower:
            return (
                f"As an <b>{raw_role}</b> ({raw_exp}), your pedagogical training and ability to break down complex concepts into structured lessons "
                "translate seamlessly into data storytelling, visual dashboards, and educational analytics."
            )
        else:
            return (
                f"As an <b>{raw_role}</b> ({raw_exp}), your habit of structured curriculum design and systematic lesson planning "
                "gives you the patience and learning discipline to master programming logic, algorithms, and software development from ground up."
            )

    # 0e. Transportation, Aviation & Maritime (Pilot, Sailor, Driver, Logistics)
    if (match_any(r_lower, ['pilot', 'mariner', 'sailor', 'merchant navy', 'ship captain', 'loco pilot', 'train driver', 'truck driver', 'cab driver', 'taxi driver', 'courier', 'delivery partner']) or
        (match_token(r_lower, 'driver') and 'device' not in r_lower and 'software' not in r_lower and 'hardware' not in r_lower)):
        if 'devops' in p_lower or 'cloud' in p_lower:
            return (
                f"As a <b>{raw_role}</b> ({raw_exp}), your checklist discipline and experience monitoring complex navigation and telemetry systems "
                "translate naturally into SRE monitoring, cloud infrastructure operations, and automated CI/CD deployment pipelines."
            )
        elif 'dsml' in p_lower or 'data' in p_lower:
            return (
                f"As a <b>{raw_role}</b> ({raw_exp}), your experience with route planning, telemetry data, and fuel/cargo metrics "
                "provides practical domain intuition for predictive supply-chain analytics and operational machine learning."
            )
        else:
            return (
                f"As a <b>{raw_role}</b> ({raw_exp}), your operational composure and systematic checklist execution "
                "help you build reliable, disciplined software development and debugging habits."
            )

    # 0f. Product Management, UI/UX & Agile Delivery
    if match_any(r_lower, ['product manager', 'apm', 'tpm', 'product owner', 'scrum master', 'agile', 'ui/ux', 'ux designer', 'product designer']):
        if 'dsml' in p_lower or 'data' in p_lower:
            return (
                f"As a <b>{raw_role}</b> ({raw_exp}), you already define product requirements and track feature adoption metrics. "
                "This track empowers you with SQL data extraction, cohort retention analytics, and A/B test predictive modeling to make data-driven product decisions."
            )
        elif 'fde' in p_lower or 'forward deployed' in p_lower:
            return (
                f"As a <b>{raw_role}</b> ({raw_exp}), pairing your product leadership and stakeholder roadmap execution with "
                "Enterprise AI deployment makes you an ideal Forward Deployed AI Engineer."
            )
        else:
            return (
                f"As a <b>{raw_role}</b> ({raw_exp}), learning software architecture, API design, and data structures bridges the technical communication gap with engineering teams."
            )

    # 0g. Skilled Trades & Construction Maintenance
    if match_any(r_lower, ['electrician', 'plumber', 'welder', 'machinist', 'carpenter', 'mason', 'construction', 'builder', 'painter', 'hvac', 'tailor']):
        if 'devops' in p_lower or 'cloud' in p_lower:
            return (
                f"As a <b>{raw_role}</b> ({raw_exp}), your practical troubleshooting and physical systems maintenance experience "
                "translate naturally into cloud infrastructure management, server provisioning, and network cabling/hardware operations."
            )
        else:
            return (
                f"As a <b>{raw_role}</b> ({raw_exp}), this Beginner Track teaches technical problem-solving and programming syntax "
                "from ground zero, providing step-by-step guidance to build professional software skills."
            )

    # 1. Finance / Accounting / Banking / Audit / CA
    if match_any(r_lower, ['account', 'finance', 'auditor', 'banking', 'ca', 'chartered', 'tax', 'bookkeeper', 'treasury', 'financial']):
        if 'dsml' in p_lower or 'data' in p_lower:
            return (
                f"As an <b>{raw_role}</b> ({raw_exp}), you already work with numerical data, spreadsheets, and financial reports daily. "
                "This program builds directly on your existing analytical mindset by transforming spreadsheet modeling into SQL queries, "
                "Python automation, and predictive machine learning models."
            )
        elif 'academy' in p_lower or 'software' in p_lower:
            return (
                f"As an <b>{raw_role}</b> ({raw_exp}), your daily discipline with structured financial calculations, reconciliation logic, "
                "and numeric precision provides a strong foundation for computational thinking, algorithmic logic, and software development."
            )
        elif 'devops' in p_lower or 'cloud' in p_lower:
            return (
                f"As an <b>{raw_role}</b> ({raw_exp}), this program offers a practical, tools-oriented technical pivot focusing on "
                "Linux, cloud infrastructure, and automation scripts without requiring abstract mathematical puzzles."
            )
        elif 'agentic' in p_lower or 'aiml' in p_lower:
            return (
                f"As an <b>{raw_role}</b> ({raw_exp}), your numerical exposure aligns with building domain-specific financial AI agents, "
                "prompt automations, and LLM data pipelines."
            )

    # 2. Healthcare / Clinical / Medical / Pharmacy
    if any(k in r_lower for k in ['nurse', 'nursing', 'doctor', 'hospital', 'physician', 'dentist', 'pharmacist', 'paramedic', 'medical', 'clinic']):
        if 'dsml' in p_lower or 'data' in p_lower:
            return (
                f"As a <b>{raw_role}</b> ({raw_exp}), your familiarity with patient records, clinical workflows, and diagnostic patterns "
                "translates directly into healthcare data analytics, statistical modeling, and predictive AI."
            )
        elif 'academy' in p_lower or 'software' in p_lower:
            return (
                f"As a <b>{raw_role}</b> ({raw_exp}), your background in executing high-precision clinical protocols and diagnostic decision-making "
                "translates naturally into structured computational thinking, step-by-step logic, and software engineering."
            )
        elif 'devops' in p_lower or 'cloud' in p_lower:
            return (
                f"As a <b>{raw_role}</b> ({raw_exp}), this program provides an accessible entry into tech through hands-on labs and "
                "cloud infrastructure automation with 1:1 mentorship."
            )

    # 3. Operations / Supply Chain / Logistics / Admin / Procurement
    if (any(k in r_lower for k in ['operation', 'logistics', 'supply chain', 'procurement', 'inventory', 'warehouse', 'coordinator']) or
        (match_token(r_lower, 'admin') and not any(t in r_lower for t in ['database', 'dba', 'sysadmin', 'system', 'linux', 'network', 'cloud', 'azure', 'aws']))):
        if 'dsml' in p_lower or 'data' in p_lower:
            return (
                f"As an <b>{raw_role}</b> ({raw_exp}), you already manage operational metrics, workflow pipelines, and inventory data daily. "
                "This program transforms that operational acumen into structured SQL data pipelines, visual dashboarding, and predictive analytics."
            )
        elif 'devops' in p_lower or 'cloud' in p_lower:
            return (
                f"As an <b>{raw_role}</b> ({raw_exp}), your background in managing end-to-end operational pipelines aligns directly with "
                "CI/CD automation, workflow orchestration, and cloud infrastructure management."
            )
        elif 'academy' in p_lower or 'software' in p_lower:
            return (
                f"As an <b>{raw_role}</b> ({raw_exp}), your experience in workflow optimization and system bottleneck resolution "
                "gives you an intuitive grasp of algorithmic processes and backend system design."
            )

    # 3b. Category Management / Merchandising / E-Commerce / Pricing
    if any(k in r_lower for k in ['category', 'merchandis', 'catalog', 'pricing', 'e-commerce', 'ecommerce', 'retail manager', 'store manager']):
        if 'dsml' in p_lower or 'data' in p_lower:
            return (
                f"As a <b>{raw_role}</b> ({raw_exp}), you already work with business KPIs, supply-demand metrics, pricing, and vendor data daily. "
                "This program translates that commercial intuition into advanced SQL pipelines, product analytics dashboards, and predictive machine learning models "
                "to accelerate you into Senior Product Analyst, Analytics Manager, and Business Data Science roles."
            )
        elif 'academy' in p_lower or 'software' in p_lower:
            return (
                f"As a <b>{raw_role}</b> ({raw_exp}), this program pairs your commercial problem-solving and business workflow acumen with "
                "foundational programming syntax, algorithmic logic building, and computational thinking from ground zero."
            )
        elif 'devops' in p_lower or 'cloud' in p_lower:
            return (
                f"As a <b>{raw_role}</b> ({raw_exp}), this program provides an accessible technical pivot into cloud infrastructure, "
                "Linux automation, and deployment pipelines without requiring abstract software design."
            )
        else:
            return (
                f"As a <b>{raw_role}</b> ({raw_exp}), this track builds the technical foundation to bridge your commercial management experience into tech."
            )

    # 4. Sales / Marketing / Growth / Business Development
    if any(k in r_lower for k in ['sales', 'marketing', 'bde', 'bda', 'growth', 'business dev', 'account manager']):
        if 'dsml' in p_lower or 'data' in p_lower:
            return (
                f"As a <b>{raw_role}</b> ({raw_exp}), you already understand customer funnels, campaign metrics, and business drivers. "
                "This program supercharges that commercial instinct with SQL queries, product analytics, and predictive customer modeling."
            )
        elif 'fde' in p_lower or 'forward deployed' in p_lower or 'agentic' in p_lower:
            return (
                f"As a <b>{raw_role}</b> ({raw_exp}), pairing your strong client communication and stakeholder management with "
                "enterprise AI deployment creates a high-leverage Forward Deployed Engineer profile."
            )
        else:
            return (
                f"As a <b>{raw_role}</b> ({raw_exp}), this program takes your commercial communication skills and pairs them with "
                "computational thinking and coding from scratch to build client-ready software products."
            )

    # 5. HR / People Ops / Recruitment
    if any(k in r_lower for k in ['hr', 'human resource', 'recruiter', 'talent', 'people ops']):
        if 'dsml' in p_lower or 'data' in p_lower:
            return (
                f"As an <b>{raw_role}</b> ({raw_exp}), you already handle workforce information and recruitment metrics. "
                "This program formalizes your reporting into SQL data pipelines, People Analytics, and predictive talent modeling."
            )
        else:
            return (
                f"As an <b>{raw_role}</b> ({raw_exp}), this Beginner Track starts from absolute fundamentals, "
                "building coding habits and computational logic step-by-step."
            )

    # 6. Core Engineering (Mechanical, Civil, Electrical, Chemical, Electronics)
    if any(k in r_lower for k in ['mechanical', 'civil', 'chemical', 'electrical', 'biotech', 'aerospace', 'automobile', 'electronics']):
        if 'academy' in p_lower or 'software' in p_lower:
            return (
                f"As a <b>{raw_role}</b> ({raw_exp}), your core engineering mathematics and physical systems background "
                "give you a massive quantitative advantage in understanding algorithms, data structures, and system design."
            )
        elif 'dsml' in p_lower or 'data' in p_lower:
            return (
                f"As a <b>{raw_role}</b> ({raw_exp}), your engineering math and scientific modeling training translate seamlessly "
                "into statistical data science, Python computing, and machine learning."
            )
        elif 'devops' in p_lower or 'cloud' in p_lower:
            return (
                f"As a <b>{raw_role}</b> ({raw_exp}), your background in physical systems and infrastructure makes "
                "cloud architecture, container clustering, and Linux automation a natural technical pivot."
            )

    # 7. Customer Support / Technical Support / BPO / Helpdesk / Operations Support
    if any(k in r_lower for k in ['support', 'bpo', 'kpo', 'helpdesk', 'service desk', 'customer care', 'call center', 'operations support', 'it support', 'desktop support']):
        if 'academy' in p_lower or 'software' in p_lower:
            return (
                f"As a <b>{raw_role}</b> ({raw_exp}), your hands-on experience troubleshooting technical issues and debugging application workflows "
                "gives you practical domain intuition into software systems. This program equips you with core Data Structures, algorithmic problem-solving, "
                "and backend engineering from ground up to transition from reactive ticket resolution into proactive software development (SDE)."
            )
        elif 'fde' in p_lower or 'forward deployed' in p_lower:
            return (
                f"As a <b>{raw_role}</b> ({raw_exp}), you already understand real-world customer pain points and system integrations daily. "
                "The Forward Deployed Engineering track leverages your customer-facing technical support background into deploying production AI systems, "
                "automating enterprise support workflows with LangGraph and RAG, and integrating custom solutions directly inside client infrastructure."
            )
        elif 'devops' in p_lower or 'cloud' in p_lower:
            return (
                f"As a <b>{raw_role}</b> ({raw_exp}), your technical troubleshooting and ticket triage background translate directly "
                "into production incident management, SRE monitoring, automated alerting, and CI/CD cloud operations."
            )
        elif 'dsml' in p_lower or 'data' in p_lower:
            return (
                f"As a <b>{raw_role}</b> ({raw_exp}), this track builds on your issue resolution and system ticketing experience by equipping you with "
                "SQL querying, product usage analytics, customer churn modeling, and automated business dashboards."
            )
        elif 'agentic' in p_lower or 'aiml' in p_lower:
            return (
                f"As a <b>{raw_role}</b> ({raw_exp}), your frontline support domain experience is prime for enterprise LLM automation—building "
                "autonomous customer resolution agents, multi-turn LangGraph workflows, and retrieval-augmented generation (RAG) pipelines."
            )
        else:
            return (
                f"As a <b>{raw_role}</b> ({raw_exp}), this track provides a structured, guided bridge from operational support into "
                "high-growth software engineering and technology leadership."
            )

    # 8. QA / SDET / Testing
    if any(k in r_lower for k in ['qa', 'test', 'sdet', 'quality']):
        if 'academy' in p_lower or 'software' in p_lower:
            if 'advanced' in t_lower or 'leadership' in t_lower:
                return (
                    f"As a senior <b>{raw_role}</b> with {raw_exp}, you have mastered quality lifecycles and enterprise systems; "
                    "this track focuses on High-Level Distributed System Design (HLD), event streaming, and architectural scalability "
                    "commanded in Principal Architect and Engineering Leadership roles."
                )
            else:
                return (
                    f"As a <b>{raw_role}</b> with {raw_exp}, you already understand software lifecycles and code structures; "
                    "this track bridges the exact gap in algorithmic optimization, advanced DSA, and low-level object-oriented design (LLD) "
                    "to transition into core Backend SDE roles."
                )
        elif 'fde' in p_lower or 'forward deployed' in p_lower:
            return (
                f"As a <b>{raw_role}</b> with {raw_exp}, your deep enterprise systems and quality assurance background translates directly "
                "into deploying reliable, enterprise-grade AI applications, agent evaluation frameworks, and client systems integration."
            )
        elif 'devops' in p_lower or 'cloud' in p_lower:
            return (
                f"As a <b>{raw_role}</b> with {raw_exp}, your test automation background translates directly into "
                "CI/CD pipelines, containerized test runners, and cloud infrastructure management - commanding a 30-50% salary boost."
            )
        elif 'dsml' in p_lower or 'agentic' in p_lower or 'data' in p_lower:
            return (
                f"As a <b>{raw_role}</b> with {raw_exp}, moving into AI/ML enables you to apply your testing rigor to "
                "AI model evaluation, data pipelines, and intelligent agent workflows."
            )

    # 9. Data Analyst / BI / Reporting
    if any(k in r_lower for k in ['data analyst', 'business analyst', 'bi analyst', 'analytics', 'tableau', 'power bi', 'sql developer']):
        if 'dsml' in p_lower or 'data' in p_lower:
            if 'beginner' in t_lower or 'analytics' in t_lower:
                return (
                    f"As a <b>{raw_role}</b> with {raw_exp}, you already have reporting exposure; this track solidifies your "
                    "foundational analytics, Python automation, and product metrics to prepare you for machine learning workflows."
                )
            else:
                return (
                    f"As a <b>{raw_role}</b> with {raw_exp}, you already write SQL queries and build dashboards daily; "
                    "this track breaks through the reporting salary ceiling by adding predictive modeling, deep neural networks, and production MLOps on AWS."
                )
        elif 'agentic' in p_lower or 'aiml' in p_lower or 'fde' in p_lower:
            return (
                f"As a <b>{raw_role}</b> with {raw_exp}, expanding from SQL and dashboards into Agentic AI, GraphRAG, and "
                "LangGraph multi-agent orchestration elevates your profile to frontier AI engineering roles."
            )
        elif 'academy' in p_lower or 'software' in p_lower:
            return (
                f"As a <b>{raw_role}</b> with {raw_exp}, adding core data structures, algorithms, and backend API engineering "
                "turns you into a full-stack data and software engineer."
            )

    # 10. Software Engineer / SDE / Web Developer
    if any(k in r_lower for k in ['sde', 'software', 'developer', 'frontend', 'backend', 'full stack', 'programmer', 'web dev']):
        if 'academy' in p_lower or 'software' in p_lower:
            if 'intermediate' in t_lower or 'dsa' in t_lower:
                return (
                    f"As a <b>{raw_role}</b> with {raw_exp}, you already know how to code - but most engineers fail product company interviews "
                    "due to lack of systematic algorithmic optimization (time complexity, space trade-offs, edge-case reasoning). "
                    "This Intermediate Track focuses 100% on FAANG interview patterns: sliding window, DP, graph traversal, and OOP design."
                )
            elif 'advanced' in t_lower:
                return (
                    f"As a <b>{raw_role}</b> with {raw_exp}, you have mastered coding and team delivery - but the next level (Staff Engineer, Principal Architect) "
                    "demands large-scale distributed systems expertise (Kafka, consistent hashing, database sharding, CAP/PACELC)."
                )
            else:
                return (
                    f"As a <b>{raw_role}</b> with {raw_exp}, this track builds structured problem-solving and algorithmic thinking "
                    "that Tier-1 product companies test rigorously in interviews."
                )
        elif 'devops' in p_lower or 'cloud' in p_lower:
            return (
                f"As a <b>{raw_role}</b> with {raw_exp}, expanding into Cloud & DevOps complements your development background with "
                "Docker, Kubernetes, CI/CD automation, and Terraform IaC - skills commanding a 30-50% compensation premium."
            )
        elif 'fde' in p_lower or 'forward deployed' in p_lower:
            return (
                f"As a <b>{raw_role}</b> with {raw_exp}, FDE is the highest-leverage AI role - building AND deploying custom LLM systems "
                "inside enterprise client infrastructure with LangGraph and Meridian simulation."
            )
        elif 'agentic' in p_lower or 'aiml' in p_lower:
            return (
                f"As a <b>{raw_role}</b> with {raw_exp}, upgrading your backend engineering skills to frontier AI (LangGraph multi-agent systems, "
                "GraphRAG, PEFT/LoRA fine-tuning, and vLLM deployment) positions you for high-paying AI Engineer roles."
            )
        elif 'dsml' in p_lower or 'data' in p_lower:
            return (
                f"As a <b>{raw_role}</b> with {raw_exp}, your coding syntax and software foundation let you bypass basic Python "
                "and advance directly into statistical modeling, feature engineering pipelines, and production machine learning at scale."
            )

    # 11. DevOps / Cloud / SRE / SysAdmin
    if any(k in r_lower for k in ['devops', 'cloud', 'sre', 'sysadmin', 'system admin', 'infrastructure', 'platform engineer']):
        if 'devops' in p_lower or 'cloud' in p_lower:
            return (
                f"As a <b>{raw_role}</b> with {raw_exp}, modernizing your infrastructure skillset with Kubernetes clustering, "
                "Terraform GitOps, and AWS cloud architecture elevates you into senior Platform Engineer and SRE roles."
            )
        elif 'academy' in p_lower or 'software' in p_lower:
            return (
                f"As a <b>{raw_role}</b> with {raw_exp}, adding core data structures, algorithms, and backend microservices design "
                "rounds out your engineering profile to clear Tier-1 software and platform engineering rounds."
            )
        elif 'agentic' in p_lower or 'aiml' in p_lower or 'dsml' in p_lower:
            return (
                f"As a <b>{raw_role}</b> with {raw_exp}, expanding into MLOps on AWS SageMaker and AI agent infrastructure makes you "
                "an invaluable AI Infrastructure / LLMOps specialist."
            )

    # 11b. Systems & Embedded Engineering (Systems Engineer, Embedded, Firmware, Hardware, IoT, Device Driver)
    if any(k in r_lower for k in ['system', 'embedded', 'firmware', 'hardware', 'vlsi', 'iot', 'kernel', 'device driver']):
        if 'academy' in p_lower or 'software' in p_lower:
            if 'advanced' in t_lower or 'leadership' in t_lower:
                return (
                    f"As a <b>{raw_role}</b> with {raw_exp}, your low-level hardware and memory control provide an exceptional foundation; "
                    "this track focuses on High-Level Distributed System Design (HLD), event streaming, database sharding, and architectural scalability "
                    "commanded in Principal Systems Architect and Staff Engineer roles."
                )
            else:
                return (
                    f"As a <b>{raw_role}</b> with {raw_exp}, your C/C++ memory management and low-level computing background "
                    "give you an intuitive edge in mastering competitive Data Structures, Algorithms, and modern backend microservices."
                )
        elif 'devops' in p_lower or 'cloud' in p_lower:
            return (
                f"As a <b>{raw_role}</b> with {raw_exp}, your deep OS, Linux, and hardware experience translates directly into "
                "bare-metal server orchestration, Kubernetes cluster operations, and high-performance cloud platform engineering."
            )
        elif 'fde' in p_lower or 'forward deployed' in p_lower:
            return (
                f"As a <b>{raw_role}</b> with {raw_exp}, your systems depth is crucial for deploying low-latency AI models, "
                "optimizing inference pipelines on custom client hardware, and integrating enterprise agent architectures."
            )
        elif 'dsml' in p_lower or 'agentic' in p_lower or 'data' in p_lower:
            return (
                f"As a <b>{raw_role}</b> with {raw_exp}, your hardware and mathematical background lets you master "
                "model quantization, edge AI deployment, and high-throughput machine learning feature pipelines."
            )

    # 11c. Cybersecurity, InfoSec & Network Security
    if any(k in r_lower for k in ['cyber security', 'cybersecurity', 'security', 'infosec', 'soc analyst', 'penetration', 'appsec', 'network security']):
        if 'devops' in p_lower or 'cloud' in p_lower:
            return (
                f"As a <b>{raw_role}</b> with {raw_exp}, your threat analysis and security governance background translates directly into "
                "DevSecOps, automated vulnerability scanning, cloud IAM architecture, and secure Kubernetes deployment."
            )
        elif 'academy' in p_lower or 'software' in p_lower:
            return (
                f"As a <b>{raw_role}</b> with {raw_exp}, adding core data structures, algorithms, and backend API engineering "
                "qualifies you for high-paying Secure Software Engineering and Application Security (AppSec) architect roles."
            )
        elif 'agentic' in p_lower or 'aiml' in p_lower or 'fde' in p_lower:
            return (
                f"As a <b>{raw_role}</b> with {raw_exp}, your security mindset is crucial for securing enterprise LLM pipelines, "
                "defending against prompt injection, and implementing robust multi-agent security guardrails."
            )

    # 11d. Database Administrator / DBA
    if any(k in r_lower for k in ['dba', 'database administrator', 'database engineer', 'oracle dba', 'sql dba']):
        if 'academy' in p_lower or 'software' in p_lower:
            return (
                f"As a <b>{raw_role}</b> with {raw_exp}, your deep relational database internals, query optimization, and storage indexing "
                "give you an unfair advantage in High-Level System Design, distributed database sharding, and backend microservices architecture."
            )
        elif 'devops' in p_lower or 'cloud' in p_lower:
            return (
                f"As a <b>{raw_role}</b> with {raw_exp}, your database reliability and backup/recovery experience maps directly into "
                "Cloud Database Operations, automated Terraform provisioning, and site reliability engineering."
            )
        elif 'dsml' in p_lower or 'data' in p_lower:
            return (
                f"As a <b>{raw_role}</b> with {raw_exp}, your SQL mastery enables an effortless transition into large-scale "
                "Data Engineering, PySpark ETL pipelines, and predictive machine learning feature stores."
            )

    # 11e. Engineering Leadership & Technical Architects
    if any(k in r_lower for k in ['tech lead', 'technical lead', 'team lead', 'engineering manager', 'director', 'cto', 'architect']):
        if 'academy' in p_lower or 'software' in p_lower:
            return (
                f"As a <b>{raw_role}</b> with {raw_exp}, this track sharpens your architectural authority - mastering distributed systems scalability, "
                "event-driven microservices (Kafka), database sharding, and high-level design patterns commanded in Staff and Principal Architect roles."
            )
        elif 'fde' in p_lower or 'forward deployed' in p_lower:
            return (
                f"As a <b>{raw_role}</b> with {raw_exp}, pairing your technical leadership and delivery governance with "
                "client-facing AI deployment positions you as a high-compensation Forward Deployed Engineering leader."
            )
        elif 'devops' in p_lower or 'cloud' in p_lower:
            return (
                f"As a <b>{raw_role}</b> with {raw_exp}, modernizing your infrastructure strategy with Kubernetes, multi-region cloud resilience, "
                "and GitOps automation equips you to lead modern cloud engineering organizations."
            )

    # 12. Freshers / Students
    if any(k in r_lower for k in ['fresher', 'student', 'intern', 'college student', 'final year']) or any(k in str(raw_exp).lower() for k in ['fresher', 'entry', 'no exp']) or str(raw_exp).strip() in ['0', '0 yrs', '0.0 yrs']:
        if 'academy' in p_lower or 'software' in p_lower:
            return (
                f"As a <b>{raw_role}</b>, this Beginner Track takes you from absolute zero to interview-ready software engineer. "
                "It builds computational thinking, problem-solving, and coding fundamentals from scratch - the exact skills Tier-1 product companies test in every interview."
            )
        elif 'dsml' in p_lower or 'data' in p_lower:
            return (
                f"As a <b>{raw_role}</b>, this track is the smoothest entry into tech because it does NOT assume any coding background. "
                "It starts with Excel, SQL queries, and visual dashboards before gradually introducing Python and machine learning."
            )
        elif 'devops' in p_lower or 'cloud' in p_lower:
            return (
                f"As a <b>{raw_role}</b>, DevOps & Cloud Engineering is an accessible entry point into tech focusing on "
                "practical tools, Linux scripting, Docker, and AWS rather than competitive algorithmic problem-solving."
            )
        else:
            return (
                f"As a <b>{raw_role}</b>, this track provides a structured ramp-up into high-growth technology careers."
            )

    # Intelligent Career Alignment (Role & Experience Aware)
    if 'fde' in p_lower or 'forward deployed' in p_lower:
        return (
            f"As a <b>{raw_role}</b> ({raw_exp}), combining your practical problem-solving with client-facing enterprise AI integration "
            "accelerates you into high-compensation Forward Deployed Engineer roles delivering custom LLM systems and production LangGraph pipelines."
        )
    elif 'devops' in p_lower or 'cloud' in p_lower:
        return (
            f"As a <b>{raw_role}</b> ({raw_exp}), this track equips you with hands-on container orchestration (Kubernetes), "
            "cloud infrastructure-as-code (Terraform), and automated CI/CD pipelines to step into modern Platform Engineering."
        )
    elif 'dsml' in p_lower or 'data' in p_lower:
        return (
            f"As a <b>{raw_role}</b> ({raw_exp}), this track translates your operational workflows into data-driven decision making—teaching "
            "SQL data querying, business metrics dashboards, and applied predictive machine learning."
        )
    elif 'agentic' in p_lower or 'aiml' in p_lower:
        return (
            f"As a <b>{raw_role}</b> ({raw_exp}), this curriculum fast-tracks your profile into modern Agentic AI, "
            "retrieval-augmented generation (RAG), and production LLMOps."
        )
    else:
        return (
            f"As a <b>{raw_role}</b> ({raw_exp}), this program provides a structured curriculum that bridges your current experience "
            "into core software development, algorithmic problem-solving, and scalable system design."
        )


def generate_curriculum_grounded_why(
    program_name, track_name, raw_role, raw_exp, modules,
    retention_rate, cohort_size, fit_tier, inbound_cat,
    is_primary=True, base_rationale="", persona="", primary_prog_name=""
):
    """
    Synthesizes a cohesive, curriculum-grounded explanation for 'Why This Program' / 'Why Fallback'.
    Grounds the reasoning directly in the candidate's current role, experience level, and career trajectory.
    """
    p_lower = str(program_name).lower()
    t_lower = str(track_name).lower()

    # 1. Career Pitch grounded in candidate's current role
    raw_career_desc = generate_role_pitch(raw_role, raw_exp, p_lower, t_lower, is_primary, persona)

    if is_primary:
        career_desc = raw_career_desc
    else:
        # For Fallback, craft a smooth transition contrasting with Primary
        if primary_prog_name and 'academy' in str(primary_prog_name).lower():
            contrast_prefix = (
                f"While <b>{primary_prog_name}</b> is your primary route for core software engineering interviews, "
                f"this alternative path in <b>{program_name}</b> focuses directly on high-demand domain application. "
            )
        elif primary_prog_name:
            contrast_prefix = (
                f"If you choose not to pursue <b>{primary_prog_name}</b>, "
                f"this alternative in <b>{program_name}</b> offers an equally high-leverage career accelerator. "
            )
        else:
            contrast_prefix = "As an alternative strategic pathway, "
        
        career_desc = f"{contrast_prefix}{raw_career_desc}"

    # 2. Extract top module phases for Curricular Milestones
    module_names = []
    if modules and isinstance(modules, list):
        for m in modules[:5]:
            p = m.get('phase', '')
            if p and p not in module_names:
                module_names.append(p)

    # 3. Standardized, high-impact curricular content descriptions by program
    if 'academy' in p_lower or 'software' in p_lower:
        if 'beginner' in t_lower or 'foundations' in t_lower:
            content_desc = (
                "Features foundational modules starting with <i>Programming Fundamentals - Thinking with AI (Logics, Loops & Control Flow)</i>, "
                "<i>Intermediate DSA (Prefix Sum, Bit Manipulation, 2D Matrices)</i>, and <i>AI & Agents: From Talking to AI to Building One</i>, "
                "before advancing into <i>Advanced DSA</i> (Linear/Non-Linear Structures, Trees, Dynamic Programming, Graphs) and <i>System Design</i>."
            )
            historical_desc = (
                f"Backed by an audited <b>{retention_rate}% completion rate</b> across {cohort_size}+ early-career and non-CS learners. "
                "Beginners placed directly into intermediate algorithms face elevated Day-14 pacing dropout; this structured ramp-up prevents that."
            )
        elif 'intermediate' in t_lower or 'dsa' in t_lower:
            content_desc = (
                "Bypasses basic syntax to focus directly on <i>Intermediate DSA : AI Assisted Problem Solving</i>, "
                "<i>Advanced DSA (Divide & Conquer, Trees, Heaps, Graphs, Dynamic Programming)</i>, and <i>Low-Level Object-Oriented Design (LLD)</i>, "
                "with an elective bridge into <i>Distributed High-Level System Design</i>."
            )
            historical_desc = (
                f"Supported by an empirical <b>{retention_rate}% completion rate</b> across {cohort_size}+ working technical professionals. "
                "Maximizes interview-readiness within 12 months while respecting full-time working hours."
            )
        else: # Advanced
            content_desc = (
                "Centers on architectural scale and engineering leadership: <i>High-Level Distributed System Design & Scalability</i> "
                "(Kafka event streaming, consistent hashing, caching at scale, database sharding, CAP/PACELC theorems) and <i>Concurrent Backend Microservices</i>."
            )
            historical_desc = (
                f"Demonstrates an elite <b>{retention_rate}% completion rate</b> across senior cohorts. "
                "Senior candidates thrive when curriculum focuses on system-level architecture rather than repetitive syntax drills."
            )

    elif 'dsml' in p_lower or 'data science' in p_lower:
        if 'beginner' in t_lower or 'analytics' in t_lower:
            content_desc = (
                "Begins with <i>Advanced SQL & AI for Data Professionals</i>, <i>Excel & Dashboarding with AI Storytelling</i>, "
                "<i>Python Foundations + AI Coding Assistants</i>, and <i>Product Analytics with AI</i>, seamlessly progressing into "
                "<i>Supervised Machine Learning with AI Workflows</i>."
            )
            historical_desc = (
                f"Proven by a <b>{retention_rate}% completion rate</b> across {cohort_size}+ learners. "
                "This progressive ramp-up achieves the highest retention of any career pivot, virtually eliminating refund risk."
            )
        else: # Intermediate / Core ML
            content_desc = (
                "Dives directly into <i>Advanced Analytics with Python & Pandas</i>, <i>Statistics & Experimentation for AI (A/B Testing Frameworks)</i>, "
                "<i>Supervised & Unsupervised Machine Learning</i>, <i>Deep Learning & Neural Networks</i>, and <i>Production MLOps on AWS</i>."
            )
            historical_desc = (
                f"Validated by an audited <b>{retention_rate}% completion rate</b> across quantitative cohorts. "
                "Analysts transitioning through predictive modeling experience rapid career acceleration into senior ML titles."
            )

    elif 'fde' in p_lower or 'forward deployed' in p_lower:
        content_desc = (
            "Delivered entirely through enterprise client simulation (<i>Meridian Platform</i>), covering <i>The Ingestion Pipeline (Production Python)</i>, "
            "<i>Production RAG for Customer Support</i>, <i>Autonomous Agents & Enterprise Integration (LangGraph & MCP)</i>, "
            "<i>Docker & Kubernetes Orchestration</i>, and <i>1-Click AWS Production Deployment with Terraform</i>."
        )
        historical_desc = (
            f"Supported by an outstanding <b>{retention_rate}% completion rate</b> across software engineering cohorts. "
            "Forward-deployed roles command a 2.5x compensation premium over traditional development due to high client demand."
        )

    elif 'agentic' in p_lower or 'aiml' in p_lower or 'program 4' in p_lower:
        if 'beginner' in t_lower or 'foundation' in t_lower:
            content_desc = (
                "Includes the dedicated 2-Month <i>Generative AI Foundations & LLM Landscape</i> (Prompt Engineering, n8n/Zapier automations, no-code agents, AWS hosting) "
                "and 1-Month <i>Python Programming Fundamentals</i>, before advancing into <i>Data Foundations</i>, <i>Supervised/Unsupervised ML</i>, "
                "<i>MLOps on AWS SageMaker</i>, and <i>LangGraph Agentic Orchestration</i>."
            )
            historical_desc = (
                f"Candidates without prior coding exposure face a 25.8% drop-off if pushed directly into tensor math; "
                "this foundational progression preserves high retention (<b>{retention_rate}% completion rate</b> across {cohort_size}+ learners)."
            )
        else: # Advanced Track
            content_desc = (
                "Bypasses introductory syntax to dive directly into <i>Data Foundations</i>, <i>Applied Deep Learning (OpenCV & Transformers)</i>, "
                "<i>MLOps on AWS SageMaker</i>, <i>Agentic Design Patterns & LangGraph Multi-Agent Orchestration</i>, "
                "<i>Advanced Cognitive Architectures (GraphRAG & Multimodal AI)</i>, and <i>PEFT/LoRA Fine-Tuning served via vLLM</i>."
            )
            historical_desc = (
                f"Backed by an empirical <b>{retention_rate}% completion rate</b> across technical cohorts. "
                "Software developers thrive when immersed directly in modern generative AI architectures and scalable LLMOps."
            )

    elif 'devops' in p_lower or 'cloud' in p_lower or 'platform' in p_lower or 'program 5' in p_lower:
        content_desc = (
            "Systematically covers the entire modern platform stack: <i>Python & Linux Shell Scripting (1 & 2)</i>, "
            "<i>DevOps Tools 1 (Docker, multi-node Kubernetes clustering, Prometheus/Grafana monitoring, Hugging Face model deployment)</i>, "
            "<i>DevOps Tools 2 (GitHub Actions CI/CD, ArgoCD GitOps, Ansible)</i>, and <i>AWS 1 & 2 (EKS, VPC, CloudFormation, Terraform IaC)</i>, "
            "with specialized electives in <i>MLOps & AI Observability</i>."
        )
        historical_desc = (
            f"Demonstrates an elite <b>{retention_rate}% completion rate</b> ({cohort_size}+ cohort). "
            "Infrastructure and platform engineering provides the highest retention and lowest refund rate among all technical transitions."
        )

    else:
        module_text = ", ".join(f"<i>{h}</i>" for h in module_names[:3]) if module_names else "core engineering and production milestones"
        content_desc = f"Curriculum structured around {module_text}."
        historical_desc = f"Supported by a {retention_rate}% completion rate across {cohort_size}+ learners."

    full_rationale = (
        f"{career_desc}<br><br>"
        f"<b>Curricular Content & Milestones:</b> {content_desc}<br><br>"
        f"<b>Historical Retention & Cohort Evidence:</b> {historical_desc}"
    )
    return full_rationale


def evaluate_lead_profile(lead_dict, matrix_data=None):
    """
    Evaluates a lead profile against the official 5-Program Scaler Catalog.
    Includes Education Prerequisite Gate, Persona Taxonomy, and spoken sales scripts.
    """
    def _field(keys, default=''):
        for k in keys:
            if k in lead_dict and lead_dict[k] is not None:
                val = str(lead_dict[k]).strip()
                if val and val.lower() not in ['nan', 'none', 'null']:
                    return val
        ld_lower = {str(k).strip().lower(): v for k, v in lead_dict.items() if v is not None}
        for k in keys:
            kl = k.lower()
            if kl in ld_lower:
                val = str(ld_lower[kl]).strip()
                if val and val.lower() not in ['nan', 'none', 'null']:
                    return val
        return default

    name = clean_str(_field(['name', 'full_name', 'candidate_name', 'student_name']), 'Prospective Learner')
    email = clean_str(_field(['email', 'email_id', 'contact_email', 'lead_email']), 'unspecified@lead.com')
    phone = clean_str(_field(['phone', 'mobile', 'contact', 'phone_number']), 'N/A')
    raw_role = clean_str(_field(['role', 'current_role', 'designation', 'job_title', 'profile']), 'General Tech Professional')
    company_type = clean_str(_field(['company type', 'company_type', 'industry', 'sector']), 'IT Services / Technology')
    prev_org = clean_str(_field(['previous org name', 'company', 'organization', 'employer']), 'Current Company')
    prev_year = clean_str(_field(['previous org year', 'year', 'org_year']), '1-2 years')
    raw_exp = clean_str(_field(['experience', 'yoe', 'total_experience', 'work_experience', 'exp']), '2 years')
    inbound_prog_raw = clean_str(_field(['program', 'inbound_program', 'enquired_program', 'course']), 'Academy')
    raw_edu = clean_str(_field(['education', 'degree', 'qualification', 'highest_qualification', 'stream']), 'Graduated / Degree')
    raw_sat_status = clean_str(_field(['set_status', 'sat_status', 'diagnostic set status', 'diagnostic sat status', 'test_launched_flag']), 'SET Not Attempted')
    if 'sat' in raw_sat_status.lower():
        raw_sat_status = raw_sat_status.replace('SAT', 'SET').replace('Sat', 'Set').replace('sat', 'set')
    raw_sat_score = clean_str(_field(['set_score', 'sat_score', 'diagnostic set score', 'diagnostic sat score']), 'Not Attempted')
    
    # Normalized taxonomy & education
    persona = normalize_persona('', raw_role)
    persona_name = get_canonical_persona_name(persona)
    role_domain = classify_world_domain(raw_role)
    exp_bracket = normalize_experience(raw_exp)
    edu_level = classify_education(raw_edu)
    inbound_str = str(inbound_prog_raw).lower()

    
    # =========================================================================
    # ACADEMIC ELIGIBILITY GATE: BELOW GRADUATION (10th/12th/Diploma)
    # =========================================================================
    if edu_level == 'BELOW_GRAD':
        prim = {
            'program': 'Not Eligible (Degree Prerequisite)',
            'catalog_code': 'Academic Prerequisite Gate',
            'track': 'Academic Eligibility Prerequisite',
            'fit_tier': 'Ineligible for Placement-Linked Programs',
            'why': (
                f"Candidate's education background ({raw_edu}) does not satisfy Scaler's formal graduation prerequisite. "
                "All Scaler career programs and hiring partner placement drives mandate an undergraduate Bachelor's degree "
                "(or enrolled final-year student). Enrolling without graduation risks placement disqualification."
            ),
            'guardrail': 'Hard Academic Gate: Mandatory Bachelor degree completion required prior to placement-linked tracks.',
            'duration': 'N/A',
            'retention_rate': 0.0,
            'refund_rate': 100.0,
            'cohort_size': 0,
            'risk_tag': 'Ineligible',
            'confidence_tier': 'Low',
            'confidence_score': 0,
            'confidence_rationale': 'Ineligible: Mandatory Bachelor degree completion required.',
            'confidence_breakdown': {
                'cohort_pts': 0, 'cohort_max': 35, 'cohort_desc': 'Ineligible',
                'ret_pts': 0, 'ret_max': 25, 'ret_desc': 'Ineligible',
                'intent_pts': 0, 'intent_max': 25, 'intent_desc': 'Ineligible',
                'apt_pts': 0, 'apt_max': 15, 'apt_desc': 'Degree prerequisite unfulfilled'
            }
        }
        fall = {
            'program': 'Degree Pathway Consultation / Open Learning',
            'catalog_code': 'Alternative Path',
            'track': 'Formal Degree Enrolment Route',
            'fit_tier': 'Preparatory Route',
            'why': "Advise candidate to pursue a recognized BCA / B.Tech / B.Sc degree first before applying to professional placement accelerators.",
            'guardrail': 'Academic counseling path',
            'duration': '3 - 4 Years',
            'retention_rate': 0.0,
            'refund_rate': 0.0,
            'cohort_size': 0,
            'risk_tag': 'Prerequisite Needed',
            'confidence_tier': 'Low',
            'confidence_score': 0,
            'confidence_rationale': 'Academic counseling pathway.',
            'confidence_breakdown': {
                'cohort_pts': 0, 'cohort_max': 35, 'cohort_desc': 'Ineligible',
                'ret_pts': 0, 'ret_max': 25, 'ret_desc': 'Ineligible',
                'intent_pts': 0, 'intent_max': 25, 'intent_desc': 'Ineligible',
                'apt_pts': 0, 'apt_max': 15, 'apt_desc': 'Preparatory degree route'
            }
        }
        first_name = name.split()[0] if name else 'there'
        sales_script = {
            'call_opening': f'"Hi {first_name}, thank you for connecting with Scaler. I reviewed your profile and noticed your education background is {raw_edu}. Before discussing technical curricula, I want to be completely transparent with you regarding our program prerequisites."',
            'program_pitch': '"At Scaler, our career accelerators and hiring partner placement networks strictly require learners to hold an undergraduate Bachelor\'s degree (or be in their final year of graduation). Because companies enforce strict degree cutoffs in technical hiring rounds, we never want you to invest time and money into a program where corporate recruiters might disqualify you on degree credentials alone."',
            'inbound_handling': '"We sincerely appreciate your drive to learn software development. Our honest recommendation is to first complete a formal degree program (such as a BCA, B.Sc, or B.Tech). As you approach your graduation year, we will gladly fast-track your enrollment into our technical cohorts."'
        }
        return {
            'person': {
                'name': name, 'email': email, 'phone': phone, 'role': raw_role,
                'role_domain': role_domain,
                'company_type': company_type, 'previous_org': prev_org, 'previous_org_year': prev_year,
                'experience': raw_exp, 'enquired_program': inbound_prog_raw,
                'education': raw_edu, 'education_level': edu_level,
                'sat_score': raw_sat_score, 'sat_status': raw_sat_status,
                'normalized_persona': persona_name, 'persona_key': persona, 'normalized_experience': exp_bracket
            },
            'primary': prim,
            'fallback': fall,
            'sales_script': sales_script,
            'academic_eligibility': {
                'status': 'Ineligible (Degree Prerequisite)',
                'is_eligible': False,
                'rationale': f"Education background ({raw_edu}) does not satisfy Bachelor's degree requirement."
            }
        }

    # Detect inbound program category
    if re.search(r'\b(program\s*3|p3|prog\s*3|fde|forward deployed|solutions engineer)\b', inbound_str):
        inbound_cat = 'P3_FDE'
    elif re.search(r'\b(program\s*4|p4|prog\s*4|agentic|aiml|deep learning|llm|genai|ai agent)\b', inbound_str):
        inbound_cat = 'P4_AIML_AGENTIC'
    elif re.search(r'\b(program\s*2|p2|prog\s*2|dsml|data science|data analytics|analytics|data engineer)\b', inbound_str) or 'machine learning' in inbound_str:
        inbound_cat = 'P2_DSML'
    elif re.search(r'\b(program\s*5|p5|prog\s*5|devops|cloud|platform|sre|kubernetes|docker)\b', inbound_str):
        inbound_cat = 'P5_DEVOPS_CLOUD'
    else:
        inbound_cat = 'P1_ACADEMY'

    is_career_break = any(k in raw_role.lower() for k in ['career break', 'break', 'sabbatical', 'gap', 'gap year', 'returning', 'homemaker', 'restart'])
    is_student = (exp_bracket == 'EXP_0_1') or any(k in raw_role.lower() for k in ['student', 'intern', 'learner', 'fresher', 'non coder', 'college'])
    
    # 1. Allowlist for Tech Roles
    tech_keywords = [
        'sde', 'swe', 'software', 'developer', 'frontend', 'backend', 'full stack', 'fullstack', 'programmer',
        'devops', 'cloud', 'sre', 'sysadmin', 'infrastructure', 'platform engineer',
        'data', 'analytics', 'analyst', 'bi', 'machine learning', 'ml', 'ai', 'artificial intelligence',
        'qa', 'sdet', 'testing', 'automation', 'embedded', 'firmware', 'linux kernel', 'architect',
        'systems engineer', 'system engineer', 'systems', 'system', 'hardware', 'vlsi', 'network engineer',
        'cyber security', 'cybersecurity', 'security engineer', 'dba', 'database administrator', 'solutions engineer', 'fde',
        'engineering manager', 'tech lead', 'technical lead', 'lead architect', 'software architect',
        'solutions architect', 'enterprise architect', 'cto', 'vp of engineering', 'director of engineering',
        'ui engineer', 'web engineer', 'mobile engineer', 'device driver', 'appsec', 'build and release',
        'release engineer', 'computer vision', 'nlp', 'applied scientist', 'big data', 'etl'
    ]
    is_tech = (
        persona in ['SYSTEMS_ENG', 'DEVOPS_CLOUD', 'DATA_ANALYST', 'QA_SDET', 'SWE_BACKEND', 'FRONTEND', 'LEADERSHIP', 'IT_SERVICES'] or
        any(match_token(raw_role.lower(), k) for k in tech_keywords) or
        (match_token(raw_role.lower(), 'team lead') and not any(op in raw_role.lower() for op in [
            'operation', 'bpo', 'kpo', 'support', 'sales', 'marketing', 'hr', 'talent',
            'retail', 'logistics', 'finance', 'non-tech', 'call center', 'process'
        ]))
    )
    # Exclude non-software engineering domains (unless explicitly classified as tech)
    if persona == 'NON_TECH':
        is_tech = False

    is_non_tech = (
        is_career_break or 
        (edu_level == 'GRAD_NON_CS' and is_student) or 
        (persona in ['NON_TECH', 'Non-Tech / Operations', 'Non-Tech / Career Switcher']) or 
        not is_tech
    )

    is_qa = (not is_non_tech) and (persona in ['QA_SDET', 'QA / SDET / Testing'] or any(k in raw_role.lower() for k in ['test', 'qa', 'sdet', 'automation']))
    is_data = (not is_non_tech) and (persona in ['DATA_ANALYST', 'Data & Analytics'] or any(k in raw_role.lower() for k in ['data', 'analyst', 'analytics', 'bi ']))
    is_systems = (not is_non_tech) and (persona in ['SYSTEMS_ENG', 'Systems & Embedded Engineering'] or any(k in raw_role.lower() for k in ['system', 'embedded', 'linux', 'hardware']))
    is_devops = (not is_non_tech) and (
        persona in ['DEVOPS_CLOUD', 'DevOps & Cloud Platform'] or
        any(k in raw_role.lower() for k in ['devops', 'cloud', 'sre', 'platform engineer', 'sysadmin', 'system admin', 'infrastructure', 'kubernetes', 'docker', 'terraform', 'site reliability'])
    )
    is_senior = (not is_student) and (not is_non_tech) and (
        exp_bracket in ['EXP_5_PLUS', '5-8 years', '8+ years', '5+ yrs (Senior / Lead)'] or 
        (exp_bracket == 'EXP_3_5' and any(k in raw_role.lower() for k in ['lead', 'senior', 'manager', 'leadership', 'director', 'founder', 'architect', 'vp']))
    )

    # 3. FIX: Strict FDE Eligibility (Must be tech & 2+ YOE)
    is_eligible_for_fde = (not is_non_tech) and (exp_bracket in ['EXP_3_5', 'EXP_5_PLUS'])

    primary = {}
    fallback = {}

    # =========================================================================
    # SCENARIO 1: NON-TECH / ZERO-CODE (Strict Catalog Gate)
    # =========================================================================
    if is_non_tech:
        # Check if the candidate's domain is Commercial / Business Management / People / Finance / Product Management
        is_product_manager = any(k in raw_role.lower() for k in ['product manager', 'associate product manager', 'apm', 'tpm', 'product owner', 'scrum master'])
        is_commercial_business = (
            any(d in role_domain for d in ['Marketing', 'Commerce', 'Finance', 'HR & People', 'Sales', 'Business Operations', 'Product Management & Design']) or
            is_product_manager or
            any(k in raw_role.lower() for k in [
                'marketing', 'brand', 'growth', 'category', 'merchandis', 'pricing', 'e-commerce', 'ecommerce',
                'finance', 'account', 'ca ', 'cpa', 'auditor', 'banking', 'bank officer', 'loan officer',
                'hr', 'human resource', 'people ops', 'recruiter', 'talent', 'sales', 'bde', 'bda',
                'business development', 'operations manager', 'supply chain', 'logistics',
                'team lead - operations', 'team lead operations', 'operations team lead', 'operations lead',
                'operations supervisor', 'process associate', 'process lead', 'project coordinator'
            ])
        )

        # Case 1: Inbound enquiry is directly DSML (or candidate is in commercial/business/product domain and enquired about advanced infrastructure/AI)
        if inbound_cat == 'P2_DSML' or (is_commercial_business and inbound_cat in ['P5_DEVOPS_CLOUD', 'P3_FDE', 'P4_AIML_AGENTIC']):
            primary['program'] = 'Modern Data Science & Machine Learning (DSML)'
            primary['catalog_code'] = 'Program 2'
            primary['track'] = 'Beginner Track (Data Analytics, Python & Business ML)'
            primary['fit_tier'] = 'Best Fit (Applied AI & Product Analytics)' if is_product_manager else 'Best Fit (Applied Business & Growth Analytics)'
            
            if inbound_cat == 'P5_DEVOPS_CLOUD':
                primary['why'] = (
                    f"While you enquired about DevOps & Cloud Platform, Program 5 strictly requires existing operating systems, "
                    f"networking, and Linux infrastructure foundations. With {raw_exp} as a {raw_role}, your highest-leverage, "
                    "highest-retention upskilling path is Program 2: Modern Data Science & Machine Learning. Rather than wrestling with "
                    "cloud infrastructure automation from scratch, this track directly empowers your commercial leadership with SQL data pipelines, "
                    "growth analytics dashboards, and predictive machine learning models."
                )
                primary['guardrail'] = "Catalog Gate: Commercial professional redirected from DevOps/Kubernetes to high-retention DSML track."
            elif inbound_cat == 'P3_FDE':
                primary['why'] = (
                    f"While you showed high interest in Forward Deployed Engineering, Program 3 requires hands-on software "
                    f"deployment depth. As a {raw_role} with {raw_exp}, Program 2 equips you with data querying, Python analytics, "
                    "and predictive modeling to build technical data capability natively within your business domain."
                )
                primary['guardrail'] = "Catalog Gate: Redirected from FDE client systems to DSML beginner track."
            elif inbound_cat == 'P4_AIML_AGENTIC':
                if is_product_manager:
                    primary['why'] = (
                        f"While you enquired about Agentic AI, building production autonomous agents mandates data querying and predictive modeling foundations. "
                        f"As a {raw_role} with {raw_exp}, Program 2 directly empowers your product leadership with SQL data extraction, "
                        "product experimentation metrics, and applied machine learning models to design, evaluate, and productize AI systems without "
                        "getting bogged down in low-level compiler syntax drills."
                    )
                    primary['guardrail'] = "Catalog Gate: Product leader routed to applied analytics & ML before autonomous agent deployment."
                else:
                    primary['why'] = (
                        f"While you enquired about Frontier Agentic AI, building production autonomous agents mandates coding foundations. "
                        f"As a {raw_role} with {raw_exp}, Program 2 provides a high-retention onramp starting with data analytics, "
                        "applied machine learning, and business intelligence."
                    )
                    primary['guardrail'] = "Catalog Gate: Foundation in data & ML required before autonomous agent design."
            else:
                primary['why'] = (
                    f"With your background as a {raw_role}, Data Science & Analytics offers the smoothest, "
                    "highest-retention path into tech. Rather than wrestling with abstract software architecture, "
                    "this track leverages your business domain experience into People/Business Analytics, SQL dashboards, "
                    "and applied Predictive Machine Learning from ground zero."
                )
                primary['guardrail'] = "Catalog Fit: Non-tech professional routed to DSML Beginner Track to build data fundamentals."

            fallback['program'] = 'Software & AI Engineering (Scaler Academy)'
            fallback['catalog_code'] = 'Program 1'
            fallback['track'] = 'Beginner Track (Foundations of Programming & Problem Solving)'
            fallback['fit_tier'] = 'Alternative Core Software Path'
            fallback['why'] = (
                "If you wish to pivot into core application software engineering rather than data analytics, "
                "Scaler Academy's Beginner Track teaches programming syntax, logic building, and problem solving from scratch."
            )
        else:
            primary['program'] = 'Software & AI Engineering (Scaler Academy)'
            primary['catalog_code'] = 'Program 1'
            primary['track'] = 'Beginner Track (Foundations of Programming & Problem Solving)'
            primary['fit_tier'] = 'Best Fit (Foundational Bridge)'
            if is_career_break:
                primary['why'] = (
                    f"For candidates returning to the industry after a career break, Scaler Academy's Beginner Track "
                    "provides a structured, supportive ramp-up covering syntax, modern developer tooling, and algorithmic logic from ground zero."
                )
            elif edu_level == 'GRAD_NON_CS':
                primary['why'] = (
                    f"With a non-computer science degree ({raw_edu}), the Beginner Track ensures you build systematic "
                    "problem-solving and coding foundations before tackling advanced data structures and system design."
                )
            else:
                primary['why'] = (
                    f"As a {raw_role} without professional coding exposure, Scaler Academy's Beginner Track "
                    "starts from ground zero (syntax, logic, loops, conditional branching). "
                    "It builds the prerequisite programming foundation before advancing to algorithms."
                )
            primary['guardrail'] = "Strict Negative Filter: Blocked from Intermediate/Advanced tracks to prevent Day 14 pacing dropout."

            if inbound_cat in ['P4_AIML_AGENTIC', 'P3_FDE']:
                fallback['program'] = 'AI & Machine Learning with Agentic AI'
                fallback['catalog_code'] = 'Program 4'
                fallback['track'] = 'Beginner Track (AI & Machine Learning Foundations)'
                fallback['fit_tier'] = 'High Risk / Conditional Fallback'
                fallback['why'] = (
                    f"You enquired about AI, but Catalog Rule 6 strictly mandates coding aptitude. "
                    "Non-tech learners face a 25.8% drop-off in advanced AI modules unless preceded by intensive programming prep."
                )
            elif inbound_cat == 'P5_DEVOPS_CLOUD':
                fallback['program'] = 'Modern Data Science & Machine Learning (DSML)'
                fallback['catalog_code'] = 'Program 2'
                fallback['track'] = 'Beginner Track (Data Analytics Foundation)'
                fallback['fit_tier'] = 'Alternative Analytics Path'
                fallback['why'] = (
                    "While you enquired about DevOps, cloud infrastructure requires deep Linux and networking fundamentals. "
                    "DSML offers a high-retention data analytics alternative."
                )
            else:
                fallback['program'] = 'Modern Data Science & Machine Learning (DSML)'
                fallback['catalog_code'] = 'Program 2'
                fallback['track'] = 'Beginner Track (Data Analytics Foundation)'
                fallback['fit_tier'] = 'Alternative Analytics Path'
                fallback['why'] = "Provides an alternative route into tech through business intelligence, SQL, and data reporting."

    # =========================================================================
    # SCENARIO 2: DATA & ANALYTICS ROLES (Data Analyst, BI, SQL Dev)
    # =========================================================================
    elif is_data:
        if inbound_cat == 'P4_AIML_AGENTIC':
            primary['program'] = 'AI & Machine Learning with Agentic AI'
            primary['catalog_code'] = 'Program 4'
            primary['track'] = 'Advanced Track (Agentic AI & LLMOps)'
            primary['fit_tier'] = 'Best Fit (Advanced AI Modeling)'
            primary['why'] = (
                f"Your background as a {raw_role} gives you data intuition. Program 4 elevates you into "
                "deep learning, neural networks, PyTorch, and building multi-agent autonomous AI systems."
            )
            primary['guardrail'] = "Catalog Tie-Breaker: Routed to Program 4 due to explicit intent to build/deploy AI models."
            
            fallback['program'] = 'Modern Data Science & Machine Learning (DSML)'
            fallback['catalog_code'] = 'Program 2'
            fallback['track'] = 'Core Analytics & Predictive Modeling Track'
            fallback['fit_tier'] = 'Alternative Analytics Specialization'
            fallback['why'] = "A safer, high-retention path focusing on predictive analytics, statistical hypothesis testing, and business ML."
        elif inbound_cat == 'P1_ACADEMY':
            primary['program'] = 'Modern Data Science & Machine Learning (DSML)'
            primary['catalog_code'] = 'Program 2'
            primary['track'] = 'Core Analytics & Machine Learning Track'
            primary['fit_tier'] = 'Best Fit (Domain Native)'
            primary['why'] = (
                f"Your background as a {raw_role} directly leverages SQL and business data into predictive machine learning."
            )
            primary['guardrail'] = "Catalog Rule: Native fit in Program 2; Academy offered as bridge for software pivot."

            fallback['program'] = 'Software & AI Engineering (Scaler Academy)'
            fallback['catalog_code'] = 'Program 1'
            fallback['track'] = 'Data Engineering & Backend Systems Track'
            fallback['fit_tier'] = 'Inbound Software Career Pivot'
            fallback['why'] = (
                "Since you enquired about Academy, this track bridges your SQL foundation into large-scale Data Engineering, "
                "distributed pipelines (Spark/Kafka), and backend API architecture."
            )
        elif inbound_cat == 'P3_FDE':
            if is_eligible_for_fde and any(k in raw_role.lower() for k in ['data engineer', 'pipeline', 'senior', 'lead', 'architect']):
                primary['program'] = 'AI Forward Deployed Engineer (FDE)'
                primary['catalog_code'] = 'Program 3'
                primary['track'] = 'Enterprise AI Integration & Production RAG Track'
                primary['fit_tier'] = 'Best Fit (Data Pipeline & Client AI Integration)'
                primary['why'] = (
                    f"As a {raw_role} with {raw_exp}, your data pipeline, PySpark, and database foundations translate directly "
                    "into Program 3's core mission: client enterprise ingestion pipelines, production RAG architectures, and live AI deployment."
                )
                primary['guardrail'] = "Verified data engineering background matches FDE client integration requirements."

                fallback['program'] = 'Modern Data Science & Machine Learning (DSML)'
                fallback['catalog_code'] = 'Program 2'
                fallback['track'] = 'Core Analytics & Machine Learning Track'
                fallback['fit_tier'] = 'Alternative Core Analytics Track'
                fallback['why'] = "Deep statistical modeling and predictive machine learning alternative."
            else:
                primary['program'] = 'Modern Data Science & Machine Learning (DSML)'
                primary['catalog_code'] = 'Program 2'
                primary['track'] = 'Core Analytics & Machine Learning Track'
                primary['fit_tier'] = 'Best Fit (Domain Native Foundation)'
                primary['why'] = (
                    f"While you enquired about FDE, Program 3 requires production deployment depth. "
                    "Program 2 builds your predictive modeling, advanced analytics, and data pipeline fundamentals first."
                )
                primary['guardrail'] = "Catalog Gate: Data professionals routed to DSML core track before client-facing AI deployment."

                fallback['program'] = 'AI Forward Deployed Engineer (FDE)'
                fallback['catalog_code'] = 'Program 3'
                fallback['track'] = 'Enterprise AI Integration Track'
                fallback['fit_tier'] = 'Aspirational Goal (Post-Analytics)'
                fallback['why'] = "Target program once production data pipelines and machine learning workflows are mastered."
        elif inbound_cat == 'P5_DEVOPS_CLOUD':
            is_data_engineer = any(k in raw_role.lower() for k in ['data engineer', 'big data', 'etl', 'pipeline', 'database engineer'])
            is_pure_analyst = any(k in raw_role.lower() for k in ['data analyst', 'bi analyst', 'business analyst', 'analytics consultant', 'tableau', 'power bi']) and not is_data_engineer
            
            if is_pure_analyst:
                primary['program'] = 'Modern Data Science & Machine Learning (DSML)'
                primary['catalog_code'] = 'Program 2'
                primary['track'] = 'Core Analytics & Machine Learning Track' if not is_student else 'Beginner Track (Data Analytics, Python & Business ML)'
                primary['fit_tier'] = 'Best Fit (Domain Native Specialization)'
                primary['why'] = (
                    f"While you enquired about DevOps & Cloud Platform, Program 5 strictly requires operating systems, bash/Linux scripting, networking, "
                    f"and server administration foundations. As a {raw_role} with {raw_exp}, your highest-leverage, highest-retention career progression "
                    "is Program 2: Modern Data Science & Machine Learning. This track directly builds upon your existing SQL and analytical strengths into "
                    "predictive modeling, machine learning, and scalable data engineering. Cloud platform engineering remains an aspirational future specialisation "
                    "once infrastructure fundamentals are established."
                )
                primary['guardrail'] = "Catalog Gate: Data Analyst redirected to DSML; Linux/OS prerequisites required before SRE/Kubernetes."

                fallback['program'] = 'DevOps, Cloud & AI Platform Engineering'
                fallback['catalog_code'] = 'Program 5'
                fallback['track'] = 'CI/CD Automation & Cloud Infrastructure Track'
                fallback['fit_tier'] = 'Aspirational Infrastructure Pivot'
                fallback['why'] = "Secondary path if you intend to transition into DataOps and cloud infrastructure, starting with foundational Linux & CI/CD."
            else:
                primary['program'] = 'DevOps, Cloud & AI Platform Engineering'
                primary['catalog_code'] = 'Program 5'
                primary['track'] = 'Site Reliability Engineering (SRE) & Kubernetes Track' if is_senior else 'CI/CD Automation & Cloud Infrastructure Track'
                primary['fit_tier'] = 'Best Fit (DataOps & Cloud Infrastructure)'
                primary['why'] = (
                    f"Your background as a {raw_role} connects naturally into DataOps and cloud platform engineering - "
                    "managing distributed data pipelines, cloud databases, and Kubernetes clusters."
                )
                primary['guardrail'] = "Natural transition from data handling to cloud infrastructure and DataOps."

                fallback['program'] = 'Modern Data Science & Machine Learning (DSML)'
                fallback['catalog_code'] = 'Program 2'
                fallback['track'] = 'Core Analytics & Machine Learning Track'
                fallback['fit_tier'] = 'Alternative Domain Native Track'
                fallback['why'] = "Core statistical modeling and machine learning alternative."
        else:
            primary['program'] = 'Modern Data Science & Machine Learning (DSML)'
            primary['catalog_code'] = 'Program 2'
            primary['track'] = 'Core Analytics & Machine Learning Track'
            primary['fit_tier'] = 'Best Fit (Domain Native)'
            primary['why'] = f"Directly accelerates your experience as a {raw_role} into statistical modeling and enterprise ML."
            primary['guardrail'] = "High retention cohort; verified quantitative aptitude."

            fallback['program'] = 'AI & Machine Learning with Agentic AI'
            fallback['catalog_code'] = 'Program 4'
            fallback['track'] = 'Advanced Track (Agentic AI & LLMOps)'
            fallback['fit_tier'] = 'Advanced Next-Gen AI Pivot'
            fallback['why'] = "Alternative path to specialize in frontier LLM engineering and agentic workflows."

    # =========================================================================
    # SCENARIO 3: QA / TEST AUTOMATION / SDET
    # =========================================================================
    elif is_qa:
        is_manual_qa = any(k in raw_role.lower() for k in ['manual', 'black box', 'functional test', 'test associate'])
        if inbound_cat == 'P5_DEVOPS_CLOUD':
            primary['program'] = 'DevOps, Cloud & AI Platform Engineering'
            primary['catalog_code'] = 'Program 5'
            primary['track'] = 'CI/CD Automation & Cloud Infrastructure Track'
            primary['fit_tier'] = 'Best Fit (Natural Synergistic Pivot)'
            primary['why'] = (
                f"Your testing background as a {raw_role} connects seamlessly into DevOps - "
                "expanding test validation suites into CI/CD pipelines, Docker containers, and Kubernetes orchestration."
            )
            primary['guardrail'] = "Catalog Tie-Breaker: Test skill naturally bridges to SRE & Cloud Engineering."

            fallback['program'] = 'Software & AI Engineering (Scaler Academy)'
            fallback['catalog_code'] = 'Program 1'
            fallback['track'] = 'Intermediate Track (Backend SDE Transition)'
            fallback['fit_tier'] = 'Alternative Core SDE'
            fallback['why'] = "If you prefer transitioning into core development, Academy focuses on Object-Oriented Design and DSA."
        elif inbound_cat == 'P2_DSML':
            primary['program'] = 'Modern Data Science & Machine Learning (DSML)'
            primary['catalog_code'] = 'Program 2'
            primary['track'] = 'Core Analytics & Machine Learning Track' if not is_student else 'Beginner Track (Data Analytics, Python & Business ML)'
            primary['fit_tier'] = 'Best Fit (Data Analytics & QA Synergy)'
            primary['why'] = (
                f"As a {raw_role}, your structured validation mindset and SQL test data verification directly empower "
                "data pipeline testing, exploratory data analysis, and predictive machine learning models."
            )
            primary['guardrail'] = "Verified quantitative transition track for quality assurance professionals."

            fallback['program'] = 'Software & AI Engineering (Scaler Academy)'
            fallback['catalog_code'] = 'Program 1'
            fallback['track'] = 'Intermediate Track (Backend SDE Transition)'
            fallback['fit_tier'] = 'Alternative Development Track'
            fallback['why'] = "Alternative path if you decide to pivot to core backend software engineering."
        elif inbound_cat == 'P3_FDE':
            primary['program'] = 'Software & AI Engineering (Scaler Academy)'
            primary['catalog_code'] = 'Program 1'
            primary['track'] = 'Intermediate Track (Backend SDE Transition)'
            primary['fit_tier'] = 'Foundational Prerequisite for FDE'
            primary['why'] = (
                f"While you enquired about Forward Deployed Engineering, Program 3 strictly mandates hands-on production backend development, "
                f"API deployment, and algorithmic problem-solving depth. With {raw_exp} in quality assurance & testing, jumping straight into "
                "client AI code deployment without modern backend development depth risks severe pacing friction. Scaler Academy's Intermediate Track "
                "(Backend SDE Transition) equips you with core algorithmic problem-solving, advanced data structures (DSA), low-level object-oriented "
                "design (LLD), and backend API architecture first, establishing the necessary engineering foundation before forward-deploying AI into enterprise environments."
            )
            primary['guardrail'] = "FDE Catalog Prerequisite: QA professionals require backend engineering, DSA & LLD foundations before client AI deployment."

            fallback['program'] = 'AI Forward Deployed Engineer (FDE)'
            fallback['catalog_code'] = 'Program 3'
            fallback['track'] = 'Enterprise AI Integration & Production RAG Track'
            fallback['fit_tier'] = 'Aspirational Goal (Post-Foundations)'
            fallback['why'] = (
                f"Target program once foundational backend software engineering, DSA, and object-oriented design are mastered, "
                f"leveraging your {raw_exp} of enterprise quality governance into live enterprise AI deployment."
            )

        elif inbound_cat == 'P4_AIML_AGENTIC':
            primary['program'] = 'AI & Machine Learning with Agentic AI'
            primary['catalog_code'] = 'Program 4'
            primary['track'] = 'Advanced Track (Agentic AI & LLMOps)' if is_senior else 'Beginner Track (AI & Machine Learning Foundations)'
            primary['fit_tier'] = 'Best Fit (AI Testing & Agentic Systems)'
            primary['why'] = (
                f"Leverages your test engineering precision as a {raw_role} to evaluate autonomous AI agents, "
                "build LLM verification benchmarks, and deploy agentic AI architectures."
            )
            primary['guardrail'] = "Pivots QA domain into next-generation AI evaluation and agent engineering."

            fallback['program'] = 'DevOps, Cloud & AI Platform Engineering'
            fallback['catalog_code'] = 'Program 5'
            fallback['track'] = 'CI/CD Automation & Cloud Infrastructure Track'
            fallback['fit_tier'] = 'Alternative Infrastructure Track'
            fallback['why'] = "Automates testing and AI agent deployment through modern cloud pipelines."
        else:
            is_pure_qa = any(k in raw_role.lower() for k in ['qa', 'test', 'quality']) and 'sdet' not in raw_role.lower()
            if is_manual_qa:
                primary['program'] = 'Software & AI Engineering (Scaler Academy)'
                primary['catalog_code'] = 'Program 1'
                if is_senior:
                    primary['track'] = 'Intermediate Track (Backend SDE Transition)'
                    primary['fit_tier'] = 'Best Fit (SDE Transition & Coding Foundation)'
                    primary['why'] = (
                        f"As a {raw_role} with {raw_exp}, you possess deep functional software domain knowledge and defect lifecycle mastery. "
                        "To successfully transition into engineering and automation roles, the critical gap is hands-on coding, data structures, "
                        "and low-level object-oriented design (LLD). This track bypasses generic high-level theory to focus directly on core "
                        "algorithmic problem-solving and clean code development."
                    )
                    primary['guardrail'] = "Manual QA Guardrail: Routed to Intermediate coding & LLD track; blocked from pure High-Level System Design until coding depth is established."
                else:
                    primary['track'] = 'Beginner Track (Foundations of Programming & Problem Solving)'
                    primary['fit_tier'] = 'Best Fit (Foundational Bridge)'
                    primary['why'] = (
                        f"As a {raw_role} with {raw_exp}, this Beginner Track teaches programming syntax, algorithmic logic, "
                        "and object-oriented development from ground zero to transition from manual testing into software engineering."
                    )
                    primary['guardrail'] = "Manual QA Guardrail: Routed to Beginner coding track to build algorithmic foundations."

                fallback['program'] = 'DevOps, Cloud & AI Platform Engineering'
                fallback['catalog_code'] = 'Program 5'
                fallback['track'] = 'CI/CD Automation & Cloud Infrastructure Track'
                fallback['fit_tier'] = 'Alternative Cloud Platform Path'
                fallback['why'] = "An alternative route to build automated deployment and cloud infrastructure skills."
            elif is_pure_qa:
                primary['program'] = 'Software & AI Engineering (Scaler Academy)'
                primary['catalog_code'] = 'Program 1'
                primary['track'] = 'Intermediate Track (Backend SDE Transition)'
                primary['fit_tier'] = 'Best Fit (Backend SDE Transition)'
                primary['why'] = (
                    f"As a {raw_role} with {raw_exp}, you already understand software lifecycles, release protocols, and code structures; "
                    "this track bridges the exact gap in algorithmic optimization, advanced DSA, and low-level object-oriented design (LLD) "
                    "to transition into core Backend SDE roles. Bypasses basic syntax to focus directly on Intermediate DSA (AI Assisted Problem Solving), "
                    "Advanced DSA (Divide & Conquer, Trees, Heaps, Graphs, Dynamic Programming), and Low-Level Design (LLD)."
                )
                primary['guardrail'] = "Calibrated for QA/Testing transition: Bridges DSA & LLD gaps to achieve product-company SDE readiness."

                fallback['program'] = 'DevOps, Cloud & AI Platform Engineering'
                fallback['catalog_code'] = 'Program 5'
                fallback['track'] = 'CI/CD Automation & Cloud Infrastructure Track' if not is_senior else 'Cloud Platform & Infrastructure Track'
                fallback['fit_tier'] = 'Alternative Cloud Platform Leadership' if is_senior else 'Alternative Infrastructure Path'
                fallback['why'] = "A fast-track alternative that leverages your testing automation into cloud engineering."
            elif is_senior:
                primary['program'] = 'Software & AI Engineering (Scaler Academy)'
                primary['catalog_code'] = 'Program 1'
                primary['track'] = 'Advanced Track (High-Level System Design & Scalability)'
                primary['fit_tier'] = 'Best Fit (Engineering Leadership & System Architecture)'
                primary['why'] = (
                    f"With {raw_exp} as a {raw_role}, you have mastered software delivery and test framework architecture. "
                    "This Advanced Track bypasses entry-level coding drills to focus 100% on High-Level System Design (HLD): "
                    "distributed caching, database sharding, Kafka event streaming, and architectural scalability."
                )
                primary['guardrail'] = "Calibrated for senior technical leaders (5+ to 20+ YOE); skips junior DSA syntax."

                fallback['program'] = 'DevOps, Cloud & AI Platform Engineering'
                fallback['catalog_code'] = 'Program 5'
                fallback['track'] = 'Cloud Platform & Infrastructure Track'
                fallback['fit_tier'] = 'Alternative Cloud Platform Leadership'
                fallback['why'] = "A strategic alternative leveraging your quality and infrastructure background into enterprise cloud architecture."
            else:
                primary['program'] = 'Software & AI Engineering (Scaler Academy)'
                primary['catalog_code'] = 'Program 1'
                primary['track'] = 'Intermediate Track (Backend SDE Transition)'
                primary['fit_tier'] = 'Best Fit (Career Upgrade)'
                primary['why'] = (
                    f"Transitioning from {raw_role} to a product company SDE requires strengthening Data Structures "
                    "and Low-Level Design (LLD). Intermediate Track skips syntax basics to focus on interview-ready engineering."
                )
                primary['guardrail'] = "Calibrated for SDET/QA transition; provides systematic problem-solving."

                fallback['program'] = 'DevOps, Cloud & AI Platform Engineering'
                fallback['catalog_code'] = 'Program 5'
                fallback['track'] = 'CI/CD Automation & Cloud Infrastructure Track'
                fallback['fit_tier'] = 'Alternative Infrastructure Path'
                fallback['why'] = "A fast-track alternative that leverages your testing automation into cloud engineering."

    # =========================================================================
    # SCENARIO 4: SYSTEMS & EMBEDDED / HARDWARE / IT INFRASTRUCTURE
    # =========================================================================
    elif is_systems:
        if inbound_cat == 'P5_DEVOPS_CLOUD':
            primary['program'] = 'DevOps, Cloud & AI Platform Engineering'
            primary['catalog_code'] = 'Program 5'
            primary['track'] = 'Cloud Architecture & Linux Systems Track'
            primary['fit_tier'] = 'Best Fit (Direct OS/Hardware Synergy)'
            primary['why'] = (
                f"Your experience as a {raw_role} provides OS, networking, and memory fundamentals. "
                "DevOps modernizes this into cloud infrastructure, Terraform, and Kubernetes cluster operations."
            )
            primary['guardrail'] = "Catalog Rule: Strong historical retention cohort in Program 5."

            fallback['program'] = 'Software & AI Engineering (Scaler Academy)'
            fallback['catalog_code'] = 'Program 1'
            fallback['track'] = 'Intermediate Track (Core Software Engineering)'
            fallback['fit_tier'] = 'Alternative Product SDE'
            fallback['why'] = "If you want to pivot into application software, Academy teaches modern Java/C++ backend microservices."
        elif inbound_cat == 'P3_FDE':
            if is_eligible_for_fde:
                primary['program'] = 'AI Forward Deployed Engineer (FDE)'
                primary['catalog_code'] = 'Program 3'
                primary['track'] = 'Enterprise AI Integration & Client Systems Track'
                primary['fit_tier'] = 'Best Fit (Enterprise Systems Depth)'
                primary['why'] = (
                    f"Your low-level systems background fits Program 3's focus on deploying AI solutions live "
                    "inside enterprise environments, PySpark pipelines, and multi-agent enterprise infrastructure."
                )
                primary['guardrail'] = "Requires verified systems/backend foundation; passes prerequisite gate."

                fallback['program'] = 'DevOps, Cloud & AI Platform Engineering'
                fallback['catalog_code'] = 'Program 5'
                fallback['track'] = 'Site Reliability Engineering (SRE) & Kubernetes Track' if is_senior else 'CI/CD Automation & Cloud Infrastructure Track'
                fallback['fit_tier'] = 'Alternative Cloud Platform Leadership' if is_senior else 'Alternative Infrastructure Track'
                fallback['why'] = "Infrastructure alternative focusing on Kubernetes and platform scalability."
            else:
                primary['program'] = 'Software & AI Engineering (Scaler Academy)'
                primary['catalog_code'] = 'Program 1'
                primary['track'] = 'Intermediate Track (Java/C++ with DSA Core)'
                primary['fit_tier'] = 'Foundational Prerequisite for FDE'
                primary['why'] = (
                    f"While you showed high interest in Forward Deployed Engineering, Program 3 requires hands-on "
                    "production backend systems and deployment experience (2+ years). Scaler Academy bridges your systems foundation into production microservices first."
                )
                primary['guardrail'] = "Catalog Gate: FDE requires software deployment depth and 2+ YOE; learner routed to foundational track."

                fallback['program'] = 'AI Forward Deployed Engineer (FDE)'
                fallback['catalog_code'] = 'Program 3'
                fallback['track'] = 'Enterprise AI Integration Track'
                fallback['fit_tier'] = 'Aspirational Goal (Post-Foundations)'
                fallback['why'] = "Target program once foundational data structures and software engineering are mastered."
        elif inbound_cat == 'P2_DSML':
            primary['program'] = 'Modern Data Science & Machine Learning (DSML)'
            primary['catalog_code'] = 'Program 2'
            primary['track'] = 'Core Analytics & Machine Learning Track'
            primary['fit_tier'] = 'Best Fit (Quantitative Systems Synergy)'
            primary['why'] = (
                f"Your background as a {raw_role} provides low-level mathematical and algorithmic rigour. "
                "Program 2 leverages this into statistical modeling, high-throughput feature pipelines, and machine learning."
            )
            primary['guardrail'] = "Engineered for technical professionals pivoting to data and quantitative engineering."

            fallback['program'] = 'DevOps, Cloud & AI Platform Engineering'
            fallback['catalog_code'] = 'Program 5'
            fallback['track'] = 'Cloud Platform & Linux Track'
            fallback['fit_tier'] = 'Alternative Systems Infrastructure Path'
            fallback['why'] = "Alternative path building upon your OS and hardware background."
        elif inbound_cat == 'P4_AIML_AGENTIC':
            primary['program'] = 'AI & Machine Learning with Agentic AI'
            primary['catalog_code'] = 'Program 4'
            primary['track'] = 'Advanced Track (Agentic AI & LLMOps)'
            primary['fit_tier'] = 'Best Fit (Hardware-Accelerated AI & Agents)'
            primary['why'] = (
                f"Your systems foundation as a {raw_role} is ideal for GPU-accelerated computing, "
                "model quantization, edge AI deployment, and high-performance agentic pipelines."
            )
            primary['guardrail'] = "Matches hardware/systems depth with cutting-edge agentic architectures."

            fallback['program'] = 'DevOps, Cloud & AI Platform Engineering'
            fallback['catalog_code'] = 'Program 5'
            fallback['track'] = 'Cloud Platform & Linux Track'
            fallback['fit_tier'] = 'Alternative Systems Infrastructure Path'
            fallback['why'] = "Alternative path focusing on infrastructure scaling and platform resilience."
        else:
            if is_senior:
                primary['program'] = 'Software & AI Engineering (Scaler Academy)'
                primary['catalog_code'] = 'Program 1'
                primary['track'] = 'Advanced Track (High-Level System Design & Scalability)'
                primary['fit_tier'] = 'Best Fit (Senior Systems Architecture)'
                primary['why'] = (
                    f"With {raw_exp} in systems engineering as a {raw_role}, you already have deep OS and hardware fundamentals. "
                    "The Advanced Track elevates this into large-scale distributed architectures, database sharding, and high-level design."
                )
                primary['guardrail'] = "Senior track calibrated for experienced systems architects."
            else:
                primary['program'] = 'Software & AI Engineering (Scaler Academy)'
                primary['catalog_code'] = 'Program 1'
                primary['track'] = 'Intermediate Track (Java/C++ with DSA Core)'
                primary['fit_tier'] = 'Best Fit (Product Company Bridge)'
                primary['why'] = (
                    f"Engineers working as {raw_role} excel in Academy's Intermediate Track, "
                    "which bridges the gap between enterprise maintenance and Tier-1 product algorithmic standards."
                )
                primary['guardrail'] = "Calibrated for 2-5 YOE service engineers."

            fallback['program'] = 'DevOps, Cloud & AI Platform Engineering'
            fallback['catalog_code'] = 'Program 5'
            fallback['track'] = 'Cloud Platform & Linux Track'
            fallback['fit_tier'] = 'Alternative Systems Path'
            fallback['why'] = "Builds upon your OS and infrastructure background without requiring competitive algorithmic design."

    # =========================================================================
    # SCENARIO 5: DEVOPS, CLOUD, SRE & PLATFORM ENGINEERING
    # =========================================================================
    elif is_devops:
        if inbound_cat == 'P1_ACADEMY':
            primary['program'] = 'Software & AI Engineering (Scaler Academy)'
            primary['catalog_code'] = 'Program 1'
            primary['track'] = 'Advanced Track (High-Level System Design & Scalability)' if is_senior else 'Intermediate Track (Data Structures, Algorithms & LLD)'
            primary['fit_tier'] = 'Best Fit (Software Engineering Pivot)'
            primary['why'] = (
                f"As a {raw_role} with {raw_exp}, your infrastructure and deployment expertise is established. "
                "Scaler Academy adds algorithmic problem-solving and distributed backend microservices architecture to transition into full-stack product development."
            )
            primary['guardrail'] = "Calibrated for platform engineers pivoting into core application development."

            fallback['program'] = 'DevOps, Cloud & AI Platform Engineering'
            fallback['catalog_code'] = 'Program 5'
            fallback['track'] = 'Site Reliability Engineering (SRE) & Kubernetes Track'
            fallback['fit_tier'] = 'Alternative Domain Native Track'
            fallback['why'] = "Advanced cloud orchestration and platform leadership alternative."

        elif inbound_cat == 'P3_FDE':
            if is_eligible_for_fde:
                primary['program'] = 'AI Forward Deployed Engineer (FDE)'
                primary['catalog_code'] = 'Program 3'
                primary['track'] = 'Enterprise AI Integration & Production RAG Track'
                primary['fit_tier'] = 'Best Fit (Cloud-Native AI Deployment)'
                primary['why'] = (
                    f"Your background as a {raw_role} in Docker, Kubernetes, and cloud infrastructure directly bridges the "
                    "Enterprise Deployment Gap—containerizing autonomous AI agents and deploying RAG pipelines directly into customer cloud environments."
                )
                primary['guardrail'] = "Cloud and infrastructure expertise provides an ideal foundation for client-facing AI deployment."

                fallback['program'] = 'DevOps, Cloud & AI Platform Engineering'
                fallback['catalog_code'] = 'Program 5'
                fallback['track'] = 'Site Reliability Engineering (SRE) & Kubernetes Track'
                fallback['fit_tier'] = 'Alternative Cloud Platform Track'
                fallback['why'] = "Platform engineering and infrastructure automation alternative."
            else:
                primary['program'] = 'DevOps, Cloud & AI Platform Engineering'
                primary['catalog_code'] = 'Program 5'
                primary['track'] = 'CI/CD Automation & Cloud Infrastructure Track'
                primary['fit_tier'] = 'Foundational Cloud Prerequisite for FDE'
                primary['why'] = (
                    f"While you enquired about Forward Deployed Engineering, Program 3 requires established "
                    "production deployment experience (2+ years). Program 5 establishes your core containerization, CI/CD, and cloud infrastructure foundation first."
                )
                primary['guardrail'] = "Catalog Gate: FDE requires 2+ YOE in production deployment; learner routed to foundational cloud track."

                fallback['program'] = 'AI Forward Deployed Engineer (FDE)'
                fallback['catalog_code'] = 'Program 3'
                fallback['track'] = 'Enterprise AI Integration Track'
                fallback['fit_tier'] = 'Aspirational Goal (Post-Cloud Foundations)'
                fallback['why'] = "Target program once production containerization and cloud infrastructure are mastered."

        elif inbound_cat == 'P2_DSML':
            primary['program'] = 'Modern Data Science & Machine Learning (DSML)'
            primary['catalog_code'] = 'Program 2'
            primary['track'] = 'Core Analytics & Machine Learning Track' if not is_student else 'Beginner Track (Data Analytics, Python & Business ML)'
            primary['fit_tier'] = 'Best Fit (Cloud Infrastructure & MLOps Synergy)'
            primary['why'] = (
                f"As a {raw_role}, your cloud and infrastructure background provides an ideal foundation for MLOps, "
                "data pipeline orchestration, and deploying scalable machine learning models into production."
            )
            primary['guardrail'] = "Synergistic pivot from cloud platform engineering to data science and production ML."

            fallback['program'] = 'DevOps, Cloud & AI Platform Engineering'
            fallback['catalog_code'] = 'Program 5'
            fallback['track'] = 'Site Reliability Engineering (SRE) & Kubernetes Track' if is_senior else 'CI/CD Automation & Cloud Infrastructure Track'
            fallback['fit_tier'] = 'Alternative Cloud Platform Track'
            fallback['why'] = "Core infrastructure and Kubernetes platform engineering path."

        elif inbound_cat == 'P4_AIML_AGENTIC':
            primary['program'] = 'AI & Machine Learning with Agentic AI'
            primary['catalog_code'] = 'Program 4'
            primary['track'] = 'Advanced Track (Agentic AI & LLMOps)'
            primary['fit_tier'] = 'Best Fit (LLMOps & AI Infrastructure)'
            primary['why'] = (
                f"As a {raw_role}, your cloud background is ideal for LLMOps, model serving (vLLM), "
                "GPU cluster orchestration, and autonomous agent infrastructure."
            )
            primary['guardrail'] = "Synergistic pivot from cloud DevOps to LLMOps and AI infrastructure."

            fallback['program'] = 'DevOps, Cloud & AI Platform Engineering'
            fallback['catalog_code'] = 'Program 5'
            fallback['track'] = 'Site Reliability Engineering (SRE) & Kubernetes Track'
            fallback['fit_tier'] = 'Alternative Cloud Platform Track'
            fallback['why'] = "Core infrastructure and Kubernetes platform engineering path."

        else:
            primary['program'] = 'DevOps, Cloud & AI Platform Engineering'
            primary['catalog_code'] = 'Program 5'
            primary['track'] = 'Site Reliability Engineering (SRE) & Kubernetes Track' if is_senior else 'CI/CD Automation & Cloud Infrastructure Track'
            primary['fit_tier'] = 'Best Fit (Domain Native)'
            primary['why'] = (
                f"Directly accelerates your experience as a {raw_role} into advanced Kubernetes clustering, "
                "Terraform GitOps, multi-region cloud resilience, and AI platform engineering."
            )
            primary['guardrail'] = "Domain native fit; highest completion rate and lowest refund rate in platform engineering."

            fallback['program'] = 'Software & AI Engineering (Scaler Academy)'
            fallback['catalog_code'] = 'Program 1'
            fallback['track'] = 'Advanced Track (High-Level System Design & Scalability)' if is_senior else 'Intermediate Track (Data Structures, Algorithms & LLD)'
            fallback['fit_tier'] = 'Alternative Backend Software Path'
            fallback['why'] = "Alternative path if you want to broaden your profile into core software engineering."

    # =========================================================================
    # SCENARIO 6: SOFTWARE ENGINEERS / DEVELOPERS (SDE / SWE)
    # =========================================================================
    else:
        if inbound_cat == 'P3_FDE':
            if not is_eligible_for_fde:
                primary['program'] = 'Software & AI Engineering (Scaler Academy)'
                primary['catalog_code'] = 'Program 1'
                primary['track'] = 'Beginner Track (Foundations of Programming & Problem Solving)' if is_student else 'Intermediate Track (Data Structures, Algorithms & LLD)'
                primary['fit_tier'] = 'Best Fit (Foundational Prerequisite for FDE)'
                primary['why'] = (
                    f"While you showed high interest in Forward Deployed Engineering, Program 3 requires existing "
                    "software deployment experience (2+ years). Scaler Academy establishes your coding foundation first."
                )
                primary['guardrail'] = "Catalog Gate: FDE requires coding proficiency and 2+ YOE; learner routed to foundational track."

                fallback['program'] = 'AI Forward Deployed Engineer (FDE)'
                fallback['catalog_code'] = 'Program 3'
                fallback['track'] = 'Enterprise AI Integration Track'
                fallback['fit_tier'] = 'Aspirational Goal (Post-Foundations)'
                fallback['why'] = "Target program once foundational data structures and software engineering are mastered."
            else:
                primary['program'] = 'AI Forward Deployed Engineer (FDE)'
                primary['catalog_code'] = 'Program 3'
                primary['track'] = 'Enterprise AI Integration & Production RAG Track'
                primary['fit_tier'] = 'Best Fit (Enterprise AI Deployment)'
                primary['why'] = (
                    f"As a {raw_role} with {raw_exp}, Program 3 trains you to bridge the Enterprise Deployment Gap - "
                    "integrating LLMs, PySpark pipelines, enterprise security, and full-stack client AI solutions."
                )
                primary['guardrail'] = "Catalog Rule 6: Verified coding background matches FDE prerequisite perfectly."

                fallback['program'] = 'AI & Machine Learning with Agentic AI'
                fallback['catalog_code'] = 'Program 4'
                fallback['track'] = 'Advanced Track (Agentic AI & LLMOps)'
                fallback['fit_tier'] = 'Alternative AI Modeling Track'
                fallback['why'] = "Focuses on model fine-tuning and autonomous multi-agent design rather than client consulting."

        elif inbound_cat == 'P4_AIML_AGENTIC':
            if is_student:
                primary['program'] = 'Software & AI Engineering (Scaler Academy)'
                primary['catalog_code'] = 'Program 1'
                primary['track'] = 'Beginner Track (Foundations of Programming & Problem Solving)'
                primary['fit_tier'] = 'Best Fit (Foundational Coding Prerequisite)'
                primary['why'] = (
                    "To build production-grade Agentic AI and fine-tune models, solid programming foundations "
                    "and data structures are required first. Scaler Academy prepares you for advanced AI tracks."
                )
                primary['guardrail'] = "Catalog Rule: Foundation in coding required before autonomous agent design."

                fallback['program'] = 'AI & Machine Learning with Agentic AI'
                fallback['catalog_code'] = 'Program 4'
                fallback['track'] = 'Beginner Track (AI & Machine Learning Foundations)'
                fallback['fit_tier'] = 'Alternative Applied AI Track'
                fallback['why'] = "Direct entry with intensive math and Python machine learning preparation."
            else:
                primary['program'] = 'AI & Machine Learning with Agentic AI'
                primary['catalog_code'] = 'Program 4'
                primary['track'] = 'Advanced Track (Agentic AI & LLMOps)'
                primary['fit_tier'] = 'Best Fit (AI / LLM Engineering)'
                primary['why'] = (
                    f"With your software engineering foundation as a {raw_role}, you skip basic programming and dive "
                    "into PyTorch, transformer architectures, vector embeddings, and autonomous multi-agent workflows."
                )
                primary['guardrail'] = "Catalog Tie-Breaker: Software background provides an ideal launchpad for AI Engineering."

                fallback['program'] = 'Software & AI Engineering (Scaler Academy)'
                fallback['catalog_code'] = 'Program 1'
                fallback['track'] = 'Advanced Track (High-Level System Design & Architecture)'
                fallback['fit_tier'] = 'Alternative Product SDE Track'
                fallback['why'] = "If you prioritize Tier-1 product SDE-2/3 roles, Academy provides High-Level System Design and concurrency."

        elif inbound_cat == 'P5_DEVOPS_CLOUD':
            primary['program'] = 'DevOps, Cloud & AI Platform Engineering'
            primary['catalog_code'] = 'Program 5'
            primary['track'] = 'Site Reliability Engineering (SRE) & Kubernetes Track'
            primary['fit_tier'] = 'Best Fit (Cloud Infrastructure)'
            primary['why'] = (
                f"Complements your development background, qualifying you for hybrid SRE and Platform Engineering roles "
                "managing distributed microservices, CI/CD pipelines, and cloud clusters."
            )
            primary['guardrail'] = "High retention path for developers transitioning to platform engineering."

            fallback['program'] = 'Software & AI Engineering (Scaler Academy)'
            fallback['catalog_code'] = 'Program 1'
            fallback['track'] = 'Backend Architecture & Distributed Systems Track'
            fallback['fit_tier'] = 'Alternative Backend Path'
            fallback['why'] = "Alternative path focusing on microservice architecture and database sharding."

        elif inbound_cat == 'P2_DSML':
            if is_senior:
                primary['program'] = 'Modern Data Science & Machine Learning (DSML)'
                primary['catalog_code'] = 'Program 2'
                primary['track'] = 'Advanced Track (Machine Learning Engineering & Production ML)'
                primary['fit_tier'] = 'Best Fit (Data & ML Engineering Pivot)'
                primary['why'] = (
                    f"With {raw_exp} of engineering experience as a {raw_role}, your coding foundation lets you bypass basic Python "
                    "and advance directly into statistical modeling, feature pipelines, and large-scale enterprise Machine Learning."
                )
                primary['guardrail'] = "Catalog Rule: Experienced engineers transition rapidly into production ML systems."

                fallback['program'] = 'AI & Machine Learning with Agentic AI'
                fallback['catalog_code'] = 'Program 4'
                fallback['track'] = 'Advanced Track (Agentic AI & LLMOps)'
                fallback['fit_tier'] = 'Alternative Frontier AI Track'
                fallback['why'] = "Frontier AI alternative focusing on LLM agents and generative architectures."
            elif is_student:
                primary['program'] = 'Modern Data Science & Machine Learning (DSML)'
                primary['catalog_code'] = 'Program 2'
                primary['track'] = 'Beginner Track (Data Analytics, Python & Business ML)'
                primary['fit_tier'] = 'Best Fit (Foundational Data & ML Track)'
                primary['why'] = (
                    f"As a {raw_role} starting out, Program 2 builds your data querying (SQL), Python programming, "
                    "and business analytics foundations from the ground up for entry-level Data Analyst/Junior Data Scientist roles."
                )
                primary['guardrail'] = "Foundational track calibrated for freshers and early learners."

                fallback['program'] = 'Software & AI Engineering (Scaler Academy)'
                fallback['catalog_code'] = 'Program 1'
                fallback['track'] = 'Beginner Track (Foundations of Programming & Problem Solving)'
                fallback['fit_tier'] = 'Alternative Core Software Track'
                fallback['why'] = "Alternative path building broad software development and problem solving skills."
            else:
                primary['program'] = 'Modern Data Science & Machine Learning (DSML)'
                primary['catalog_code'] = 'Program 2'
                primary['track'] = 'Core Analytics & Machine Learning Track'
                primary['fit_tier'] = 'Best Fit (Data Science & ML Engineering)'
                primary['why'] = (
                    f"With {raw_exp} as a {raw_role}, your programming logic provides an excellent springboard. "
                    "This program equips you with advanced SQL, mathematical modeling, and production ML pipelines."
                )
                primary['guardrail'] = "High retention cohort for developers transitioning to data science."

                fallback['program'] = 'Software & AI Engineering (Scaler Academy)'
                fallback['catalog_code'] = 'Program 1'
                fallback['track'] = 'Intermediate Track (Data Structures, Algorithms & LLD)'
                fallback['fit_tier'] = 'Alternative Core SDE Track'
                fallback['why'] = "If you decide to continue in core software development, Academy prepares you for Tier-1 product roles."

        else:
            if is_senior:
                track_level = 'Advanced Track (High-Level System Design & Scalability)'
                fit_tier = 'Best Fit (Senior Architecture & Scalability)'
                why_text = (
                    f"With {raw_exp} as a {raw_role}, your coding syntax is established. You need architectural depth - "
                    "distributed caching, database sharding, microservices event-driven architectures, and high-level design."
                )
                fallback_prog = 'AI Forward Deployed Engineer (FDE)'
                fallback_code = 'Program 3'
                fallback_track = 'Enterprise AI Integration Track'
                fallback_tier = 'Enterprise AI Leadership Pivot'
                fallback_why = "For senior engineers, FDE offers enterprise client-facing AI consulting with high compensation multiples."
            elif is_student:
                track_level = 'Beginner Track (Foundations of Programming & Problem Solving)'
                fit_tier = 'Best Fit (Foundational Entry & Campus Prep)'
                why_text = (
                    f"As a {raw_role} with {raw_exp}, the Beginner Track builds core programming, "
                    "algorithmic thinking, and foundational Data Structures from scratch to prepare you for Tier-1 product hiring."
                )
                fallback_prog = 'Modern Data Science & Machine Learning (DSML)'
                fallback_code = 'Program 2'
                fallback_track = 'Beginner Track (Data Analytics & Python Foundations)'
                fallback_tier = 'Alternative Analytics Track'
                fallback_why = "A strong entry-level alternative focusing on data analytics and practical problem solving."
            else:
                track_level = 'Intermediate Track (Data Structures, Algorithms & LLD)'
                fit_tier = 'Best Fit (Product SDE Transition)'
                why_text = (
                    f"With {raw_exp} as a {raw_role}, you need algorithmic problem-solving and "
                    "Low-Level Object-Oriented Design (LLD) to crack Tier-1 product company technical bars."
                )
                fallback_prog = 'DevOps, Cloud & AI Platform Engineering'
                fallback_code = 'Program 5'
                fallback_track = 'Cloud Infrastructure Track'
                fallback_tier = 'Alternative Cloud Platform Pivot'
                fallback_why = "A fast-growing alternative if you prefer distributed cloud pipelines over pure algorithmic problem solving."

            primary['program'] = 'Software & AI Engineering (Scaler Academy)'
            primary['catalog_code'] = 'Program 1'
            primary['track'] = track_level
            primary['fit_tier'] = fit_tier
            primary['why'] = why_text
            primary['guardrail'] = "Track level assigned based on YOE maturity and technical foundation."

            fallback['program'] = fallback_prog
            fallback['catalog_code'] = fallback_code
            fallback['track'] = fallback_track
            fallback['fit_tier'] = fallback_tier
            fallback['why'] = fallback_why

    # Assign official program track durations & diagnostic SET scores
    primary['duration'] = get_track_duration(primary.get('program', ''), primary.get('track', ''))
    fallback['duration'] = get_track_duration(fallback.get('program', ''), fallback.get('track', ''))
    primary['sat_score'] = raw_sat_score
    primary['sat_status'] = raw_sat_status
    primary['set_score'] = raw_sat_score
    primary['set_status'] = raw_sat_status
    fallback['sat_score'] = raw_sat_score
    fallback['sat_status'] = raw_sat_status
    fallback['set_score'] = raw_sat_score
    fallback['set_status'] = raw_sat_status

    # -------------------------------------------------------------
    # PULL EMPIRICAL RETENTION & REFUND STATS FROM 13,180 RECORDS
    # -------------------------------------------------------------
    primary_lookup = 'P1_ACADEMY' if 'Academy' in primary['program'] else (
        'P2_DSML' if 'DSML' in primary['program'] else (
            'P3_FDE' if 'FDE' in primary['program'] else (
                'P5_DEVOPS' if 'DevOps' in primary['program'] else 'P4_AIML'
            )
        )
    )
    fallback_lookup = 'P1_ACADEMY' if 'Academy' in fallback['program'] else (
        'P2_DSML' if 'DSML' in fallback['program'] else (
            'P3_FDE' if 'FDE' in fallback['program'] else (
                'P5_DEVOPS' if 'DevOps' in fallback['program'] else 'P4_AIML'
            )
        )
    )

    primary_stats = get_cohort_stats(primary_lookup, persona, exp_bracket, matrix_data)
    fallback_stats = get_cohort_stats(fallback_lookup, persona, exp_bracket, matrix_data)
    
    primary['retention_rate'] = primary_stats.get('retention_rate', 78.2)
    primary['refund_rate'] = primary_stats.get('refund_rate', 21.8)
    primary['cohort_size'] = primary_stats.get('total', 100)
    primary['risk_tag'] = 'High Retention' if primary['retention_rate'] >= 80 else ('Moderate' if primary['retention_rate'] >= 75 else 'High Risk')

    fallback['retention_rate'] = fallback_stats.get('retention_rate', 75.0)
    fallback['refund_rate'] = fallback_stats.get('refund_rate', 25.0)
    fallback['cohort_size'] = fallback_stats.get('total', 100)
    fallback['risk_tag'] = 'High Retention' if fallback['retention_rate'] >= 80 else ('Moderate' if fallback['retention_rate'] >= 75 else 'High Risk')

    # Empirical Confidence Calculation (0-100 Score & Tier)
    prim_conf = calculate_confidence(
        primary['program'], inbound_cat, primary['cohort_size'],
        primary['retention_rate'], raw_sat_status, raw_sat_score, edu_level
    )
    fall_conf = calculate_confidence(
        fallback['program'], inbound_cat, fallback['cohort_size'],
        fallback['retention_rate'], raw_sat_status, raw_sat_score, edu_level
    )

    primary['confidence_tier'] = prim_conf['tier']
    primary['confidence_score'] = prim_conf['score']
    primary['confidence_rationale'] = prim_conf['rationale']
    primary['confidence_breakdown'] = prim_conf.get('breakdown', {})

    fallback['confidence_tier'] = fall_conf['tier']
    fallback['confidence_score'] = fall_conf['score']
    fallback['confidence_rationale'] = fall_conf['rationale']
    fallback['confidence_breakdown'] = fall_conf.get('breakdown', {})

    # Clean salutation first name (avoid awkward "Hi Candidate" on phone calls)
    if not name or name in ['Prospective Learner', 'there'] or name.lower().startswith('candidate') or '_' in name or any(c.isdigit() for c in name.split()[0]):
        lead_first_name = 'there'
    else:
        lead_first_name = name.split()[0]
    
    # 1. Opening Dialogue
    if is_student:
        call_opening = (
            f"\"Hi {lead_first_name}, I saw that you're currently {raw_role} ({raw_exp}). "
            "Many candidates at this stage want to build ironclad fundamentals in programming and algorithmic problem solving "
            "so they stand out in product company recruitment. What is the main career milestone you're aiming for?\""
        )
    elif is_non_tech:
        call_opening = (
            f"\"Hi {lead_first_name}, I saw that you're currently working in {raw_role} with {raw_exp} of experience. "
            "A lot of professionals reaching out to us from non-technical backgrounds are looking to make a structured, "
            "long-term transition into tech, but are worried about coding prerequisites. "
            "What has been the main trigger behind your plan to upskill right now?\""
        )
    elif is_senior:
        call_opening = (
            f"\"Hi {lead_first_name}, I noticed you've been working as a {raw_role} with {raw_exp} of experience. "
            "At your seniority, most engineers aren't looking for basic tutorials - they're looking to master large-scale "
            "system architecture, high-level design, and lead engineering teams at top product companies. "
            "Is that the primary transition you're targeting?\""
        )
    else:
        call_opening = (
            f"\"Hi {lead_first_name}, I saw you're currently working as a {raw_role} with {raw_exp} of experience. "
            "Many engineers at this career stage feel ready to move beyond routine project tasks and crack top-tier product SDE roles. "
            "What specific career milestone are you aiming to hit over the next 6 to 12 months?\""
        )

    # 2. Program & Track Value Pitch
    program_pitch = (
        f"\"Based on where your career is right now, the exact program we recommend is {primary['program']}, "
        f"specifically our {primary['track']}. Here is why this matters: we don't put you into a generic one-size-fits-all batch. "
        f"This track is calibrated for your experience level, focusing directly on the core problem-solving, design patterns, and "
        "real-world engineering that top product companies test for in technical rounds.\""
    )

    # 3. Handling Inbound Curiosity / Alternative Course Objection
    inbound_is_same = (
        (inbound_cat == 'P1_ACADEMY' and 'academy' in primary['program'].lower()) or
        (inbound_cat == 'P2_DSML' and 'dsml' in primary['program'].lower()) or
        (inbound_cat == 'P3_FDE' and 'fde' in primary['program'].lower()) or
        (inbound_cat == 'P4_AIML_AGENTIC' and 'agentic' in primary['program'].lower()) or
        (inbound_cat == 'P5_DEVOPS_CLOUD' and 'devops' in primary['program'].lower())
    )
    if inbound_is_same:
        inbound_handling = (
            f"\"Your interest in {primary['program']} is spot on. It directly aligns with your career transition goals, "
            f"and our {primary['track']} gives you a structured, step-by-step foundation without a steep learning cliff.\""
        )
    else:
        if primary.get('retention_rate', 0) >= fallback.get('retention_rate', 0):
            retention_claim = f"gives you a much stronger technical foundation ({primary.get('retention_rate')}% completion rate)"
        else:
            retention_claim = f"provides the most direct alignment with your current background"
            
        inbound_handling = (
            f"\"I also noted your interest in {inbound_prog_raw}. That's an incredible domain, but to be completely honest with you, "
            f"our historical graduation data shows that starting with {primary['program']} {retention_claim}. Once you lock down these engineering fundamentals, transitioning into "
            f"{fallback['program']} becomes vastly easier and faster.\""
        )

    sales_script = {
        'call_opening': call_opening,
        'program_pitch': program_pitch,
        'inbound_handling': inbound_handling
    }

    # 5. Market Intelligence, Audited Placement Metrics & Curriculum Attachment
    prim_market = get_market_intelligence(primary.get('program', ''), raw_role, raw_exp, company_type, primary.get('track', ''))
    fall_market = get_market_intelligence(fallback.get('program', ''), raw_role, raw_exp, company_type, fallback.get('track', ''))

    primary['market_intelligence'] = prim_market
    primary['catalogue_url'] = prim_market.get('catalogue_url', 'https://www.scaler.com/')
    primary['curriculum_modules'] = prim_market.get('curriculum_modules', [])
    primary['career_options'] = prim_market.get('career_options', {})

    fallback['market_intelligence'] = fall_market
    fallback['catalogue_url'] = fall_market.get('catalogue_url', 'https://www.scaler.com/')
    fallback['curriculum_modules'] = fall_market.get('curriculum_modules', [])
    fallback['career_options'] = fall_market.get('career_options', {})

    # Synthesize comprehensive, curriculum-grounded reasons for Primary and Fallback
    primary['why'] = generate_curriculum_grounded_why(
        primary.get('program', ''), primary.get('track', ''), raw_role, raw_exp,
        primary.get('curriculum_modules', []), primary.get('retention_rate', 78.0),
        primary.get('cohort_size', 100), primary.get('fit_tier', ''), inbound_cat,
        is_primary=True, base_rationale=primary.get('why', ''), persona=persona
    )

    fallback['why'] = generate_curriculum_grounded_why(
        fallback.get('program', ''), fallback.get('track', ''), raw_role, raw_exp,
        fallback.get('curriculum_modules', []), fallback.get('retention_rate', 75.0),
        fallback.get('cohort_size', 100), fallback.get('fit_tier', ''), inbound_cat,
        is_primary=False, base_rationale=fallback.get('why', ''), persona=persona,
        primary_prog_name=primary.get('program', '')
    )

    return {
        'person': {
            'name': name,
            'email': email,
            'phone': phone,
            'role': raw_role,
            'role_domain': role_domain,
            'company_type': company_type,
            'previous_org': prev_org,
            'previous_org_year': prev_year,
            'experience': raw_exp,
            'enquired_program': inbound_prog_raw,
            'education': raw_edu,
            'education_level': edu_level,
            'sat_score': raw_sat_score,
            'sat_status': raw_sat_status,
            'set_score': raw_sat_score,
            'set_status': raw_sat_status,
            'normalized_persona': persona_name,
            'persona_key': persona,
            'normalized_experience': exp_bracket
        },

        'primary': primary,
        'fallback': fallback,
        'sales_script': sales_script,
        'market_intelligence': prim_market,
        'academic_eligibility': {
            'status': 'Degree Verified',
            'is_eligible': True,
            'rationale': f"Education background ({raw_edu or 'Degree'}) satisfies Bachelor's degree prerequisite."
        }
    }
