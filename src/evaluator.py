import os
import json
import re
from .matrix_engine import get_cohort_stats, normalize_persona, normalize_experience, normalize_program
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
    
    # Program 1: Scaler Academy
    if 'academy' in p_lower or 'program 1' in p_lower:
        if 'beginner' in t_lower:
            return '12 - 18 Months'
        elif 'intermediate' in t_lower:
            return '12 Months'
        elif 'advanced' in t_lower:
            return '10 - 17 Months'
        return '12 Months'
        
    # Program 2: DSML
    elif 'dsml' in p_lower or 'data science' in p_lower or 'program 2' in p_lower:
        if 'beginner' in t_lower:
            return '14 - 21.5 Months'
        elif 'intermediate' in t_lower or 'core' in t_lower or 'predictive' in t_lower:
            return '11.5 Months'
        return '11.5 - 14 Months'
        
    # Program 3: AI Forward Deployed Engineer (FDE)
    elif 'fde' in p_lower or 'forward deployed' in p_lower or 'program 3' in p_lower:
        return '12 - 16 Months'
        
    # Program 4: AI & ML with Agentic AI
    elif 'agentic' in p_lower or 'program 4' in p_lower or 'aiml' in p_lower:
        if 'beginner' in t_lower or 'foundation' in t_lower:
            return '14 - 18 Months'
        return '11 - 15 Months'
        
    # Program 5: DevOps, Cloud & AI Platform Engineering
    elif 'devops' in p_lower or 'cloud' in p_lower or 'platform' in p_lower or 'program 5' in p_lower:
        return '14 - 18 Months'
        
    return '12 Months'

def classify_education(education_str):
    if not education_str:
        return 'GRAD_UNKNOWN'
    edu = str(education_str).lower().strip()
    if edu in ['nan', 'none', 'null', '', '-', 'unknown']:
        return 'GRAD_UNKNOWN'
    
    # 1. Below Graduation (10th, 12th, Diploma, Polytechnic)
    if any(k in edu for k in [
        '10th', '12th', 'hsc', 'ssc', 'intermediate', '10+2', '12 pass', '10 pass',
        'matric', 'polytechnic', 'diploma', 'iti', 'below graduation', 'high school',
        'puc', 'higher secondary'
    ]):
        return 'BELOW_GRAD'
        
    # 2. Computer Science / Technical Degrees
    if any(k in edu for k in [
        'b.tech cs', 'b.tech cse', 'b.tech it', 'be cs', 'be cse', 'be it',
        'bca', 'mca', 'm.tech cs', 'm.tech cse', 'm.tech it', 'computer science',
        'information tech', 'software eng'
    ]):
        return 'GRAD_CS'
        
    # 3. Non-CS Degrees
    if any(k in edu for k in [
        'b.com', 'b.a', 'bba', 'bhm', 'b.des', 'llb', 'mbbs', 'b.pharm',
        'mechanical', 'civil', 'chemical', 'electrical', 'biotech', 'arts',
        'commerce', 'humanities'
    ]):
        return 'GRAD_NON_CS'
        
    # 4. General Engineering / Graduate
    if any(k in edu for k in ['b.tech', 'b.e', 'be ', 'btech', 'b.sc', 'm.sc', 'mba', 'm.tech', 'graduate', 'degree', 'engineering']):
        return 'GRAD_GENERAL'
        
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
        apt_desc = "degree verified, SAT pending"
    else:
        apt_pts = 5
        apt_desc = "diagnostic SAT not yet attempted"

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


def generate_curriculum_grounded_why(
    program_name, track_name, raw_role, raw_exp, modules,
    retention_rate, cohort_size, fit_tier, inbound_cat,
    is_primary=True, base_rationale="", persona=""
):
    """
    Synthesizes a comprehensive, curriculum-grounded explanation for 'Why This Program'
    or 'Why Fallback', combining:
    1. The specific curriculum modules and technical milestones of the assigned track.
    2. The candidate's background, current role, and years of experience.
    3. Historical retention, completion rates, and dropout prevention guardrails.
    """
    p_lower = str(program_name).lower()
    t_lower = str(track_name).lower()
    
    # Extract top module phases from loaded curriculum modules
    module_names = []
    if modules and isinstance(modules, list):
        for m in modules[:5]:
            p = m.get('phase', '')
            if p and p not in module_names:
                module_names.append(p)
    module_text = ", ".join(f"<i>{h}</i>" for h in module_names[:3]) if module_names else "core engineering and production milestones"

    # 1. Scaler Academy (Program 1)
    if 'academy' in p_lower or 'software' in p_lower:
        if 'beginner' in t_lower or 'foundations' in t_lower:
            content_desc = (
                "Features foundational modules starting with <i>Programming Fundamentals - Thinking with AI (Logics, Loops & Control Flow)</i>, "
                "<i>Intermediate DSA (Prefix Sum, Bit Manipulation, 2D Matrices)</i>, and <i>AI & Agents: From Talking to AI to Building One</i>, "
                "before advancing into <i>Advanced DSA</i> (Linear/Non-Linear Structures, Trees, Dynamic Programming, Graphs) and <i>System Design</i>."
            )
            career_desc = (
                f"As a {raw_role} with {raw_exp}, building systematic computational thinking and problem-solving habits from ground zero "
                "is the single most decisive factor for cracking Tier-1 product company recruitment."
            )
            historical_desc = (
                f"Backed by an audited <b>{retention_rate}% completion rate</b> across {cohort_size}+ early-career and non-CS learners. "
                "Historical cohort analytics demonstrate that beginners placed directly into intermediate algorithms face an elevated Day-14 "
                "pacing dropout; this structured ramp-up provides the scaffolding necessary for long-term retention."
            )
        elif 'intermediate' in t_lower or 'dsa' in t_lower:
            content_desc = (
                "Bypasses basic syntax to focus directly on <i>Intermediate DSA : AI Assisted Problem Solving</i>, "
                "<i>Advanced DSA (Divide & Conquer, Trees, Heaps, Graphs, Dynamic Programming)</i>, and <i>Low-Level Object-Oriented Design (LLD)</i>, "
                "with an elective bridge into <i>Distributed High-Level System Design</i>."
            )
            career_desc = (
                f"Calibrated for engineers working as {raw_role} with {raw_exp}. You don't need basic loop syntax - you need "
                "interview-tested algorithmic optimization patterns and clean design principles to transition from service tasks to Tier-1 product SDE roles."
            )
            historical_desc = (
                f"Supported by an empirical <b>{retention_rate}% completion rate</b> across {cohort_size}+ working technical professionals. "
                "Historical graduation data confirms this track maximizes interview-readiness within 12 months while respecting full-time working hours."
            )
        else: # Advanced
            content_desc = (
                "Centers on architectural scale and engineering leadership: <i>High-Level Distributed System Design & Scalability</i> "
                "(Kafka event streaming, consistent hashing, caching at scale, database sharding, CAP/PACELC theorems) and <i>Concurrent Backend Microservices</i>."
            )
            career_desc = (
                f"Tailored for senior engineers with {raw_exp} as a {raw_role}. Eliminates elementary coding tutorials to focus 100% on "
                "large-scale distributed architecture, trade-off analysis, and executive technical communication."
            )
            historical_desc = (
                f"Demonstrates an elite <b>{retention_rate}% completion rate</b> across senior cohorts. Historical retention shows that "
                "senior candidates thrive when curriculum focuses on system-level architecture rather than repetitive syntax drills."
            )

    # 2. Modern Data Science & ML (Program 2)
    elif 'dsml' in p_lower or 'data science' in p_lower:
        if 'beginner' in t_lower or 'analytics' in t_lower:
            content_desc = (
                "Begins with <i>Advanced SQL & AI for Data Professionals</i>, <i>Excel & Dashboarding with AI Storytelling</i>, "
                "<i>Python Foundations + AI Coding Assistants</i>, and <i>Product Analytics with AI</i>, seamlessly progressing into "
                "<i>Supervised Machine Learning with AI Workflows</i>."
            )
            career_desc = (
                f"For a {raw_role} with {raw_exp}, learning data analytics through business metrics and SQL dashboards leverages your existing "
                "domain intuition directly into tech without wrestling with abstract software engineering."
            )
            historical_desc = (
                f"Proven by a <b>{retention_rate}% completion rate</b> across {cohort_size}+ learners. Historical cohort data reveals "
                "this progressive ramp-up achieves the highest retention of any career pivot, virtually eliminating refund risk."
            )
        else: # Intermediate / Core ML
            content_desc = (
                "Dives directly into <i>Advanced Analytics with Python & Pandas</i>, <i>Statistics & Experimentation for AI (A/B Testing Frameworks)</i>, "
                "<i>Supervised & Unsupervised Machine Learning</i>, <i>Deep Learning & Neural Networks</i>, and <i>Production MLOps on AWS</i>."
            )
            career_desc = (
                f"Elevates your experience as a {raw_role} ({raw_exp}) from descriptive reporting into statistical hypothesis testing, "
                "predictive modeling, and enterprise AI production pipelines."
            )
            historical_desc = (
                f"Validated by an audited <b>{retention_rate}% completion rate</b> across quantitative cohorts. Historical data confirms "
                "analysts transitioning through applied predictive modeling experience rapid career acceleration into senior ML titles."
            )

    # 3. AI Forward Deployed Engineer (Program 3)
    elif 'fde' in p_lower or 'forward deployed' in p_lower:
        content_desc = (
            "Delivered entirely through enterprise client simulation (<i>Meridian Platform</i>), covering <i>The Ingestion Pipeline (Production Python)</i>, "
            "<i>Production RAG for Customer Support</i>, <i>Autonomous Agents & Enterprise Integration (LangGraph & MCP)</i>, "
            "<i>Docker & Kubernetes Orchestration</i>, and <i>1-Click AWS Production Deployment with Terraform</i>."
        )
        career_desc = (
            f"As a {raw_role} with {raw_exp}, this program bridges the Enterprise Deployment Gap - transforming backend and systems engineers "
            "into high-leverage client-facing AI architects capable of deploying custom LLM systems directly inside Fortune 500 infrastructure."
        )
        historical_desc = (
            f"Supported by an outstanding <b>{retention_rate}% completion rate</b> across software engineering cohorts. Historical placement analytics "
            "indicate that forward-deployed roles command a 2.5x compensation premium over traditional development due to high client demand."
        )

    # 4. AI & Machine Learning with Agentic AI (Program 4)
    elif 'agentic' in p_lower or 'aiml' in p_lower or 'program 4' in p_lower:
        if 'beginner' in t_lower or 'foundation' in t_lower:
            content_desc = (
                "Includes the dedicated 2-Month <i>Generative AI Foundations & LLM Landscape</i> (Prompt Engineering, n8n/Zapier automations, no-code agents, AWS hosting) "
                "and 1-Month <i>Python Programming Fundamentals</i>, before advancing into <i>Data Foundations</i>, <i>Supervised/Unsupervised ML</i>, "
                "<i>MLOps on AWS SageMaker</i>, and <i>LangGraph Agentic Orchestration</i>."
            )
            career_desc = (
                f"Provides a structured, supportive ramp-up for a {raw_role} ({raw_exp}), ensuring solid coding foundations before tackling advanced AI math and neural models."
            )
            historical_desc = (
                f"Enforces Catalog Rule 6: candidates without prior coding exposure face a 25.8% drop-off if pushed directly into tensor math; "
                f"this foundational progression preserves high retention (<b>{retention_rate}% completion rate</b> across {cohort_size}+ learners)."
            )
        else: # Advanced Track
            content_desc = (
                "Bypasses introductory syntax to dive directly into <i>Data Foundations</i>, <i>Applied Deep Learning (OpenCV & Transformers)</i>, "
                "<i>MLOps on AWS SageMaker</i>, <i>Agentic Design Patterns & LangGraph Multi-Agent Orchestration</i>, "
                "<i>Advanced Cognitive Architectures (GraphRAG & Multimodal AI)</i>, and <i>PEFT/LoRA Fine-Tuning served via vLLM</i>."
            )
            career_desc = (
                f"Capitalizes on your engineering foundation as a {raw_role} with {raw_exp}. You skip introductory coding to focus 100% on "
                "model fine-tuning, autonomous agent loops, vector indexing, and token-economic model serving."
            )
            historical_desc = (
                f"Backed by an empirical <b>{retention_rate}% completion rate</b> across technical cohorts. Historical data verifies that "
                "software developers thrive when immersed directly in modern generative AI architectures and scalable LLMOps."
            )

    # 5. DevOps, Cloud & AI Platform Engineering (Program 5)
    elif 'devops' in p_lower or 'cloud' in p_lower or 'platform' in p_lower or 'program 5' in p_lower:
        content_desc = (
            "Systematically covers the entire modern platform stack: <i>Python & Linux Shell Scripting (1 & 2)</i>, "
            "<i>DevOps Tools 1 (Docker, multi-node Kubernetes clustering, Prometheus/Grafana monitoring, Hugging Face model deployment)</i>, "
            "<i>DevOps Tools 2 (GitHub Actions CI/CD, ArgoCD GitOps, Ansible)</i>, and <i>AWS 1 & 2 (EKS, VPC, CloudFormation, Terraform IaC)</i>, "
            "with specialized electives in <i>MLOps & AI Observability</i>."
        )
        career_desc = (
            f"Complements your background as a {raw_role} ({raw_exp}), converting your existing development, testing, or systems experience "
            "into high-availability cloud infrastructure and SRE engineering without requiring competitive algorithmic design."
        )
        historical_desc = (
            f"Demonstrates an elite <b>{retention_rate}% completion rate</b> ({cohort_size}+ cohort). Historical transition data shows that "
            "infrastructure and platform engineering provides the highest retention and lowest refund rate among all technical career transitions."
        )

    # Generic Fallback
    else:
        content_desc = f"Curriculum structured around {module_text}."
        career_desc = f"Calibrated for {raw_role} with {raw_exp} to support long-term technical growth."
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
    name = clean_str(lead_dict.get('name'), 'Prospective Learner')
    email = clean_str(lead_dict.get('email'), 'unspecified@lead.com')
    phone = clean_str(lead_dict.get('phone'), 'N/A')
    raw_role = clean_str(lead_dict.get('role'), 'General Tech Professional')
    company_type = clean_str(lead_dict.get('company type'), 'IT Services / Technology')
    prev_org = clean_str(lead_dict.get('previous org name'), 'Current Company')
    prev_year = clean_str(lead_dict.get('previous org year'), '1-2 years')
    raw_exp = clean_str(lead_dict.get('experience'), '2 years')
    inbound_prog_raw = clean_str(lead_dict.get('program'), 'Academy')
    raw_edu = clean_str(lead_dict.get('education') or lead_dict.get('degree') or lead_dict.get('qualification'), 'Graduated / Degree')
    raw_sat_status = clean_str(lead_dict.get('sat_status'), 'SAT Not Attempted')
    raw_sat_score = clean_str(lead_dict.get('sat_score'), 'Not Attempted')
    
    # Normalized taxonomy & education
    persona = normalize_persona('', raw_role)
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
            'inbound_handling': '"We sincerely appreciate your drive to learn software development. Our honest recommendation is to first complete a formal degree program (such as a BCA, B.Sc, or B.Tech). As you approach your graduation year, we will gladly fast-track your enrollment into our technical cohorts."',
            'commitment_setting': '"Rather than rushing into an enrollment that could lead to career placement hurdles, focus on completing your formal degree foundations. We will keep your profile active and reconnect with you once you are in your graduation year."'
        }
        return {
            'person': {
                'name': name, 'email': email, 'phone': phone, 'role': raw_role,
                'company_type': company_type, 'previous_org': prev_org, 'previous_org_year': prev_year,
                'experience': raw_exp, 'enquired_program': inbound_prog_raw,
                'education': raw_edu, 'education_level': edu_level,
                'sat_score': raw_sat_score, 'sat_status': raw_sat_status,
                'normalized_persona': persona, 'normalized_experience': exp_bracket
            },
            'primary': prim,
            'fallback': fall,
            'sales_script': sales_script
        }

    # Detect inbound program category
    if any(k in inbound_str for k in ['fde', 'forward deployed', 'solutions engineer']):
        inbound_cat = 'P3_FDE'
    elif any(k in inbound_str for k in ['agentic', 'aiml', 'deep learning', 'llm', 'genai']):
        inbound_cat = 'P4_AIML_AGENTIC'
    elif any(k in inbound_str for k in ['dsml', 'data science', 'analytics']):
        inbound_cat = 'P2_DSML'
    elif any(k in inbound_str for k in ['devops', 'cloud', 'platform', 'sre', 'kubernetes']):
        inbound_cat = 'P5_DEVOPS_CLOUD'
    else:
        inbound_cat = 'P1_ACADEMY'

    is_career_break = any(k in raw_role.lower() for k in ['career break', 'break', 'sabbatical', 'gap', 'gap year', 'returning', 'homemaker', 'restart'])
    is_student = (exp_bracket == 'EXP_0_1') or any(k in raw_role.lower() for k in ['student', 'intern', 'learner', 'fresher', 'non coder', 'college'])
    is_non_tech = (
        is_career_break or 
        (edu_level == 'GRAD_NON_CS' and is_student) or 
        (persona in ['NON_TECH', 'Non-Tech / Operations']) or 
        any(k in raw_role.lower() for k in [
            'hr', 'human resource', 'recruiter', 'talent', 'staffing', 'people partner', 'people ops', 'hrbp',
            'marketing', 'seo', 'growth', 'content', 'copywriter', 'branding', 'digital marketing',
            'sales', 'business development', 'bde', 'bda', 'account executive', 'inside sales', 'telecaller',
            'finance', 'accounting', 'accountant', 'auditor', 'taxation', 'banking', 'insurance',
            'operations', 'admin', 'administration', 'consultant', 'legal', 'lawyer', 'procurement', 'logistics', 'supply chain',
            'bpo', 'kpo', 'customer', 'support', 'call center',
            'mechanical', 'civil', 'chemical', 'electrical', 'biotech',
            'non-tech', 'non tech', 'non coder', 'non-coder', 'student', 'learner', 'intern', 'fresher'
        ])
    )
    is_qa = (not is_non_tech) and (persona in ['QA_SDET', 'QA / SDET / Testing'] or any(k in raw_role.lower() for k in ['test', 'qa', 'sdet', 'automation']))
    is_data = (not is_non_tech) and (persona in ['DATA_ANALYST', 'Data & Analytics'] or any(k in raw_role.lower() for k in ['data', 'analyst', 'analytics', 'bi ']))
    is_systems = (not is_non_tech) and (persona in ['SYSTEMS_ENG', 'Systems & Embedded Engineering'] or any(k in raw_role.lower() for k in ['system', 'embedded', 'linux', 'hardware']))
    is_senior = (not is_student) and (not is_non_tech) and (
        exp_bracket in ['EXP_5_PLUS', '5-8 years', '8+ years', '5+ yrs (Senior / Lead)'] or 
        any(k in raw_role.lower() for k in ['lead', 'senior', 'manager', 'leadership', 'director', 'founder', 'architect', 'vp'])
    )

    primary = {}
    fallback = {}

    # =========================================================================
    # SCENARIO 1: NON-TECH / ZERO-CODE (Strict Catalog Gate)
    # =========================================================================
    if is_non_tech:
        # If candidate enquired about DSML, respect their intent: DSML Beginner Track is the #1 natural business transition!
        if inbound_cat == 'P2_DSML':
            primary['program'] = 'Modern Data Science & Machine Learning (DSML)'
            primary['catalog_code'] = 'Program 2'
            primary['track'] = 'Beginner Track (Data Analytics, Python & Business ML)'
            primary['fit_tier'] = 'Best Fit (Applied Business Analytics)'
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
        if inbound_cat == 'P5_DEVOPS_CLOUD':
            primary['program'] = 'DevOps, Cloud & AI Platform Engineering'
            primary['catalog_code'] = 'Program 5'
            primary['track'] = 'CI/CD Automation & Cloud Infrastructure Track'
            primary['fit_tier'] = 'Best Fit (Natural Synergistic Pivot)'
            primary['why'] = (
                f"Your automation testing background as a {raw_role} connects seamlessly into DevOps - "
                "expanding test automation suites into CI/CD pipelines, Docker containers, and Kubernetes orchestration."
            )
            primary['guardrail'] = "Catalog Tie-Breaker: Test automation skill naturally bridges to SRE & Cloud Engineering."

            fallback['program'] = 'Software & AI Engineering (Scaler Academy)'
            fallback['catalog_code'] = 'Program 1'
            fallback['track'] = 'Intermediate Track (Backend SDE Transition)'
            fallback['fit_tier'] = 'Alternative Core SDE'
            fallback['why'] = "If you prefer transitioning into core development, Academy focuses on Object-Oriented Design and DSA."
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
            fallback['track'] = 'Cloud Platform & Infrastructure Track'
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
        elif inbound_cat == 'P3_FDE' and not is_non_tech:
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
            fallback['track'] = 'Cloud Platform Track'
            fallback['fit_tier'] = 'Alternative Infrastructure Track'
            fallback['why'] = "Infrastructure alternative focusing on Kubernetes and platform scalability."
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
    # SCENARIO 5: SOFTWARE ENGINEERS / DEVELOPERS (SDE / SWE)
    # =========================================================================
    else:
        if inbound_cat == 'P3_FDE':
            if is_student:
                primary['program'] = 'Software & AI Engineering (Scaler Academy)'
                primary['catalog_code'] = 'Program 1'
                primary['track'] = 'Beginner Track (Foundations of Programming & Problem Solving)'
                primary['fit_tier'] = 'Best Fit (Foundational Prerequisite for FDE)'
                primary['why'] = (
                    f"While you showed high interest in Forward Deployed Engineering, Program 3 requires existing "
                    "software deployment experience. Scaler Academy's Beginner Track establishes your coding foundation first."
                )
                primary['guardrail'] = "Catalog Gate: FDE requires coding proficiency; learner routed to foundational track."

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

    # Assign official program track durations & diagnostic SAT scores
    primary['duration'] = get_track_duration(primary.get('program', ''), primary.get('track', ''))
    fallback['duration'] = get_track_duration(fallback.get('program', ''), fallback.get('track', ''))
    primary['sat_score'] = raw_sat_score
    primary['sat_status'] = raw_sat_status
    fallback['sat_score'] = raw_sat_score
    fallback['sat_status'] = raw_sat_status

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
        inbound_handling = (
            f"\"I also noted your interest in {inbound_prog_raw}. That's an incredible domain, but to be completely honest with you, "
            f"our historical graduation data shows that starting with {primary['program']} gives you a much stronger technical foundation "
            f"({primary['retention_rate']}% completion rate). Once you lock down these engineering fundamentals, transitioning into "
            f"{fallback['program']} becomes vastly easier and faster.\""
        )

    # 4. Expectation & Commitment Setting (Retention Safeguard)
    commitment_setting = (
        "\"To be completely transparent with you, this is an intensive, high-impact curriculum. "
        "It requires a consistent commitment of 12 to 15 hours per week. Completing the initial onboarding assessment and staying "
        "disciplined with live sessions is the key difference between learners who struggle and those who successfully transition. "
        "If you can commit that time, our mentors and teaching assistants will support you through every assignment.\""
    )

    sales_script = {
        'call_opening': call_opening,
        'program_pitch': program_pitch,
        'inbound_handling': inbound_handling,
        'commitment_setting': commitment_setting
    }

    # 5. Market Intelligence, Audited Placement Metrics & Curriculum Attachment
    prim_market = get_market_intelligence(primary.get('program', ''), raw_role, raw_exp, company_type, primary.get('track', ''))
    fall_market = get_market_intelligence(fallback.get('program', ''), raw_role, raw_exp, company_type, fallback.get('track', ''))

    primary['market_intelligence'] = prim_market
    primary['catalogue_url'] = prim_market.get('catalogue_url', 'https://www.scaler.com/')
    primary['curriculum_modules'] = prim_market.get('curriculum_modules', [])

    fallback['market_intelligence'] = fall_market
    fallback['catalogue_url'] = fall_market.get('catalogue_url', 'https://www.scaler.com/')
    fallback['curriculum_modules'] = fall_market.get('curriculum_modules', [])

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
        is_primary=False, base_rationale=fallback.get('why', ''), persona=persona
    )

    return {
        'person': {
            'name': name,
            'email': email,
            'phone': phone,
            'role': raw_role,
            'company_type': company_type,
            'previous_org': prev_org,
            'previous_org_year': prev_year,
            'experience': raw_exp,
            'enquired_program': inbound_prog_raw,
            'education': raw_edu,
            'education_level': edu_level,
            'sat_score': raw_sat_score,
            'sat_status': raw_sat_status,
            'normalized_persona': persona,
            'normalized_experience': exp_bracket
        },
        'primary': primary,
        'fallback': fallback,
        'sales_script': sales_script,
        'market_intelligence': prim_market
    }
