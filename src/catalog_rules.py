# ==============================================================================
# OFFICIAL SCALER 5-PROGRAM CATALOG KNOWLEDGE BASE
# Extracted directly from: Documentation_Scaler_Updated.pdf (Pages 1 - 20)
# ==============================================================================

SCALER_CATALOG = {
    "Program 1": {
        "code": "Program 1",
        "name": "Software & AI Engineering Program (Scaler Academy)",
        "short_name": "Scaler Academy",
        "pages": "1 - 4",
        "core_mission": "Bridges the modern 'AI-Blindspot' and 'Floor vs. Ceiling' disconnect in software engineering. Equips engineers to write production-grade code, architect scalable systems, and build AI-augmented applications.",
        "tracks": {
            "Beginner Track": {
                "name": "Beginner Track (Foundations of Programming)",
                "prerequisites": "No prior coding experience required. Starts from absolute ground zero (variables, loops, conditional statements, basic algorithms).",
                "recommended_for": "Non-Tech, Career Switchers, Operations, Mechanical/Civil, Freshers with 0 coding."
            },
            "Intermediate Track": {
                "name": "Intermediate Track (Data Structures, Algorithms & LLD)",
                "prerequisites": "Basic syntax familiarity in Java, C++, Python, or JavaScript.",
                "recommended_for": "QA/SDET, Systems Engineers, IT Service maintenance engineers (TCS/Cognizant/Wipro) with 1-4 YOE."
            },
            "Advanced Track": {
                "name": "Advanced Track (High-Level System Design, Concurrency & Scalability)",
                "prerequisites": "Strong DSA background and verified professional software engineering exposure (>= 1 year SDE).",
                "recommended_for": "Experienced SDEs (3+ YOE) seeking Tier-1 product SDE-2/3 roles."
            }
        },
        "negative_filters": [
            "Never pitch the Advanced Track to leads with zero coding experience or fewer than 1 year of professional technical exposure.",
            "Do not pitch to leads solely seeking pure business dashboarding or statistical reporting without coding (route to Program 2)."
        ],
        "target_titles": [
            "Software Development Engineer (SDE-1, SDE-2, SDE-3)",
            "Backend Engineer",
            "Full-Stack Developer",
            "Tech Lead / Engineering Manager"
        ],
        "tie_breaker_rules": {
            "vs_Program_2": "Route to Program 1 if career objective is building scalable software applications, backend microservices, or fullstack web systems. Route to Program 2 (DSML) if primary focus is analyzing data or building predictive models.",
            "vs_Program_4": "Route to Program 1 if lead seeks software engineering jobs with AI enhancement. Route to Program 4 if lead seeks dedicated machine learning engineering, neural networks, and agentic AI.",
            "vs_Program_5": "Route to Program 1 if focus is core application code. Route to Program 5 if focus is cloud infrastructure, Kubernetes, and CI/CD pipelines."
        },
        "common_refund_reasons": [
            "Program Content / Pace Issues: Experience level mismatches and pacing concerns (placing beginners in intermediate/advanced tracks).",
            "Time Commitment: Work-schedule conflicts and falling behind on daily problem-solving.",
            "Financial Constraints: EMI hesitation and unexpected expenses."
        ]
    },

    "Program 2": {
        "code": "Program 2",
        "name": "Modern Data Science & Machine Learning with Specialization in AI (DSML)",
        "short_name": "Scaler DSML",
        "pages": "4 - 7",
        "core_mission": "Bridges the gap between raw data manipulation and predictive intelligence. Teaches advanced SQL, product analytics, statistics, hypothesis testing, and enterprise machine learning.",
        "tracks": {
            "Beginner Track": {
                "name": "Beginner Track (Data Analytics & SQL Foundations)",
                "prerequisites": "No prior coding or math background required (starts from scratch with basic logic and school-level math).",
                "recommended_for": "Non-tech switchers interested in analytics, business professionals, junior analysts."
            },
            "Advanced Track": {
                "name": "Advanced Track (Applied Machine Learning & Deep Learning)",
                "prerequisites": "Basic syntax familiarity and understanding of tabular data / basic math.",
                "recommended_for": "Data Analysts, BI Developers, SQL Programmers with 1+ YOE."
            }
        },
        "negative_filters": [
            "Never pitch this program to leads whose primary goal is building scalable web application backends, microservices, or frontend UIs (route to Program 1).",
            "Do not pitch as an infrastructure/DevOps path (route to Program 5)."
        ],
        "target_titles": [
            "Data Scientist",
            "Data Analyst / Business Analyst",
            "Machine Learning Engineer",
            "Product Analyst",
            "Analytics Consultant"
        ],
        "tie_breaker_rules": {
            "vs_Program_1": "Route to Program 2 if primary career objective is working with data analytics, business metrics, dashboards, product funnel analysis, or predictive modeling rather than core application software.",
            "vs_Program_4": "Route to Program 2 (DSML) if focus is business analytics, SQL, reporting, and standard ML. Route to Program 4 if intent is building generative AI, deep neural networks, and autonomous multi-agent systems."
        },
        "common_refund_reasons": [
            "Program Content / Pace Issues: Math anxiety and advanced Python learning curves for non-math backgrounds.",
            "Time Commitment: High project turnaround times during hypothesis testing and ML projects."
        ]
    },

    "Program 3": {
        "code": "Program 3",
        "name": "AI Forward Deployed Engineer (FDE) Program",
        "short_name": "Scaler FDE",
        "pages": "7 - 11",
        "core_mission": "Tackles the 'Enterprise Deployment Gap' where 95% of GenAI proofs-of-concept fail in production. Prepares engineers to deploy, integrate, secure, and customize autonomous AI solutions live inside client enterprise architectures.",
        "tracks": {
            "Core FDE Track": {
                "name": "Enterprise AI Deployment & Production RAG Track",
                "prerequisites": "Solid programming background in Python, Java, Go, JS, or C++ and basic familiarity with backend systems or APIs.",
                "recommended_for": "Senior backend developers, tech leads, solutions engineers, client-facing enterprise consultants."
            }
        },
        "negative_filters": [
            "MANDATORY EXCLUSION RULE (Page 10): NEVER pitch this program to absolute beginners or freshers with zero coding background!",
            "Do not pitch to candidates seeking standard data analyst or junior testing roles."
        ],
        "target_titles": [
            "Forward Deployed Engineer (FDE)",
            "AI Solutions Architect",
            "Enterprise AI Implementation Engineer",
            "Applied AI Engineer"
        ],
        "tie_breaker_rules": {
            "vs_Program_1": "Route to Program 3 if objective is specifically enterprise client integration, PySpark pipelines, production RAG, and live AI deployment. Route to Program 1 if objective is general consumer-facing software.",
            "vs_Program_4": "Route to Program 3 if focus is client-facing consulting, enterprise security, and integration. Route to Program 4 if focus is pure research, model fine-tuning, and algorithmic model building."
        },
        "common_refund_reasons": [
            "Program Expectation Mismatch: Expecting pure coding without understanding the client-facing enterprise consulting requirements.",
            "Workload / Time Crunch: Senior engineers getting staffed on urgent client production releases."
        ]
    },

    "Program 4": {
        "code": "Program 4",
        "name": "AI & Machine Learning with Agentic AI Program",
        "short_name": "Scaler Agentic AI",
        "pages": "11 - 15",
        "core_mission": "Tackles the modern 'AI-Blindspot' by teaching neural networks, deep learning, PyTorch, LLM fine-tuning, vector databases, and multi-agent system orchestration.",
        "tracks": {
            "Beginner Track": {
                "name": "Beginner Track (Python, Math Foundations & Basic ML)",
                "prerequisites": "No prior coding or advanced math required (starts from basic logic and school-level calculus/algebra).",
                "recommended_for": "Motivated career switchers with quantitative aptitude willing to take foundational prep."
            },
            "Advanced Track": {
                "name": "Advanced Track (Transformer Architectures & Autonomous Agents)",
                "prerequisites": "1+ years of programming exposure and basic understanding of machine learning.",
                "recommended_for": "Software Engineers and Data Analysts pivoting into frontier AI/ML engineering."
            }
        },
        "negative_filters": [
            "Never pitch to software engineers whose primary objective is traditional low-level design or cracking SDE-2 backend interviews (route to Program 1).",
            "Never pitch to leads wanting cloud server reliability, Kubernetes clusters, and GPU orchestration without model building (route to Program 5)."
        ],
        "target_titles": [
            "AI/ML Engineer",
            "Agentic AI Engineer",
            "LLM / GenAI Engineer",
            "Deep Learning Research Engineer"
        ],
        "tie_breaker_rules": {
            "vs_Program_2": "Route to Program 4 if primary goal is AI/ML engineering (deep learning, LLMOps, autonomous multi-agents). Route to Program 2 if primary goal is business intelligence, metrics, and applied data analytics.",
            "vs_Program_5": "Route to Program 4 if objective is building the AI models and agentic workflows themselves. Route to Program 5 if objective is building and maintaining the cloud/Kubernetes clusters that host them."
        },
        "common_refund_reasons": [
            "Program Content / Pace: Fast-moving generative AI architectures and heavy PyTorch math.",
            "Expectation Gap: Expecting simple prompt engineering rather than deep algorithmic model training."
        ]
    },

    "Program 5": {
        "code": "Program 5",
        "name": "DevOps, Cloud & AI Platform Engineering Program",
        "short_name": "Scaler DevOps & Cloud",
        "pages": "15 - 20",
        "core_mission": "Bridges the 'AI-Infrastructure Gap' where traditional sysadmins cannot handle modern distributed AI platforms. Teaches Linux systems, Docker, Kubernetes, Terraform, CI/CD, SRE reliability, and GPU cluster operations.",
        "tracks": {
            "Core Cloud Track": {
                "name": "Cloud Infrastructure & Platform Operations Track",
                "prerequisites": "Basic programming or technical aptitude (starts with Linux shell scripting and beginner Python for absolute alignment).",
                "recommended_for": "Systems Engineers, Linux Admins, QA Automation, Tech Support, Cloud Engineers."
            }
        },
        "negative_filters": [
            "Never pitch to software engineers whose primary goal is building frontend UI components or consumer-facing mobile apps.",
            "Never pitch to leads wanting pure machine learning model creation or algorithmic data science (route to Program 4)."
        ],
        "target_titles": [
            "DevOps Engineer",
            "Site Reliability Engineer (SRE)",
            "Cloud Platform Architect",
            "MLOps Infrastructure Engineer"
        ],
        "tie_breaker_rules": {
            "vs_Program_1": "Route to Program 5 if focus is infrastructure, deployment automation, and system reliability. Route to Program 1 if focus is writing application business logic and algorithms.",
            "vs_Program_3": "Route to Program 5 if focus is platform operations and cloud infrastructure with no client-facing consulting. Route to Program 3 if focus is custom enterprise client AI integration."
        },
        "common_refund_reasons": [
            "Time Commitment: Shift work and on-call operational duty conflicts.",
            "Pacing: Linux command-line and distributed networking hurdles for non-infrastructure leads."
        ]
    }
}

def get_catalog_entry(program_code_or_name):
    """
    Retrieves full catalog metadata for any program code (Program 1 - 5) or partial name.
    """
    for code, data in SCALER_CATALOG.items():
        if code.lower() in str(program_code_or_name).lower() or data['short_name'].lower() in str(program_code_or_name).lower():
            return data
    return SCALER_CATALOG["Program 1"]
