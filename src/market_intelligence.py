"""
Program Intelligence & Curriculum Engine for Scaler Program Evaluator
Provides official catalogue URLs, structured curriculum modules, and
inbound masterclass vs comprehensive program comparison matrices.
"""

# Official Scaler Program Catalog & Curriculum Definitions
PROGRAM_CATALOG_DATA = {
    'P1_ACADEMY': {
        'program_name': 'Modern Software & AI Engineering (Scaler Academy)',
        'catalogue_url': 'https://www.scaler.com/academy/',
        'top_hiring_companies': [
            'Amazon', 'Microsoft', 'Google', 'Razorpay', 'Swiggy', 
            'PayPal', 'Atlassian', 'Walmart', 'PhonePe', 'Salesforce'
        ],
        'curriculum_modules': [
            {
                'phase': 'Phase 1: Algorithmic Thinking & DSA Core',
                'duration': '12 Weeks',
                'topics': 'Time/Space Complexity, Recursion, Trees, Graphs, Dynamic Programming, Greedy Algorithms.',
                'deliverable': 'Mastery of 300+ interview patterns reverse-engineered from MAANG hiring benchmarks.'
            },
            {
                'phase': 'Phase 2: Low-Level Design (LLD) & Clean OOP',
                'duration': '8 Weeks',
                'topics': 'SOLID Principles, Design Patterns (Factory, Strategy, Observer), Schema Modeling, Concurrency.',
                'deliverable': 'Build production-grade systems from scratch: Parking Lot, Splitwise, and In-Memory Cache.'
            },
            {
                'phase': 'Phase 3: High-Level System Design (HLD)',
                'duration': '10 Weeks',
                'topics': 'Distributed Systems, Caching (Redis), Message Queues (Kafka), Database Sharding, Microservices.',
                'deliverable': 'Design real scalable architectures: Ride Matching & Video Streaming at 1M+ RPS.'
            },
            {
                'phase': 'Phase 4: Full-Stack & Generative AI Integration',
                'duration': '8 Weeks',
                'topics': 'Spring Boot / Node.js, Cloud Deployment (AWS), REST/gRPC APIs, Integrating LLM Workflows.',
                'deliverable': 'End-to-end production application live on cloud with automated CI/CD pipeline.'
            }
        ]
    },
    'P2_DSML': {
        'program_name': 'Modern Data Science & Machine Learning (AI Specialization)',
        'catalogue_url': 'https://www.scaler.com/data-science-course/',
        'top_hiring_companies': [
            'Amazon', 'Flipkart', 'PayPal', 'Sigmoid', 'Fractal', 
            'Mu Sigma', 'Quantiphi', 'Deloitte', 'Accenture', 'Tredence'
        ],
        'curriculum_modules': [
            {
                'phase': 'Phase 1: Python, Advanced SQL & Data Wrangling',
                'duration': '10 Weeks',
                'topics': 'Pandas, NumPy, Advanced SQL (Window Functions, CTEs), Data Cleaning, Exploratory Analysis.',
                'deliverable': 'Execute business analytics queries across 10M+ transaction tables with sub-second execution.'
            },
            {
                'phase': 'Phase 2: Applied Statistics & Probability for AI',
                'duration': '8 Weeks',
                'topics': 'Inferential Statistics, Hypothesis Testing, A/B Testing Frameworks, Regression Modeling.',
                'deliverable': 'Design statistical experiment pipelines evaluated by product companies for business impact.'
            },
            {
                'phase': 'Phase 3: Machine Learning & Deep Learning',
                'duration': '12 Weeks',
                'topics': 'Supervised & Unsupervised Learning, XGBoost, Scikit-Learn, PyTorch, Neural Architectures, NLP.',
                'deliverable': 'Train and tune production recommendation and predictive risk scoring models.'
            },
            {
                'phase': 'Phase 4: Generative AI, LLMs & MLOps',
                'duration': '8 Weeks',
                'topics': 'LangChain, Vector DBs (Chroma/Pinecone), Retrieval-Augmented Generation (RAG), Model Serving (FastAPI/Docker).',
                'deliverable': 'Deploy end-to-end Enterprise RAG Question-Answering Bot on AWS.'
            }
        ]
    },
    'P3_FDE': {
        'program_name': 'AI Forward Deployed Engineer (FDE) Program',
        'catalogue_url': 'https://www.scaler.com/ai/',
        'top_hiring_companies': ['Palantir', 'Fractal', 'Tiger Analytics', 'Accenture AI', 'EY Tech', 'KPMG Lighthouse'],
        'curriculum_modules': [
            {
                'phase': 'Phase 1: Enterprise Problem Framing & Data Engineering',
                'duration': '8 Weeks',
                'topics': 'ETL Pipelines, PySpark, Snowflake, Data Governance, Client Solution Discovery.',
                'deliverable': 'Automated enterprise ingestion pipeline processing streaming IoT/CRM data.'
            },
            {
                'phase': 'Phase 2: Production Applied ML & LLM Workflows',
                'duration': '10 Weeks',
                'topics': 'HuggingFace, Fine-Tuning Open-Weights LLMs (Llama-3), Embeddings, Agentic Decision Loops.',
                'deliverable': 'Automated document processing and intelligence extraction system for enterprise clients.'
            },
            {
                'phase': 'Phase 3: Client Deployment & AI Architecture Integration',
                'duration': '8 Weeks',
                'topics': 'Enterprise Security, SOC2 Compliance, On-Prem/VPC LLM Deployment, System Evaluation.',
                'deliverable': 'Full client-ready PoC deployed in air-gapped simulated VPC environment.'
            }
        ]
    },
    'P4_AIML_AGENTIC': {
        'program_name': 'AI & Machine Learning with Agentic AI Program',
        'catalogue_url': 'https://www.scaler.com/ai/',
        'top_hiring_companies': ['Google DeepMind Ecosystem', 'Microsoft Research', 'NVIDIA', 'Siemens Healthineers', 'Zoho AI'],
        'curriculum_modules': [
            {
                'phase': 'Phase 1: Deep Learning Foundations & Transformers',
                'duration': '10 Weeks',
                'topics': 'Attention Mechanisms, Transformer Architectures from scratch, BERT, GPT, Vision Transformers.',
                'deliverable': 'Implement and train mini-transformer decoder from scratch using PyTorch.'
            },
            {
                'phase': 'Phase 2: Multi-Agent Systems & Tool Calling',
                'duration': '10 Weeks',
                'topics': 'LangGraph, AutoGen, CrewAI, Function Calling, ReAct Agent Loops, Memory Architectures.',
                'deliverable': 'Autonomous multi-agent research analyst team coordinating code writing and verification.'
            },
            {
                'phase': 'Phase 3: Autonomous Task Execution & Evaluation Frameworks',
                'duration': '8 Weeks',
                'topics': 'Agent benchmarking (SWE-bench), Guardrails, Safety, Cost & Latency Optimization.',
                'deliverable': 'Production agent capable of debugging and generating GitHub Pull Requests autonomously.'
            }
        ]
    },
    'P5_DEVOPS_CLOUD': {
        'program_name': 'DevOps, Cloud & AI Platform Engineering',
        'catalogue_url': 'https://www.scaler.com/devops/',
        'top_hiring_companies': ['Cisco', 'NetApp', 'AWS', 'VMware', 'Red Hat', 'BrowserStack'],
        'curriculum_modules': [
            {
                'phase': 'Phase 1: Linux Internals & Networking',
                'duration': '6 Weeks',
                'topics': 'Kernel namespaces, cgroups, TCP/IP, DNS, Bash automation.',
                'deliverable': 'Custom container runtime built from scratch.'
            },
            {
                'phase': 'Phase 2: Docker & Kubernetes at Scale',
                'duration': '10 Weeks',
                'topics': 'K8s Cluster architecture, Helm, Service Mesh, Ingress, Pod autoscaling.',
                'deliverable': 'Production K8s deployment handling zero-downtime rolling updates.'
            },
            {
                'phase': 'Phase 3: Infrastructure as Code & GitOps',
                'duration': '8 Weeks',
                'topics': 'Terraform, Ansible, ArgoCD, GitHub Actions CI/CD.',
                'deliverable': 'Multi-region cloud infrastructure provisioned via 1-click GitOps.'
            }
        ]
    }
}

def resolve_program_code(prog_val):
    if not prog_val:
        return 'P1_ACADEMY'
    p = str(prog_val).upper().strip()
    if 'P2' in p or 'DSML' in p or 'DATA SCIENCE' in p:
        return 'P2_DSML'
    elif 'P3' in p or 'FDE' in p or 'FORWARD' in p:
        return 'P3_FDE'
    elif 'P4' in p or 'AGENTIC' in p:
        return 'P4_AIML_AGENTIC'
    elif 'P5' in p or 'DEVOPS' in p or 'CLOUD' in p or 'PLATFORM' in p:
        return 'P5_DEVOPS_CLOUD'
    elif 'P1' in p or 'ACADEMY' in p or 'SOFTWARE' in p:
        return 'P1_ACADEMY'
    return 'P1_ACADEMY'

def get_market_intelligence(arg1="", arg2="", arg3="", arg4="", track_name=""):
    """
    Returns official catalogue URLs and curriculum modules.
    """
    if any(k in str(arg1).upper() for k in ['P1', 'P2', 'P3', 'P4', 'P5', 'ACADEMY', 'DSML', 'DATA SCIENCE', 'DEVOPS', 'FDE', 'AGENTIC', 'PROGRAM']):
        p_code = resolve_program_code(arg1)
    elif any(k in str(arg4).upper() for k in ['P1', 'P2', 'P3', 'P4', 'P5', 'ACADEMY', 'DSML', 'DATA SCIENCE', 'DEVOPS', 'FDE', 'AGENTIC', 'PROGRAM']):
        p_code = resolve_program_code(arg4)
    else:
        p_code = resolve_program_code(arg1)

    p_data = PROGRAM_CATALOG_DATA.get(p_code, PROGRAM_CATALOG_DATA['P1_ACADEMY'])

    return {
        'program_name': p_data['program_name'],
        'catalogue_url': p_data['catalogue_url'],
        'top_hiring_companies': p_data.get('top_hiring_companies', []),
        'curriculum_modules': p_data.get('curriculum_modules', [])
    }

