"""
Program Intelligence & Curriculum Engine for Scaler Program Evaluator
Provides official catalogue URLs, track-specific structured curriculum modules,
and deep-dive syllabus outlines tailored to each learner's recommended track.
"""

# Official Scaler Program Catalog & Base Metadata
PROGRAM_CATALOG_DATA = {
    'P1_ACADEMY': {
        'program_name': 'Modern Software & AI Engineering (Scaler Academy)',
        'catalogue_url': 'https://d2beiqkhq929f0.cloudfront.net/public_assets/assets/000/218/970/original/Academy_brochure_2026_%281%29.pdf?1787132291',
        'top_hiring_companies': [
            'Amazon', 'Microsoft', 'Google', 'Razorpay', 'Swiggy', 
            'PayPal', 'Atlassian', 'Walmart', 'PhonePe', 'Salesforce'
        ]
    },
    'P2_DSML': {
        'program_name': 'Modern Data Science & Machine Learning (AI Specialization)',
        'catalogue_url': 'https://d2beiqkhq929f0.cloudfront.net/public_assets/assets/000/210/531/original/DSML_Brochure_2026_%282%29.pdf?1783928557',
        'top_hiring_companies': [
            'Amazon', 'Flipkart', 'PayPal', 'Sigmoid', 'Fractal', 
            'Mu Sigma', 'Quantiphi', 'Deloitte', 'Accenture', 'Tredence'
        ],
        'curriculum_modules': [
            {
                'segment': 'Data Analytics & SQL',
                'type': 'Core',
                'phase': 'Phase 1: Python, Advanced SQL & Data Wrangling',
                'duration': '10 Weeks',
                'topics': 'Pandas, NumPy, Advanced SQL (Window Functions, CTEs, Pivots), Data Cleaning, Exploratory Data Analysis (EDA).',
                'deliverable': 'Execute business analytics queries across 10M+ transaction tables with sub-second execution.'
            },
            {
                'segment': 'Mathematical Foundations',
                'type': 'Core',
                'phase': 'Phase 2: Applied Statistics & Probability for AI',
                'duration': '8 Weeks',
                'topics': 'Inferential Statistics, Probability Distributions, Hypothesis Testing, A/B Testing Frameworks, Regression Modeling.',
                'deliverable': 'Design statistical experiment pipelines evaluated by product companies for business impact.'
            },
            {
                'segment': 'Machine Learning',
                'type': 'Core',
                'phase': 'Phase 3: Supervised, Unsupervised & Deep Learning',
                'duration': '12 Weeks',
                'topics': 'Scikit-Learn, XGBoost, Random Forests, PyTorch, Neural Architectures, CNNs, RNNs, NLP Fundamentals.',
                'deliverable': 'Train and tune production recommendation and predictive risk scoring models.'
            },
            {
                'segment': 'Generative AI & MLOps',
                'type': 'Specialisation',
                'phase': 'Phase 4: Generative AI, LLMs & Production MLOps',
                'duration': '8 Weeks',
                'topics': 'LangChain, Vector DBs (Chroma/Pinecone), Retrieval-Augmented Generation (RAG), Model Serving (FastAPI, Docker, AWS).',
                'deliverable': 'Deploy end-to-end Enterprise RAG Question-Answering Bot on AWS.'
            }
        ]
    },
    'P3_FDE': {
        'program_name': 'AI Forward Deployed Engineer (FDE) Program',
        'catalogue_url': 'https://d2beiqkhq929f0.cloudfront.net/public_assets/assets/000/217/310/original/FDE_Brochure_.pdf?1786110990',
        'top_hiring_companies': ['Palantir', 'Fractal', 'Tiger Analytics', 'Accenture AI', 'EY Tech', 'KPMG Lighthouse'],
        'curriculum_modules': [
            {
                'segment': 'Enterprise Data Pipelines',
                'type': 'Core',
                'phase': 'Phase 1: Enterprise Problem Framing & Data Engineering',
                'duration': '8 Weeks',
                'topics': 'ETL Pipelines, PySpark, Snowflake, Data Governance, Client Solution Discovery, Cloud Warehousing.',
                'deliverable': 'Automated enterprise ingestion pipeline processing streaming IoT/CRM data.'
            },
            {
                'segment': 'Applied AI Solutions',
                'type': 'Core',
                'phase': 'Phase 2: Production Applied ML & LLM Workflows',
                'duration': '10 Weeks',
                'topics': 'HuggingFace, Fine-Tuning Open-Weights LLMs (Llama-3), Embeddings, Agentic Decision Loops, Tool Calling.',
                'deliverable': 'Automated document processing and intelligence extraction system for enterprise clients.'
            },
            {
                'segment': 'Client Deployment & Security',
                'type': 'Specialisation',
                'phase': 'Phase 3: Client Deployment & AI Architecture Integration',
                'duration': '8 Weeks',
                'topics': 'Enterprise Security, SOC2 Compliance, On-Prem/VPC LLM Deployment, System Evaluation, Air-gapped Infra.',
                'deliverable': 'Full client-ready PoC deployed in air-gapped simulated VPC environment.'
            }
        ]
    },
    'P4_AIML_AGENTIC': {
        'program_name': 'AI & Machine Learning with Agentic AI Program',
        'catalogue_url': 'https://d2beiqkhq929f0.cloudfront.net/public_assets/assets/000/207/098/original/AI__ML_Agentic_AI_Brochure_.pdf?1782394058',
        'top_hiring_companies': ['Google DeepMind Ecosystem', 'Microsoft Research', 'NVIDIA', 'Siemens Healthineers', 'Zoho AI'],
        'curriculum_modules': [
            {
                'segment': 'Deep Learning Core',
                'type': 'Core',
                'phase': 'Phase 1: Deep Learning Foundations & Transformers',
                'duration': '10 Weeks',
                'topics': 'Attention Mechanisms, Transformer Architectures from scratch, BERT, GPT, Vision Transformers, PyTorch internals.',
                'deliverable': 'Implement and train mini-transformer decoder from scratch using PyTorch.'
            },
            {
                'segment': 'Agentic Architectures',
                'type': 'Core',
                'phase': 'Phase 2: Multi-Agent Systems & Tool Calling',
                'duration': '10 Weeks',
                'topics': 'LangGraph, AutoGen, CrewAI, Function Calling, ReAct Agent Loops, Memory Architectures, Vector Stores.',
                'deliverable': 'Autonomous multi-agent research analyst team coordinating code writing and verification.'
            },
            {
                'segment': 'Autonomous Execution',
                'type': 'Specialisation',
                'phase': 'Phase 3: Autonomous Task Execution & Evaluation Frameworks',
                'duration': '8 Weeks',
                'topics': 'Agent benchmarking (SWE-bench), Guardrails, Safety, Cost & Latency Optimization, Production Deployment.',
                'deliverable': 'Production agent capable of debugging and generating GitHub Pull Requests autonomously.'
            }
        ]
    },
    'P5_DEVOPS_CLOUD': {
        'program_name': 'DevOps, Cloud & AI Platform Engineering',
        'catalogue_url': 'https://d2beiqkhq929f0.cloudfront.net/public_assets/assets/000/206/970/original/DEVOPS-Brochure-2026_%281%29.pdf?1782371159',
        'top_hiring_companies': ['Cisco', 'NetApp', 'AWS', 'VMware', 'Red Hat', 'BrowserStack'],
        'curriculum_modules': [
            {
                'segment': 'Systems & Networking',
                'type': 'Core',
                'phase': 'Phase 1: Linux Internals & Networking',
                'duration': '6 Weeks',
                'topics': 'Kernel namespaces, cgroups, TCP/IP, DNS, Bash automation, System troubleshooting.',
                'deliverable': 'Custom container runtime built from scratch.'
            },
            {
                'segment': 'Container Orchestration',
                'type': 'Core',
                'phase': 'Phase 2: Docker & Kubernetes at Scale',
                'duration': '10 Weeks',
                'topics': 'K8s Cluster architecture, Helm, Service Mesh, Ingress, Pod autoscaling, Observability (Prometheus/Grafana).',
                'deliverable': 'Production K8s deployment handling zero-downtime rolling updates.'
            },
            {
                'segment': 'Infrastructure as Code',
                'type': 'Specialisation',
                'phase': 'Phase 3: Infrastructure as Code & GitOps',
                'duration': '8 Weeks',
                'topics': 'Terraform, Ansible, ArgoCD, GitHub Actions CI/CD, Multi-cloud AWS/GCP orchestration.',
                'deliverable': 'Multi-region cloud infrastructure provisioned via 1-click GitOps.'
            }
        ]
    }
}

# ==============================================================================
# SOFTWARE & AI ENGINEERING (SCALER ACADEMY) - TRACK SPECIFIC DETAILED CURRICULA
# ==============================================================================

# 1. BEGINNERS TRACK (Includes Programming Fundamentals with AI)
P1_ACADEMY_BEGINNER_MODULES = [
    {
        'segment': 'Programming Fundamentals',
        'type': 'Core',
        'phase': 'Programming Fundamentals - Thinking with AI: Logics, Loops & Control Flow',
        'duration': '1 Month',
        'topics': 'Programming Foundations & AI Awareness, Operators & Expression Evaluation using AI, Data Types 1 & 2 + Reading Inputs, If-Else & AI Edge Case Thinking, Lab Session on If-Else, Loops & Iteration Analysis by AI, Lab Session on Loop, More problems on Loops & Patterns, Lab Session on Patterns, Dual Camera Proctoring, Data Types, If-Else & Loops Contest discussion.',
        'deliverable': 'Mastery of foundational computational logic, edge case handling, and AI-assisted debugging loops.'
    },
    {
        'segment': 'Programming Fundamentals',
        'type': 'Core',
        'phase': 'Programming Fundamentals - Code Smarter with AI: Function & Arrays',
        'duration': '1 Month',
        'topics': 'Functions & Modularity: Designing Code with AI, Lab Session on Functions, Introduction to Strings, 1D Array, Lab Session on 1D Array (1 & 2), 2D Array (1 & 2), Strings in Memory: Visualizing with AI, Maths Basics & Calculate Iterations, Language Internals, Contest 2: Functions & Arrays.',
        'deliverable': 'Multi-dimensional array manipulation, memory layout tracing, and clean modular function architecture.'
    },
    {
        'segment': 'Programming Fundamentals',
        'type': 'Core',
        'phase': 'Intermediate DSA : AI Assisted Problem Solving',
        'duration': '1 Month',
        'topics': 'Time Complexity, Arrays & Basics of AI, Lab Session on TC/SC/Output & Debugging, Prefix Sum & Carry Forward with AI-Assisted Problem Solving, Arrays techniques & smart prompting, Memory Management & Sorting Basics, Bit Manipulation Basics, 2D Matrices, Strings & Immutability visualisations through AI, Contest.',
        'deliverable': 'Master prefix sum patterns, bit manipulation, time/space complexity optimization, and fast matrix operations.'
    },
    {
        'segment': 'Agentic AI',
        'type': 'Core',
        'phase': 'AI & Agents: From Talking to AI to Building One',
        'duration': '1 Month',
        'topics': 'GenAI World & LLM Landscape, Prompt Engineering Basics, Advanced Prompting & AI Safety Basics, LLM Built-in Power Tools, RAG Architectures, n8n Automation Workflows, What Is an AI Agent?, Building Agents with n8n, OpenClaw: Personal 24/7 AI Agent, Multi-Agent Systems, Debugging AI.',
        'deliverable': 'Deploy autonomous multi-agent developer workflows with n8n and build a personal 24/7 AI agent.'
    },
    {
        'segment': 'Advanced DSA',
        'type': 'Core',
        'phase': 'Advanced DSA: Foundations: Core Techniques & Optimization',
        'duration': '1 Month',
        'topics': 'Time Complexity, Arrays Techniques (1D & 2D), Bit Manipulation, Recursion & Backtracking Prep, Maths: Modular Arithmetic & GCD, Hashing, Sorting (Count Sort, Merge Sort, Quick Sort & Comparator Problems), Sample Contest & Contest 1.',
        'deliverable': 'Algorithmic problem-solving foundations, recursive tree modeling, and custom comparator sorting mastery.'
    },
    {
        'segment': 'Advanced DSA',
        'type': 'Core',
        'phase': 'Advanced DSA: Linear & Non-Linear Structures',
        'duration': '1 Month',
        'topics': 'Searching 1 (Binary Search on Array) & Searching 2 (Binary Search on Answer), Classes/Objects & Linked List Intro, Linked List Basic Problems, Stacks, Queues: Implementation & Problems, Trees 1 (Structure & Traversal), Trees 2 (BST), Contest 2.',
        'deliverable': 'Production implementation of custom Linked Lists, Stacks, Queues, and Binary Search Tree traversal engines.'
    },
    {
        'segment': 'Advanced DSA',
        'type': 'Core',
        'phase': 'Advanced DSA: Backtracking & Advanced Trees',
        'duration': '1 Month',
        'topics': 'Combinatorics Basics & Prime Numbers, Lab Session on Prime Numbers & 2 Pointers, Backtracking, Linked List Sorting, Doubly Linked List & Detecting Loops, Trees 4: Morris Inorder Traversal + LCA, Hashing 3: Internal Implementation, Contest 3.',
        'deliverable': 'Solve complex backtracking constraints, tree LCA, and Morris traversal with zero auxiliary space overhead.'
    },
    {
        'segment': 'Advanced DSA',
        'type': 'Core',
        'phase': 'Advanced DSA: DP, Heaps & Graphs — Crack It with AI Edge',
        'duration': '1 Month',
        'topics': 'Heaps & Heap Sort, Greedy Algorithms, Dynamic Programming (1D, 2D, Knapsack), Graphs 1 (DFS & Cycle Detection), Graphs 2 (BFS & MST), Graphs 3 (Dijkstra Algo & Topological Sort), Social Network Analyzer Capstone, Invoice Merger Capstone, Mandatory Skill Evaluation Test.',
        'deliverable': 'Production Capstones: Social Network Graph Analyzer & Invoice Merger; full graph traversal & dynamic programming.'
    },
    {
        'segment': 'Databases & SQL',
        'type': 'Core',
        'phase': 'Databases & SQL: Production Schema Design & Optimization',
        'duration': '1 Month',
        'topics': 'Introduction to DBMS & Keys, CRUD Operations (1 & 2), Joins, Aggregate Queries, Subqueries & Views, Indexing, Transactions & Isolation, Window Functions, Schema Design (1 & 2), Databases & SQL Contest.',
        'deliverable': 'Design ACID-compliant normalized relational database schemas with high-speed indexing & window queries.'
    },
    {
        'segment': 'Backend Specialisation',
        'type': 'Specialisation',
        'phase': 'Foundations of Object-Oriented Design & Scalable Systems',
        'duration': '1 Month',
        'topics': 'Intro to LLD for Scalable & AI-Ready Systems, OOP Lab (Access Modifiers, Constructors, Inheritance, Polymorphism, Interfaces, Abstract Classes), Concurrency (Threads, Executors, Callables, Synchronization, Semaphores), Java Advanced Concepts (Generics, Collections, Streams, Lambdas, Exception Handling), Contest 1.',
        'deliverable': 'Multi-threaded thread-safe concurrent in-memory caching and messaging primitives.'
    },
    {
        'segment': 'Backend Specialisation',
        'type': 'Specialisation',
        'phase': 'Design Principles & Patterns for Extensible Systems',
        'duration': '1 Month',
        'topics': 'SOLID Principles with AI integrations, Creational Patterns (Singleton, Builder, Prototype/Registry, Factory for Service Abstraction), Structural Patterns (Adapter, Facade, Decorator, Flyweight), Behavioural Patterns, UML Diagrams, Contest 2.',
        'deliverable': 'Architectural design blueprints conforming to strict SOLID principles and GoF design patterns.'
    },
    {
        'segment': 'Backend Specialisation',
        'type': 'Specialisation',
        'phase': 'Applied Design & Machine Coding',
        'duration': '1 Month',
        'topics': 'Machine Coding Strategies under timed conditions, Design & Implement: TicTacToe (1 & 2), Parking Lot, BookMyShow (1, 2, 3), Splitwise (1 & 2), Machine Coding Evaluations.',
        'deliverable': 'Build complete, working, object-oriented machine-coded systems (Parking Lot, Splitwise, BookMyShow).'
    },
    {
        'segment': 'Backend Specialisation',
        'type': 'Specialisation',
        'phase': 'AI-First Backend Capstone Project Primer',
        'duration': '1 Month',
        'topics': 'Intro to Backend Systems & AI-Augmented Development, Version Control & Git, Spring Framework & Building APIs, MVC & Microservices with AI Service Integration, 3rd Party APIs & LLM Services, Spring Data JPA, Automated Unit Testing, OAuth2 & JWT Security, AWS Cloud Deployment.',
        'deliverable': 'Live Spring Boot microservice deployed to AWS with AI service integration and automated authentication.'
    },
    {
        'segment': 'Backend Specialisation',
        'type': 'Elective',
        'phase': 'AI-First Backend Capstone Advance & Build a Production-Ready AI System',
        'duration': '1.5 - 2.5 Months',
        'topics': 'RestTemplate Resilience, Mocking & Unit Tests, OAuth2, AWS (EBS, RDS, VPC, Route 53), Semantic Search, Stripe Payments & Reconciliation, Redis Caching & Kafka Queues, Spring Cloud, Docker, BookMyShow Chat Agent, Splitwise AI Receipt Processor.',
        'deliverable': 'Enterprise-grade microservices suite with Redis caching, Kafka streaming, and autonomous AI agents.'
    },
    {
        'segment': 'Fullstack Track',
        'type': 'Specialisation',
        'phase': 'Fullstack Web Platform, React & Backend Systems (Alternative Specialisation)',
        'duration': '4 Months',
        'topics': 'Web Platform Foundations (HTML5, Responsive CSS, Flexbox/Grid), JavaScript Runtime Systems (DOM, Async/Await, Event Loop, Weather & Kanban Apps), React & Redux Product Architecture (IMDB Clone), Node.js, Express & MongoDB Production Systems.',
        'deliverable': 'Production MERN stack platform with real-time seat reservation engine and Redux state architecture.'
    },
    {
        'segment': 'System Design & Electives',
        'type': 'Elective',
        'phase': 'Distributed System Design & AI-Integrated Architectures',
        'duration': '1.5 Months',
        'topics': 'Load Balancing, Consistent Hashing, CDN & Caching at Scale (Scaler Judge, FB News Feed), CAP/PACELC Theorem, Master-Slave Replication, SQL vs NoSQL, Database Sharding, Case Studies: Google Typeahead, Messaging Apps (WhatsApp, FB Messenger), Apache Kafka, ElasticSearch, S3/HDFS, Uber Nearest Neighbor, Rate Limiter, OTT Microservices.',
        'deliverable': 'Distributed systems architecture handling 1M+ RPS with high availability and resilience.'
    },
    {
        'segment': 'Interview Prep & Electives',
        'type': 'Elective',
        'phase': 'Mastering LastMile Simulation, Data Engineering & Gen AI Electives',
        'duration': '1.5 Weeks - 2 Months',
        'topics': 'DSA/LLD/HLD Interview Simulation under pressure, Data Engineering (PySpark, Hadoop, Hive, Spark Streaming, AWS), DSA Edge (Advanced Patterns), Product Management for Engineers, Gen AI for Software Engineers (RAG, Agents, Fine-Tuning, Quantization).',
        'deliverable': 'MAANG interview clearance readiness, high-throughput data pipelines, and production generative AI systems.'
    }
]

# 2. INTERMEDIATE TRACK (Skips Beginner Programming Fundamentals; starts at Intermediate DSA)
P1_ACADEMY_INTERMEDIATE_MODULES = [
    {
        'segment': 'Programming Fundamentals',
        'type': 'Core',
        'phase': 'Intermediate DSA : AI Assisted Problem Solving',
        'duration': '1 Month',
        'topics': 'Time Complexity, Arrays & Basics of AI, Lab Session on TC/SC/Output & Debugging, Prefix Sum & Carry Forward with AI-Assisted Problem Solving, Arrays techniques & smart prompting, Memory Management & Sorting Basics, Bit Manipulation Basics, 2D Matrices, Strings & Immutability visualisations through AI, Contest.',
        'deliverable': 'Master prefix sum patterns, bit manipulation, time/space complexity optimization, and fast matrix operations.'
    },
    {
        'segment': 'Agentic AI',
        'type': 'Core',
        'phase': 'AI & Agents: From Talking to AI to Building One',
        'duration': '1 Month',
        'topics': 'GenAI World & LLM Landscape, Prompt Engineering Basics, Advanced Prompting & AI Safety Basics, LLM Built-in Power Tools, RAG Architectures, n8n Automation Workflows, What Is an AI Agent?, Building Agents with n8n, OpenClaw: Personal 24/7 AI Agent, Multi-Agent Systems, Debugging AI.',
        'deliverable': 'Deploy autonomous multi-agent developer workflows with n8n and build a personal 24/7 AI agent.'
    },
    {
        'segment': 'Advanced DSA',
        'type': 'Core',
        'phase': 'Advanced DSA: Foundations: Core Techniques & Optimization',
        'duration': '1 Month',
        'topics': 'Time Complexity, Arrays Techniques (1D & 2D), Bit Manipulation, Recursion & Backtracking Prep, Maths: Modular Arithmetic & GCD, Hashing, Sorting (Count Sort, Merge Sort, Quick Sort & Comparator Problems), Sample Contest & Contest 1.',
        'deliverable': 'Algorithmic problem-solving foundations, recursive tree modeling, and custom comparator sorting mastery.'
    },
    {
        'segment': 'Advanced DSA',
        'type': 'Core',
        'phase': 'Advanced DSA: Linear & Non-Linear Structures',
        'duration': '1 Month',
        'topics': 'Searching 1 (Binary Search on Array) & Searching 2 (Binary Search on Answer), Classes/Objects & Linked List Intro, Linked List Basic Problems, Stacks, Queues: Implementation & Problems, Trees 1 (Structure & Traversal), Trees 2 (BST), Contest 2.',
        'deliverable': 'Production implementation of custom Linked Lists, Stacks, Queues, and Binary Search Tree traversal engines.'
    },
    {
        'segment': 'Advanced DSA',
        'type': 'Core',
        'phase': 'Advanced DSA: Backtracking & Advanced Trees',
        'duration': '1 Month',
        'topics': 'Combinatorics Basics & Prime Numbers, Lab Session on Prime Numbers & 2 Pointers, Backtracking, Linked List Sorting, Doubly Linked List & Detecting Loops, Trees 4: Morris Inorder Traversal + LCA, Hashing 3: Internal Implementation, Contest 3.',
        'deliverable': 'Solve complex backtracking constraints, tree LCA, and Morris traversal with zero auxiliary space overhead.'
    },
    {
        'segment': 'Advanced DSA',
        'type': 'Core',
        'phase': 'Advanced DSA: DP, Heaps & Graphs — Crack It with AI Edge',
        'duration': '1 Month',
        'topics': 'Heaps & Heap Sort, Greedy Algorithms, Dynamic Programming (1D, 2D, Knapsack), Graphs 1 (DFS & Cycle Detection), Graphs 2 (BFS & MST), Graphs 3 (Dijkstra Algo & Topological Sort), Social Network Analyzer Capstone, Invoice Merger Capstone, Mandatory Skill Evaluation Test.',
        'deliverable': 'Production Capstones: Social Network Graph Analyzer & Invoice Merger; full graph traversal & dynamic programming.'
    },
    {
        'segment': 'Databases & SQL',
        'type': 'Core',
        'phase': 'Databases & SQL: Production Schema Design & Optimization',
        'duration': '1 Month',
        'topics': 'Introduction to DBMS & Keys, CRUD Operations (1 & 2), Joins, Aggregate Queries, Subqueries & Views, Indexing, Transactions & Isolation, Window Functions, Schema Design (1 & 2), Databases & SQL Contest.',
        'deliverable': 'Design ACID-compliant normalized relational database schemas with high-speed indexing & window queries.'
    },
    {
        'segment': 'Backend Specialisation',
        'type': 'Specialisation',
        'phase': 'Foundations of Object-Oriented Design & Scalable Systems',
        'duration': '1 Month',
        'topics': 'Intro to LLD for Scalable & AI-Ready Systems, OOP Lab (Access Modifiers, Constructors, Inheritance, Polymorphism, Interfaces, Abstract Classes), Concurrency (Threads, Executors, Callables, Synchronization, Semaphores), Java Advanced Concepts (Generics, Collections, Streams, Lambdas, Exception Handling), Contest 1.',
        'deliverable': 'Multi-threaded thread-safe concurrent in-memory caching and messaging primitives.'
    },
    {
        'segment': 'Backend Specialisation',
        'type': 'Specialisation',
        'phase': 'Design Principles & Patterns for Extensible Systems',
        'duration': '1 Month',
        'topics': 'SOLID Principles with AI integrations, Creational Patterns (Singleton, Builder, Prototype/Registry, Factory for Service Abstraction), Structural Patterns (Adapter, Facade, Decorator, Flyweight), Behavioural Patterns, UML Diagrams, Contest 2.',
        'deliverable': 'Architectural design blueprints conforming to strict SOLID principles and GoF design patterns.'
    },
    {
        'segment': 'Backend Specialisation',
        'type': 'Specialisation',
        'phase': 'Applied Design & Machine Coding',
        'duration': '1 Month',
        'topics': 'Machine Coding Strategies under timed conditions, Design & Implement: TicTacToe (1 & 2), Parking Lot, BookMyShow (1, 2, 3), Splitwise (1 & 2), Machine Coding Evaluations.',
        'deliverable': 'Build complete, working, object-oriented machine-coded systems (Parking Lot, Splitwise, BookMyShow).'
    },
    {
        'segment': 'Backend Specialisation',
        'type': 'Specialisation',
        'phase': 'AI-First Backend Capstone Project Primer',
        'duration': '1 Month',
        'topics': 'Intro to Backend Systems & AI-Augmented Development, Version Control & Git, Spring Framework & Building APIs, MVC & Microservices with AI Service Integration, 3rd Party APIs & LLM Services, Spring Data JPA, Automated Unit Testing, OAuth2 & JWT Security, AWS Cloud Deployment.',
        'deliverable': 'Live Spring Boot microservice deployed to AWS with AI service integration and automated authentication.'
    },
    {
        'segment': 'Backend Specialisation',
        'type': 'Specialisation',
        'phase': 'AI-First Backend Capstone Advance & Build a Production-Ready AI System',
        'duration': '1.5 - 2.5 Months',
        'topics': 'RestTemplate Resilience, Mocking & Unit Tests, OAuth2, AWS (EBS, RDS, VPC, Route 53), Semantic Search, Stripe Payments & Reconciliation, Redis Caching & Kafka Queues, Spring Cloud, Docker, BookMyShow Chat Agent, Splitwise AI Receipt Processor.',
        'deliverable': 'Enterprise-grade microservices suite with Redis caching, Kafka streaming, and autonomous AI agents.'
    },
    {
        'segment': 'Fullstack Track',
        'type': 'Specialisation',
        'phase': 'Fullstack Web Platform, React & Backend Systems (Alternative Specialisation)',
        'duration': '4.5 Months',
        'topics': 'Web Platform Foundations (HTML5, Responsive CSS, Flexbox/Grid), JavaScript Runtime Systems (Execution Model, Closures, DOM, Async/Await, Weather App & Kanban Board Labs), React & Redux Product Architecture (IMDB Clone), Node.js, Express & MongoDB Production Systems.',
        'deliverable': 'Production MERN stack platform with real-time seat reservation engine and Redux state architecture.'
    },
    {
        'segment': 'System Design & Electives',
        'type': 'Elective',
        'phase': 'Distributed System Design & AI-Integrated Architectures',
        'duration': '1.5 Months',
        'topics': 'Load Balancing, Consistent Hashing, CDN & Caching at Scale, CAP/PACELC Theorem, Master-Slave Replication, SQL vs NoSQL, Database Sharding, Case Studies: Google Typeahead, Messaging Apps, Apache Kafka, ElasticSearch, S3/HDFS, Uber Nearest Neighbor, Rate Limiter, OTT Microservices.',
        'deliverable': 'Scalable distributed systems architectures engineered for 1M+ queries/sec with zero single points of failure.'
    },
    {
        'segment': 'Interview Prep & Electives',
        'type': 'Elective',
        'phase': 'Mastering LastMile Simulation & Emerging Tech Electives',
        'duration': '1.5 Weeks - 2 Months',
        'topics': 'DSA/LLD/HLD Interview Simulation under pressure, Data Engineering (PySpark, Hadoop, Hive, Spark Streaming, AWS), DSA Edge (Advanced Patterns), Product Management for Engineers, Gen AI for Software Engineers (RAG, Agents, Fine-Tuning, Quantization).',
        'deliverable': 'MAANG interview clearance readiness, high-throughput data pipelines, and production generative AI systems.'
    }
]

# 3. ADVANCED TRACK (Skips all Beginner Fundamentals & Intermediate DSA; System Design is CORE)
P1_ACADEMY_ADVANCED_MODULES = [
    {
        'segment': 'Agentic AI',
        'type': 'Core',
        'phase': 'AI & Agents: From Talking to AI to Building One',
        'duration': '1 Month',
        'topics': 'The runway to AI, GenAI World & LLM Landscape, Prompt Engineering Basics, Advanced Prompting & AI Safety Basics, LLM Built-in Power Tools, RAG Architectures, n8n Automation Workflows, What Is an AI Agent?, Building Agents with n8n, OpenClaw: Personal 24/7 AI Agent, Multi-Agent Systems, Debugging AI with Vibecoding Tools.',
        'deliverable': 'Deploy autonomous multi-agent developer workflows with n8n and build a personal 24/7 AI agent.'
    },
    {
        'segment': 'Advanced DSA',
        'type': 'Core',
        'phase': 'Advanced DSA: Foundations: Core Techniques & Optimization',
        'duration': '1 Month',
        'topics': 'Time Complexity Optimization, 1D & 2D Arrays Techniques, Bit Manipulation, Recursion, Maths: Modular Arithmetic & GCD, Hashing, Sorting (Count Sort, Merge Sort, Quick Sort & Comparators), Dual Camera Proctoring Contest 1.',
        'deliverable': 'Algorithmic problem-solving foundations, recursive tree modeling, and custom comparator sorting mastery.'
    },
    {
        'segment': 'Advanced DSA',
        'type': 'Core',
        'phase': 'Advanced DSA: Linear & Non-Linear Structures',
        'duration': '1 Month',
        'topics': 'Searching 1 (Binary Search on Array) & Searching 2 (Binary Search on Answer), Classes/Objects & Linked Lists, Stacks & Queues Architecture, Binary Trees Structure & Traversal, Binary Search Trees (BST), Contest 2.',
        'deliverable': 'Production implementation of custom non-linear data structures and BST operations.'
    },
    {
        'segment': 'Advanced DSA',
        'type': 'Core',
        'phase': 'Advanced DSA: Backtracking & Advanced Trees',
        'duration': '1 Month',
        'topics': 'Combinatorics & Primes, Two Pointers, Backtracking Masterclass, Morris Inorder Traversal, Lowest Common Ancestor (LCA), Advanced Hashing Internals, Contest 3.',
        'deliverable': 'Solve complex backtracking constraints, tree LCA, and Morris traversal with zero auxiliary space overhead.'
    },
    {
        'segment': 'Advanced DSA',
        'type': 'Core',
        'phase': 'Advanced DSA: DP, Heaps & Graphs — Crack It with AI Edge',
        'duration': '1 Month',
        'topics': 'Heaps & Heap Sort, Greedy Algorithms, Dynamic Programming (1D, 2D, Knapsack), Graphs 1 (DFS & Cycle Detection), Graphs 2 (BFS & MST), Graphs 3 (Dijkstra Algo & Topological Sort), Social Network Analyzer Capstone, Invoice Merger Capstone, Mandatory Skill Evaluation Test.',
        'deliverable': 'Production Capstones: Social Network Graph Analyzer & Invoice Merger; full graph traversal & dynamic programming.'
    },
    {
        'segment': 'Databases & SQL',
        'type': 'Core',
        'phase': 'Databases & SQL: Production Schema Design & Optimization',
        'duration': '1 Month',
        'topics': 'Introduction to DBMS & Keys, CRUD Operations (1 & 2), Joins, Aggregate Queries, Subqueries & Views, Indexing, Transactions & Isolation, Window Functions, Schema Design (1 & 2), SQL and Schema Design Contest.',
        'deliverable': 'Design ACID-compliant normalized relational database schemas with high-speed indexing & window queries.'
    },
    {
        'segment': 'Backend Specialisation',
        'type': 'Specialisation',
        'phase': 'Foundations of Object-Oriented Design & Scalable Systems',
        'duration': '1 Month',
        'topics': 'Intro to LLD for Scalable & AI-Ready Systems, OOP Lab (Access Modifiers, Constructors, Inheritance, Polymorphism, Interfaces, Abstract Classes), Concurrency (Threads, Executors, Callables, Synchronization, Semaphores), Java Advanced Concepts (Generics, Collections, Streams, Lambdas, Exception Handling), Contest 1.',
        'deliverable': 'Multi-threaded thread-safe concurrent in-memory caching and messaging primitives.'
    },
    {
        'segment': 'Backend Specialisation',
        'type': 'Specialisation',
        'phase': 'Design Principles & Patterns for Extensible Systems',
        'duration': '1 Month',
        'topics': 'SOLID Principles with AI integrations, Creational Patterns (Singleton, Builder, Prototype/Registry, Factory for Service Abstraction), Structural Patterns (Adapter, Facade, Decorator, Flyweight), Behavioural Patterns, UML Diagrams, Contest 2.',
        'deliverable': 'Architectural design blueprints conforming to strict SOLID principles and GoF design patterns.'
    },
    {
        'segment': 'Backend Specialisation',
        'type': 'Specialisation',
        'phase': 'Applied Design & Machine Coding',
        'duration': '1 Month',
        'topics': 'Machine Coding Strategies under timed conditions, Design & Implement: TicTacToe (1 & 2), Parking Lot, BookMyShow (1, 2, 3), Splitwise (1 & 2), Low Level Design & Machine Coding Evaluations.',
        'deliverable': 'Build complete, working, object-oriented machine-coded systems (Parking Lot, Splitwise, BookMyShow).'
    },
    {
        'segment': 'Backend Specialisation',
        'type': 'Specialisation',
        'phase': 'AI-First Backend Capstone Project Primer',
        'duration': '1 Month',
        'topics': 'Intro to Backend Systems & AI-Augmented Development, Version Control & Git, Spring Framework & Building APIs, MVC & Microservices with AI Service Integration, 3rd Party APIs & LLM Services, Spring Data JPA, Automated Unit Testing, OAuth2 & JWT Security, AWS Cloud Deployment.',
        'deliverable': 'Live Spring Boot microservice deployed to AWS with AI service integration and automated authentication.'
    },
    {
        'segment': 'Backend Specialisation',
        'type': 'Specialisation',
        'phase': 'AI-First Backend Capstone Advance & Build a Production-Ready AI System',
        'duration': '1.5 - 2.5 Months',
        'topics': 'RestTemplate Resilience, Mocking & Unit Tests, OAuth2, AWS (EBS, RDS, VPC, Route 53), Semantic Search, Stripe Payments & Reconciliation, Redis Caching & Kafka Queues, Spring Cloud, Docker, BookMyShow Chat Agent, Splitwise AI Receipt Processor.',
        'deliverable': 'Enterprise-grade microservices suite with Redis caching, Kafka streaming, and autonomous AI agents.'
    },
    {
        'segment': 'System Design',
        'type': 'Core',
        'phase': 'Distributed System Design & AI-Integrated Architectures',
        'duration': '1.5 Months',
        'topics': 'System Design Foundations & Modern Infrastructure, Load Balancing, Consistent Hashing & Traffic Routing at Scale, Caching Systems (CDN, Scaler Judge Leaderboards), CAP/PACELC Theorem, Master-Slave Replication, SQL vs NoSQL, Database Sharding, Case Studies: Google Typeahead, Messaging Apps (WhatsApp, FB Messenger), Apache Kafka, ElasticSearch, S3/HDFS, Uber Nearest Neighbor, Rate Limiter, OTT Microservices.',
        'deliverable': 'High-Level System Design architectures handling 1M+ RPS with high availability and zero single point of failure.'
    },
    {
        'segment': 'Interview Preparation',
        'type': 'Elective',
        'phase': 'Mastering LastMile - Interview Simulation',
        'duration': '1.5 Weeks',
        'topics': 'DSA Interview Simulation: Problem Solving & Thinking Under Pressure, LLD Interview Simulation: Structuring Scalable Solutions, HLD Interview Simulation: Designing Systems & Communicating Trade-offs.',
        'deliverable': 'Live simulated interview clearance benchmarked against MAANG hiring bars.'
    },
    {
        'segment': 'Electives',
        'type': 'Elective',
        'phase': 'Data Engineering, Gen AI for Software Engineers & Product Management',
        'duration': '1.5 - 2 Months',
        'topics': 'Data Engineering (PySpark, Hadoop, Hive, Spark Streaming, AWS), DSA Edge (Advanced Patterns, Tries, Bellman-Ford), Product Management for Engineers, Gen AI for Software Engineers (RAG, Agents, Fine-Tuning, Quantization).',
        'deliverable': 'High-throughput big data pipelines, fine-tuned domain models, and autonomous AI coding agents.'
    }
]


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
    Returns official catalogue URLs and track-tailored curriculum modules.
    If Scaler Academy (P1) is selected, returns the precise modules for
    the candidate's assigned track (Beginner, Intermediate, or Advanced).
    """
    # 1. Resolve program code
    if any(k in str(arg1).upper() for k in ['P1', 'P2', 'P3', 'P4', 'P5', 'ACADEMY', 'DSML', 'DATA SCIENCE', 'DEVOPS', 'FDE', 'AGENTIC', 'PROGRAM']):
        p_code = resolve_program_code(arg1)
    elif any(k in str(arg4).upper() for k in ['P1', 'P2', 'P3', 'P4', 'P5', 'ACADEMY', 'DSML', 'DATA SCIENCE', 'DEVOPS', 'FDE', 'AGENTIC', 'PROGRAM']):
        p_code = resolve_program_code(arg4)
    else:
        p_code = resolve_program_code(arg1)

    p_data = PROGRAM_CATALOG_DATA.get(p_code, PROGRAM_CATALOG_DATA['P1_ACADEMY'])

    # 2. Track-specific resolution for Scaler Academy (P1)
    if p_code == 'P1_ACADEMY':
        all_text = f"{str(track_name)} {str(arg1)} {str(arg2)} {str(arg3)} {str(arg4)}".lower()
        t_low = str(track_name).lower() if track_name else ''

        if 'advanced' in t_low or 'system design' in t_low or 'scalability' in t_low or 'architecture' in t_low:
            selected_modules = P1_ACADEMY_ADVANCED_MODULES
            track_label = 'Advanced Track'
        elif 'intermediate' in t_low or 'dsa core' in t_low or 'sde transition' in t_low or 'algorithms & lld' in t_low:
            selected_modules = P1_ACADEMY_INTERMEDIATE_MODULES
            track_label = 'Intermediate Track'
        elif 'beginner' in t_low or 'foundation' in t_low or 'problem solving' in t_low:
            selected_modules = P1_ACADEMY_BEGINNER_MODULES
            track_label = 'Beginner Track'
        else:
            # Fallback to experience-based tier if track_name is generic
            try:
                exp_num = float(str(arg3).replace('years', '').replace('yrs', '').replace('+', '').strip())
                if exp_num >= 5.0:
                    selected_modules = P1_ACADEMY_ADVANCED_MODULES
                    track_label = 'Advanced Track'
                elif exp_num >= 2.0:
                    selected_modules = P1_ACADEMY_INTERMEDIATE_MODULES
                    track_label = 'Intermediate Track'
                else:
                    selected_modules = P1_ACADEMY_BEGINNER_MODULES
                    track_label = 'Beginner Track'
            except Exception:
                selected_modules = P1_ACADEMY_BEGINNER_MODULES
                track_label = 'Beginner Track'

        return {
            'program_name': p_data['program_name'],
            'catalogue_url': p_data['catalogue_url'],
            'top_hiring_companies': p_data.get('top_hiring_companies', []),
            'curriculum_modules': selected_modules,
            'track_label': track_label
        }

    # For other programs (P2, P3, P4, P5), return their structured curriculum modules
    return {
        'program_name': p_data['program_name'],
        'catalogue_url': p_data['catalogue_url'],
        'top_hiring_companies': p_data.get('top_hiring_companies', []),
        'curriculum_modules': p_data.get('curriculum_modules', []),
        'track_label': str(track_name) if track_name else 'Standard Track'
    }
