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
        'top_hiring_companies': ['Palantir', 'Fractal', 'Tiger Analytics', 'Accenture AI', 'EY Tech', 'KPMG Lighthouse']
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

# ==============================================================================
# MODERN DATA SCIENCE & MACHINE LEARNING (DSML) - TRACK SPECIFIC CURRICULA
# ==============================================================================

# 1. BEGINNERS TRACK (14 - 21.5 Months - Foundations through Machine Learning & Agentic AI)
P2_DSML_BEGINNER_MODULES = [
    {
        'segment': 'Data Foundations & SQL',
        'type': 'Core',
        'phase': 'Advanced SQL & AI for Data Professionals',
        'duration': '2 Months',
        'topics': 'Data Foundations & SQL Intro, Schema Basics, Data Filtering, NULLs & Aggregation, GROUP BY Metrics, Applied SQL Labs (1 to 4), CASE WHEN, JOINs (INNER, LEFT, FULL OUTER, CROSS, SELF, NON-EQUI), Subqueries (Correlated & Non-Correlated, EXISTS), CTEs, Window Functions (ROW_NUMBER, Advanced Ranking, Navigation & Trends), Date/Time SQL, MySQL Setup, DDL/DML, Views, Indexing, Partitioning, Stored Procedures, Funnel Analytics & Cohort Retention.',
        'deliverable': 'Production SQL pipelines, cohort retention models, and sub-second analytical query optimization.'
    },
    {
        'segment': 'BI & Storytelling',
        'type': 'Core',
        'phase': 'Excel & Dashboarding with AI Storytelling',
        'duration': '1 Month',
        'topics': 'Excel (Structure, Formulas, Lookups, Pivot Tables, Mini Dashboard, Live Reporting Case), Tableau (Viz Fundamentals, KPIs, Filters, Calculations, Dashboard Labs, LOD Expressions, Table Calcs, Live Business Case 4: Dashboard Storytelling).',
        'deliverable': 'Interactive executive dashboards in Tableau and Excel with AI-powered KPI storytelling.'
    },
    {
        'segment': 'Programming for Data',
        'type': 'Core',
        'phase': 'Python Foundations + AI Coding Assistants',
        'duration': '1 Month',
        'topics': 'Python (Data Types, Variables, I/O, Control Flow, Loops, Functions, Lists, Strings, Data Structures, Debugging Masterclass), Pandas (Read, Filter, Select, Groupby KPIs, Merge, Cleaning, EDA & Data Quality Checks, Complete EDA).',
        'deliverable': 'Clean Python scripts, automated EDA pipelines, and robust data munging using Pandas.'
    },
    {
        'segment': 'Product Analytics',
        'type': 'Core',
        'phase': 'Data to Decisions: Product Analytics with AI',
        'duration': '1 Month',
        'topics': 'Metrics Foundations (DAU, MAU, Retention, Funnels), Event Tracking & Data Instrumentation, User Segmentation & Behavioral Analysis, Funnel Analysis, Cohort Analysis & Retention Deep Dive, Growth Metrics (Activation, Engagement, Retention), A/B Testing Fundamentals & Pitfalls, Revenue Metrics (AOV, LTV, CAC), Feature Adoption, AI for Product Analytics, Applied Product Lab.',
        'deliverable': 'Product analytics frameworks, user retention cohorts, and AI-driven growth hypothesis generation.'
    },
    {
        'segment': 'Analytics Automation',
        'type': 'Core',
        'phase': 'Generative AI for Data Analytics & Automation',
        'duration': '1 Month',
        'topics': 'GenAI & LLMs for Analysts, Prompt Engineering for Data (SQL, Python, Insights), AI for SQL Query Generation & Debugging, Python/Pandas Automation, AI for Data Cleaning & EDA, Dashboard Insights & Storytelling, AI-Assisted Reports, Automating Repetitive Analysis, Evaluating AI Outputs (Hallucination, Bias), OpenAI APIs for Data Workflows, Mini AI Tools, Applied GenAI Lab.',
        'deliverable': 'Autonomous analyst workflows, automated report generation, and custom OpenAI-powered data tools.'
    },
    {
        'segment': 'Career Readiness',
        'type': 'Core',
        'phase': 'Interview Readiness: Technical & Product Cases',
        'duration': '1 Month',
        'topics': 'SQL Pattern Recognition & Case-Based Problem Solving (JOINs, Window Functions, CTEs), Python & Pandas Technical Interview Prep, Product Case Interviews (Metrics & Business Thinking), Estimation & Guesstimates, Resume Building (Projects, Impact, Storytelling), LinkedIn & Portfolio Optimization.',
        'deliverable': 'Analyst portfolio, case study defense, and technical interview clearance for Tier-1 data teams.'
    },
    {
        'segment': 'Advanced Data Engineering',
        'type': 'Core',
        'phase': 'Advanced Analytics with Python, Pandas & AI Workflows',
        'duration': '1 Month',
        'topics': 'Python Refresher, Data Manipulation & Chaining, Groupby Transformations, Multi-Table Data Handling, Handling Large Datasets, Data Cleaning at Scale, NumPy Foundations & Advanced NumPy for Analytics, Data Visualization & Feature Engineering, Automation Scripts & Scheduling, AI-Assisted Analysis & Code Generation, End-to-End AI Data Solutions.',
        'deliverable': 'Scalable data manipulation pipelines processing massive multi-table datasets with automated feature engineering.'
    },
    {
        'segment': 'Applied Statistics',
        'type': 'Core',
        'phase': 'Statistics, Experimentation & AI for Data-Driven Decisions',
        'duration': '1 Month',
        'topics': 'Probability Foundations, Distributions (Normal, Binomial), Sampling Techniques & Bias, Central Limit Theorem (Intuition + Applications), Hypothesis Testing Fundamentals, p-values, Confidence Intervals & Errors, A/B Testing (Design, Setup, Analysis & Interpretation), Experimentation Pitfalls (Bias, Peeking, Simpson\'s Paradox), Metric Design, AI-Assisted Statistical Interpretation & Validation, Applied Experiment Lab.',
        'deliverable': 'Rigorous statistical A/B testing framework evaluated by product tech leaders.'
    },
    {
        'segment': 'Product Analytics',
        'type': 'Core',
        'phase': 'Advanced Product Analytics & Strategy',
        'duration': '1 Month',
        'topics': 'Advanced Funnel Analysis (Multi-step, Multi-channel), Retention Models & Cohort Deep Dive, Customer Lifetime Value (LTV) Modeling, Customer Acquisition Cost (CAC) & Payback, Growth Loops & Product-Led Growth, Segmentation Strategies (Behavioral & Value-based), Churn Analysis & Retention Strategies, Predictive Analytics for Product, Recommendation Systems (Conceptual), Decision Frameworks, AI for Product Strategy, Applied Product Capstone.',
        'deliverable': 'End-to-end product strategy and predictive customer retention model capstone.'
    },
    {
        'segment': 'Domain Analytics',
        'type': 'Elective',
        'phase': 'Domain Analytics (FinTech, E-Commerce, HealthTech)',
        'duration': '1 Month',
        'topics': 'E-commerce Analytics & Basket Analysis, FinTech Risk & Fraud Modeling, HealthTech Analytics, SaaS Growth Metrics, Custom Domain Case Studies.',
        'deliverable': 'Specialized industry capstone solving real enterprise domain problem statements.'
    },
    {
        'segment': 'Cloud Analytics',
        'type': 'Elective',
        'phase': 'Cloud & Data Analytics on AWS',
        'duration': '1 Month',
        'topics': 'Modern Cloud Data Stack, AWS Fundamentals (S3, IAM), S3 Data Lakes, Querying Data with Amazon Athena, Data Warehousing with Amazon Redshift, ETL with AWS Glue, End-to-End Data Pipelines, Connecting Tableau to Cloud Data Sources, Performance & Cost Optimization, Intro to Databricks & Lakehouse Concept, Applied Cloud Lab.',
        'deliverable': 'Production cloud data lakehouse on AWS with Athena, Redshift, and automated Glue ETL.'
    },
    {
        'segment': 'Applied AI',
        'type': 'Core',
        'phase': 'AI For Everyone & Autonomous Workflows',
        'duration': '2 Months',
        'topics': 'Comparative Framework for AI Tools, Model Selection, AI Failure Modes & Mitigation, Voice-Driven Analytical Workflows, No-Code Process Automation for Data, Org Knowledge Bases Integration, Reusable Prompt Libraries, Project Task Decomposition, Three-Tier Workflow Mapping, No-Code Prototyping, Autonomous AI Boundaries, Multi-Step AI Pipelines, Applied Agent Dev (Data Monitoring Workflow), AI-Assisted Presentations & Communicating AI Work Responsibly.',
        'deliverable': 'Autonomous data-monitoring AI agents and no-code analytical tools deployed across enterprise workflows.'
    },
    {
        'segment': 'Mathematical Foundations',
        'type': 'Core',
        'phase': 'Mathematical Foundations for AI',
        'duration': '1 Month',
        'topics': 'Linear Algebra in ML (Dot products, hyperplanes, halfspaces, distance, loss minimization in classification), Calculus & Optimization (Gradient descent in action, constrained optimization, Principal Component Analysis PCA).',
        'deliverable': 'Mathematical vector foundations and custom gradient descent optimization engine from scratch.'
    },
    {
        'segment': 'Machine Learning',
        'type': 'Core',
        'phase': 'Machine Learning with AI Workflows',
        'duration': '1 Month',
        'topics': 'Intro to ML, Linear Regression (1 to 4), Polynomial Regression, Bias-Variance Tradeoff, Regularization (L1/L2), Cross-Validation, Logistic Regression (1 & 2), Classification Metrics (Confusion Matrix, ROC-AUC, Imbalanced Data).',
        'deliverable': 'Calibrated predictive regression and classification pipelines handling imbalanced enterprise data.'
    },
    {
        'segment': 'Machine Learning',
        'type': 'Elective',
        'phase': 'Supervised Machine Learning with AI',
        'duration': '1 Month',
        'topics': 'k-Nearest Neighbors (1 & 2), Decision Trees (1 & 2), Bagging & Random Forest, Boosting (AdaBoost, Gradient Boosting, XGBoost), Ensemble Techniques, Naive Bayes (1 & 2), Support Vector Machines (SVM 1 & 2), Supervised ML Wrap-up.',
        'deliverable': 'Tuned ensemble models (XGBoost, Random Forest) solving complex classification challenges.'
    },
    {
        'segment': 'Machine Learning',
        'type': 'Elective',
        'phase': 'Un-supervised Machine Learning with AI',
        'duration': '1 Month',
        'topics': 'Dimensionality Reduction (PCA, t-SNE, UMAP), Clustering (K-Means, K-Means++, Gaussian Mixture Models GMM, Hierarchical Clustering, DBSCAN), Anomaly Detection, End-to-End Business Cases (1 & 2).',
        'deliverable': 'High-dimensional customer segmentation and anomaly detection engines.'
    },
    {
        'segment': 'Forecasting & Recommenders',
        'type': 'Elective',
        'phase': 'Time Series and Recommender Systems with AI Workflows',
        'duration': '1 Month',
        'topics': 'Time Series Forecasting (ARIMA, SARIMA, Prophet), Trend & Seasonality Decomposition, Recommender Systems (Collaborative Filtering, Matrix Factorization, Content-Based, Hybrid Engines), End-to-end Practical Session.',
        'deliverable': 'Scalable multi-modal recommendation engine and automated time-series demand forecasting system.'
    },
    {
        'segment': 'MLOps & Platform',
        'type': 'Elective',
        'phase': 'MLOps & AI Deployment',
        'duration': '1 Month',
        'topics': 'Git & GitHub for MLOps, Building Streamlit Tools (Cars24 case), Web APIs using Flask/FastAPI, Containerization with Docker & DockerHub, Deploying APIs on AWS ECS, CI/CD with GitHub Actions, Experiment Tracking with MLflow, ML System Design (1 & 2), AWS SageMaker Pipelines, Large-scale processing with Apache Spark.',
        'deliverable': 'End-to-end production CI/CD MLOps pipeline on AWS ECS with Docker, MLflow, and SageMaker.'
    },
    {
        'segment': 'Deep Learning',
        'type': 'Elective',
        'phase': 'Deep Learning & Neural Networks',
        'duration': '1 Month',
        'topics': 'Neural Networks Intro, Forward & Backpropagation, N-Layer Neural Networks, Backprop Mathematics, TensorFlow & Keras (1 & 2), Optimizers (Adam, RMSprop), Hyperparameter Tuning, Autoencoders, MLP Design & Debugging, Model Interpretability (LIME).',
        'deliverable': 'Multi-layer perceptron neural network architectures with custom optimizers and explainability frameworks.'
    },
    {
        'segment': 'Computer Vision',
        'type': 'Elective',
        'phase': 'AI for Computer Vision',
        'duration': '1 Month',
        'topics': 'Computer Vision Intro (CNNs), Addressing Overfitting, CNN under the hood, Transfer Learning, Image Similarity & Embeddings, CNN for Medical Diagnosis, Object Localization & Detection (YOLO), Object Segmentation, Siamese Networks, Generative Models & GANs Intro.',
        'deliverable': 'Real-time object detection and visual feature extraction pipeline using Transfer Learning.'
    },
    {
        'segment': 'Natural Language Processing',
        'type': 'Elective',
        'phase': 'AI for Natural Language Processing',
        'duration': '1 Month',
        'topics': 'NLP Foundations, Text Representation, Word Embeddings (Word2Vec), Language Modeling, Topic Modeling, RNNs, LSTMs, Named Entity Recognition (NER), Attention Mechanisms, Transformer Architecture, BERT.',
        'deliverable': 'Production text intelligence pipeline with named entity extraction and transformer embeddings.'
    },
    {
        'segment': 'Agentic AI',
        'type': 'Elective',
        'phase': 'AI Engineering and Agentic AI',
        'duration': '1.5 Months',
        'topics': 'AI Engineering Intro, Modern Text & Image Model Architectures, Text Generation APIs (OpenAI), Eval Pipelines & Observability, Prompt Engineering & Security, RAG & Embeddings Deep Dive, Multimodal & Tabular RAG, Autonomous Agents (Foundations, Planning, Frameworks & Protocols - LangGraph/CrewAI), Fine-Tuning Models, Scaling AI Apps, Quantization, Inference Optimization.',
        'deliverable': 'Enterprise Autonomous Multi-Agent reasoning system and production RAG pipeline.'
    }
]

# 2. INTERMEDIATE TRACK (11.5 Months - Core ML, MLOps, Deep Learning & Agentic AI)
P2_DSML_INTERMEDIATE_MODULES = [
    {
        'segment': 'Advanced Data Engineering',
        'type': 'Core',
        'phase': 'Advanced Analytics with Python, Pandas & AI Workflows',
        'duration': '1 Month',
        'topics': 'Python Refresher, Data Manipulation & Chaining, Groupby Transformations, Multi-Table Data Handling, Handling Large Datasets, Data Cleaning at Scale, NumPy Foundations & Advanced NumPy for Analytics, Data Visualization & Feature Engineering, Automation Scripts & Scheduling, AI-Assisted Analysis & Code Generation, End-to-End AI Data Solutions.',
        'deliverable': 'Scalable data manipulation pipelines processing massive multi-table datasets with automated feature engineering.'
    },
    {
        'segment': 'Applied Statistics',
        'type': 'Core',
        'phase': 'Statistics, Experimentation & AI for Data-Driven Decisions',
        'duration': '1 Month',
        'topics': 'Probability Foundations, Distributions (Normal, Binomial), Sampling Techniques & Bias, Central Limit Theorem (Intuition + Applications), Hypothesis Testing Fundamentals, p-values, Confidence Intervals & Errors, A/B Testing (Design, Setup, Analysis & Interpretation), Experimentation Pitfalls (Bias, Peeking, Simpson\'s Paradox), Metric Design, AI-Assisted Statistical Interpretation & Validation, Applied Experiment Lab.',
        'deliverable': 'Rigorous statistical A/B testing framework evaluated by product tech leaders.'
    },
    {
        'segment': 'Product Analytics',
        'type': 'Core',
        'phase': 'Advanced Product Analytics',
        'duration': '1 Month',
        'topics': 'Advanced Funnel Analysis (Multi-step, Multi-channel), Retention Models & Cohort Deep Dive, Customer Lifetime Value (LTV) Modeling, Customer Acquisition Cost (CAC) & Payback, Growth Loops & Product-Led Growth, Segmentation Strategies (Behavioral & Value-based), Churn Analysis & Retention Strategies, Predictive Analytics for Product, Recommendation Systems (Conceptual), Decision Frameworks, AI for Product Strategy, Applied Product Capstone.',
        'deliverable': 'End-to-end product strategy and predictive customer retention model capstone.'
    },
    {
        'segment': 'Mathematical Foundations',
        'type': 'Core',
        'phase': 'Mathematical Foundations for AI',
        'duration': '1 Month',
        'topics': 'Linear Algebra in ML (Dot products, hyperplanes, halfspaces, distance, loss minimization in classification), Calculus & Optimization (Gradient descent in action, constrained optimization, Principal Component Analysis PCA).',
        'deliverable': 'Mathematical vector foundations and custom gradient descent optimization engine from scratch.'
    },
    {
        'segment': 'Machine Learning',
        'type': 'Core',
        'phase': 'Machine Learning with AI Workflows',
        'duration': '1 Month',
        'topics': 'Intro to ML, Linear Regression (1 to 4), Polynomial Regression, Bias-Variance Tradeoff, Regularization (L1/L2), Cross-Validation, Logistic Regression (1 & 2), Classification Metrics (Confusion Matrix, ROC-AUC, Imbalanced Data).',
        'deliverable': 'Calibrated predictive regression and classification pipelines handling imbalanced enterprise data.'
    },
    {
        'segment': 'Supervised Learning',
        'type': 'Core',
        'phase': 'Supervised Machine Learning with AI',
        'duration': '1 Month',
        'topics': 'k-Nearest Neighbors (1 & 2), Decision Trees (1 & 2), Bagging & Random Forest, Boosting (AdaBoost, Gradient Boosting, XGBoost), Ensemble Techniques, Naive Bayes (1 & 2), Support Vector Machines (SVM 1 & 2), Supervised ML Wrap-up.',
        'deliverable': 'Tuned ensemble models (XGBoost, Random Forest) solving complex classification challenges.'
    },
    {
        'segment': 'Unsupervised Learning',
        'type': 'Core',
        'phase': 'Un-supervised Machine Learning with AI',
        'duration': '1 Month',
        'topics': 'Dimensionality Reduction (PCA, t-SNE, UMAP), Clustering (K-Means, K-Means++, Gaussian Mixture Models GMM, Hierarchical Clustering, DBSCAN), Anomaly Detection, End-to-End Business Cases (1 & 2).',
        'deliverable': 'High-dimensional customer segmentation and anomaly detection engines.'
    },
    {
        'segment': 'Forecasting & Recommenders',
        'type': 'Core',
        'phase': 'Time Series and Recommender Systems with AI Workflows',
        'duration': '1 Month',
        'topics': 'Time Series Forecasting (ARIMA, SARIMA, Prophet), Trend & Seasonality Decomposition, Recommender Systems (Collaborative Filtering, Matrix Factorization, Content-Based, Hybrid Engines), End-to-end Practical Session.',
        'deliverable': 'Scalable multi-modal recommendation engine and automated time-series demand forecasting system.'
    },
    {
        'segment': 'MLOps & Platform',
        'type': 'Core',
        'phase': 'MLOps & AI Deployment',
        'duration': '1 Month',
        'topics': 'Git & GitHub for MLOps, Building Streamlit Tools (Cars24 case), Web APIs using Flask/FastAPI, Containerization with Docker & DockerHub, Deploying APIs on AWS ECS, CI/CD with GitHub Actions, Experiment Tracking with MLflow, ML System Design (1 & 2), AWS SageMaker Pipelines, Large-scale processing with Apache Spark.',
        'deliverable': 'End-to-end production CI/CD MLOps pipeline on AWS ECS with Docker, MLflow, and SageMaker.'
    },
    {
        'segment': 'Deep Learning',
        'type': 'Core',
        'phase': 'Deep Learning & Neural Networks',
        'duration': '1 Month',
        'topics': 'Neural Networks Intro, Forward & Backpropagation, N-Layer Neural Networks, Backprop Mathematics, TensorFlow & Keras (1 & 2), Optimizers (Adam, RMSprop), Hyperparameter Tuning, Autoencoders, MLP Design & Debugging, Model Interpretability (LIME).',
        'deliverable': 'Multi-layer perceptron neural network architectures with custom optimizers and explainability frameworks.'
    },
    {
        'segment': 'Agentic AI',
        'type': 'Core',
        'phase': 'AI Engineering and Agentic AI',
        'duration': '1.5 Months',
        'topics': 'Introduction to AI Engineering, Refresher on Modern Text & Image Model Architectures, Text Generation APIs (OpenAI API), Eval Pipelines & Observability, Prompt Engineering & Security, Retrieval-Augmented Generation (RAG) & Embeddings Deep Dive, Multimodal & Tabular RAG, Autonomous Agents (Foundations, Planning, Frameworks & Protocols), Fine-Tuning Existing Models, Modalities (Audio, Image, Video), Scaling AI Applications, Model Quantization, Advanced Fine-Tuning, Dataset Engineering & Inference Optimization.',
        'deliverable': 'Production-grade enterprise Autonomous Agent systems, optimized fine-tuned LLMs, and high-performance RAG architectures.'
    }
]

# ==============================================================================
# AI FORWARD DEPLOYED ENGINEER (FDE) - COMPREHENSIVE CURRICULUM & DEEP DIVE
# ==============================================================================

P3_FDE_MODULES = [
    {
        'segment': 'Enterprise Data & Role Playbook',
        'type': 'Core',
        'phase': 'The FDE Launchpad — Role, SQL & the Legacy Data Problem',
        'duration': '1.25 Months',
        'topics': 'Your Playbook for Every Client Room, The Artifact Toolkit That Runs Every Engagement, Meet the Schema - From Entities to Queries, Reporting Views That Run the Dashboard, Find the Bottleneck, Fix the Query, No Half-Measures - Atomic Updates That Don\'t Corrupt, Designing a Schema the Client Won\'t Outgrow, Building Meridian\'s Full Data Model, Lock It Down - PII, Encryption & Audit Trails, Reaching Across the Firewall - Legacy Data Access, Picking the Right Engine for the Job, Quick Diagnostics Before the Pipeline Exists, Designing the Pipeline - ETL Thinking, Explaining Your Schema to the VP Who Signs Off, Turning Query Results into Client-Ready Insight.',
        'deliverable': 'Production enterprise data model (Meridian Data Architecture), legacy data access bridge, and client-ready analytical views with audit trails.'
    },
    {
        'segment': 'Data Ingestion & Concurrency',
        'type': 'Core',
        'phase': 'The Ingestion Pipeline — Production Python',
        'duration': '1.25 Months',
        'topics': 'Your Workbench - Python Toolchain Done Right, Stream It, Don\'t Load It, Reusable Building Blocks - Decorators & Context Managers, Modeling the Real World in Code, Make It Fast - Concurrency & Async, When the Data Fights Back - Error Handling & Resilience, Validate Everything, Log Everything, Prove It Works - Testing & CI, Code That Survives the Next Engineer, PySpark - When Python Meets Big Data, Pipeline Day - Full PySpark Ingestion Build, Under Pressure - Timed Python Build, PR Reviews That Build Trust, Write the Doc They\'ll Actually Read.',
        'deliverable': 'Resilient, high-throughput asynchronous PySpark ingestion pipeline processing enterprise streaming and batch feeds.'
    },
    {
        'segment': 'Enterprise Backend & APIs',
        'type': 'Core',
        'phase': 'The Platform\'s Backend — Orders, Payments & Real-Time Systems',
        'duration': '1.75 Months',
        'topics': 'Your First Production API, Routing the First Request, Making FastAPI Do the Heavy Lifting, Consuming APIs Like a Professional, Who Gets In - Auth Done Right with OAuth2 & JWT, Locking Doors by Role - RBAC, OIDC & Multi-Tenant Auth, The Order Lifecycle - State Machines in Production, Money and Messages - Payments & Notifications, The Contract Between Backend & Frontend, Break the Contract, Break the Build, Push, Don\'t Poll - WebSockets & Server-Sent Events, Queues, Cache, Invalidate - Redis & Message Patterns, Observability & Tracing, Beyond Rows - JSONB, Full-Text Search & Vector Storage, Warehouse Layer - dbt, DuckDB & Dimensional Modeling, Orchestrating the Nightly Pipeline, Kafka Fundamentals, Pipeline Under Fire - Timed Debug Challenge, Running the Room - API Reviews & Incident Updates.',
        'deliverable': 'Production FastAPI enterprise service with multi-tenant RBAC, Kafka event bus, Redis caching, and real-time WebSockets.'
    },
    {
        'segment': 'Client-Facing Systems & UI',
        'type': 'Core',
        'phase': 'The Client-Facing Layer — Frontend Engineering for FDEs',
        'duration': '1 Month',
        'topics': 'How the Web Works: From DOM to Dashboard, Async, Typed and Connected: Talking to the Backend, Thinking in Components: Building the Dashboard One Boundary at a Time, Forms That Don\'t Frustrate: Validation, Control and Reuse, Wiring the Dashboard Live: APIs, Caching and Server State, KPIs, Tables and Filters: The Dashboard Takes Shape, Defending the Architecture: React Decisions and Next.js Awareness, Gating the Dashboard: Authentication, Roles and Protected Routes, Real-Time and AI-Ready Interfaces, Fast, Reliable and Ready: Testing and Performance, Defending the Solution to Leadership, The Handover Moment: Walking the Ops Team Through Their Dashboard.',
        'deliverable': 'Modern enterprise React/Next.js client operations dashboard with live KPI state management and role-gated UI routes.'
    },
    {
        'segment': 'Enterprise RAG & Evaluation',
        'type': 'Core',
        'phase': 'The New Ask — Production RAG for Customer Support',
        'duration': '1 Month',
        'topics': 'The AI Landscape - Picking Your Weapons, Your First System Prompt - And Why It\'ll Break, Choosing How to Serve - APIs, Context & Parameters, Prompts as Code - Versioning & Regression Testing, Building the Knowledge Pipeline - RAG End to End, Does It Actually Find the Right Answer?, Does It Tell the Truth? - Generation Eval & RAGAS, Guardrails That Actually Work - PII Leak Prevention, Red Team Your Own Copilot, Spend Less, Answer Faster, Ship It - Timed RAG Build, Explaining AI Risk Without Scaring the Room, Making Eval Numbers Mean Something to the Board.',
        'deliverable': 'Production RAG customer copilot evaluated with RAGAS, protected by PII guardrails, and optimized for latency/token spend.'
    },
    {
        'segment': 'Autonomous Agents & Protocols',
        'type': 'Core',
        'phase': 'From Answering to Acting — Agents & Enterprise Integration',
        'duration': '1.25 Months',
        'topics': 'From Chatbot to Coworker, Giving the Agent Real Tools, Orchestrating Agent Intelligence with LangGraph, Production Agent Patterns, When the Agent Breaks, MCP - The Universal Tool Protocol, The Agent Team - Multi-Agent & Human-in-the-Loop, Mapping the Client\'s System Landscape, Data Integration with Legacy Enterprise Systems, Wiring It Together - API Connectors & Webhooks, When the Integration Breaks, Ship Day - The Full Agentic Copilot Goes Live, Red-Team War Room, Explaining What the Agent Will and Won\'t Do Alone, Getting the Client\'s IT Team on Your Side.',
        'deliverable': 'LangGraph multi-agent autonomous system integrated via Model Context Protocol (MCP) and enterprise webhooks.'
    },
    {
        'segment': 'Distributed Systems & Scale',
        'type': 'Core',
        'phase': 'The Scale Question — System Design for Black Friday',
        'duration': '1.25 Months',
        'topics': 'The System Design Playbook, Spreading the Load, Cache Everything, Consistency vs Availability, When One Database Isn\'t Enough, Shard It and Build It, When Your Table Hits 10TB, The Event Backbone - Kafka at Scale, Search That Scales, Rate Limiting & Unique IDs, Monolith or Microservices, Distributed Transactions - Saga vs 2PC, Whiteboarding With the Client\'s Architects, System Design Under Pressure.',
        'deliverable': 'Resilient, multi-region distributed system architecture capable of surviving 10x traffic spikes with zero data loss.'
    },
    {
        'segment': 'AI Infrastructure & Architecture',
        'type': 'Core',
        'phase': 'Scaling the AI Layer — Enterprise AI Architecture',
        'duration': '1 Month',
        'topics': 'Serving AI at Scale, One Gateway, Many Models, GPU Math - Capacity Planning, When to Fine-Tune - And When Not To, Embedding Pipelines at Scale, Vector Search at Billion Scale, Evals as Infrastructure, Tracking Experiments - MLflow & Model Registries, Ship Without Breaking - Canary Rollouts for AI, Is the AI Drifting?, Defend Your AI Architecture, Selling the AI Stack to the Board.',
        'deliverable': 'Billion-scale vector search and unified multi-model LLM gateway with canary deployment infrastructure.'
    },
    {
        'segment': 'Systems & Linux Infrastructure',
        'type': 'Core',
        'phase': 'Prepping the Ground — Linux, Networking & Shell',
        'duration': '1 Month',
        'topics': 'Your First Server, Who Gets Access, What\'s Running and Why, Finding the Needle, How Packets Flow, Locking Down the Network, TCP vs. UDP: Below the Surface, Automate the Boring Stuff, Scripts That Keep the Lights On, The Log Parser, Write the Runbook the 3AM Engineer Will Thank You For.',
        'deliverable': 'Hardened Linux operating environment, automated Bash maintenance runbooks, and locked-down network routing.'
    },
    {
        'segment': 'Containers & Orchestration',
        'type': 'Core',
        'phase': 'Containerizing Meridian — Docker & Kubernetes',
        'duration': '1.25 Months',
        'topics': 'Containers 101, Slim, Fast and Secure Images in Production, Containers Talking to Each Other, Hardening Containers, Why You Need an Orchestrator, Deploy It, Wiring Services Together, Scale/Update Under Pressure, Lock It Down, Production K8s, The Pod Won\'t Start, Deploying AI Models on a Cluster, GitOps - Declarative Deployments with ArgoCD, Do We Really Need Kubernetes?, Coordinating the Rollout.',
        'deliverable': 'Production Kubernetes deployment with ArgoCD declarative GitOps, zero-downtime rollouts, and secure container images.'
    },
    {
        'segment': 'Cloud & Infrastructure as Code',
        'type': 'Elective',
        'phase': 'Going Live — AWS Production Deployment with Terraform',
        'duration': '2.25 Months',
        'topics': 'Designing Cloud Network, Compute on AWS, Load Balancing Across AZs, Object Storage, SQL & NoSQL in Cloud, Caching, Locking Down Cloud, Breach Drill, Kubernetes in Cloud (I, II, III), Securing Meridian\'s Cluster, Data & Application, Cert Manager & Route 53 (SSL + DNS), AWS Capstone Kickoff, EKS Capstone (Parts 1 & 2), Cloud Rosetta Stone (AWS ↔ GCP ↔ Azure), Boardroom Cloud Talk, War-Room 101, IaC - Terraform Fundamentals & In Action, CI Pipelines, Deploying Docker Image to EKS.',
        'deliverable': '1-Click Terraform IaC cloud infrastructure on AWS EKS with multi-AZ load balancing, SSL, and automated CI pipelines.'
    },
    {
        'segment': 'SRE & Disaster Recovery',
        'type': 'Elective',
        'phase': 'Making It Bulletproof — Reliability, HA & Disaster Recovery',
        'duration': '1 Month',
        'topics': 'SRE - When 99.9% Isn\'t Enough, Surviving Region Failure - HA Architecture, The DR Plan Nobody Tests (Until It\'s Too Late), Sharding in Production, Breaking to Ensure It Doesn\'t Break (Chaos Engineering), CRDs, Operators & Admission Webhooks in Kubernetes, Advanced AWS Networking, NoSQL & Caching on AWS, Load Testing at Scale - Proving It Before Black Friday, The Reliability Check, Selling Reliability to the CFO.',
        'deliverable': 'Active-active multi-region Disaster Recovery plan, Kubernetes Operators, and Chaos Engineering verified reliability suite.'
    },
    {
        'segment': 'Security & Governance',
        'type': 'Elective',
        'phase': 'Enterprise Sign-Off — Security Hardening & Incident Response',
        'duration': '0.75 Months',
        'topics': 'Threat Modeling - Where Will They Attack?, OWASP Top 10 - Hands-On Exploitation & Defence, Securing the AI Layer, Secrets, Keys & Certificates Lifecycle, Compliance Frameworks - SOC2, GDPR & What FDEs Actually Do, Penetration Testing Your Own Platform, The Incident Response Playbook, Incident Simulation - Full Red Team Exercise, The Security Briefing the Board Actually Needs.',
        'deliverable': 'SOC2/GDPR compliance posture, automated threat defense, secrets rotation vault, and board-ready security clearance.'
    },
    {
        'segment': 'Client Simulation Capstone',
        'type': 'Elective',
        'phase': 'Capstone & Hiring Readiness — New Client, Full Simulation',
        'duration': '0.75 Months',
        'topics': 'New Brief, Day One - The Capstone Kickoff, Build Sprint 1 (Data & Backend), Build Sprint 2 (Frontend & AI Feature), Red Team Day - Classmates Break Your Build, Portfolio Day - Packaging Meridian for Interviews, System Design Interview Prep, Behavioral & FDE Interview Prep, Capstone Demo Day - Graduation.',
        'deliverable': 'End-to-end client engagement simulation (Meridian Platform) presented and defended before enterprise engineering directors.'
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
    If Scaler Academy (P1) or DSML (P2) is selected, returns the precise modules for
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

    # 3. Track-specific resolution for Modern Data Science & ML (P2)
    if p_code == 'P2_DSML':
        t_low = str(track_name).lower() if track_name else ''
        all_text = f"{str(track_name)} {str(arg1)} {str(arg2)} {str(arg3)} {str(arg4)}".lower()

        if 'intermediate' in t_low or 'core analytics' in t_low or 'machine learning' in t_low or 'predictive' in t_low or 'specialization' in t_low:
            selected_modules = P2_DSML_INTERMEDIATE_MODULES
            track_label = 'Intermediate Track (Core ML & AI Engineering)'
        elif 'beginner' in t_low or 'python prep' in t_low or 'foundation' in t_low or 'business ml' in t_low or 'data analytics' in t_low:
            selected_modules = P2_DSML_BEGINNER_MODULES
            track_label = 'Beginner Track (Data Analytics, Python & Business ML)'
        else:
            # Fallback based on experience
            try:
                exp_num = float(str(arg3).replace('years', '').replace('yrs', '').replace('+', '').strip())
                if exp_num >= 2.0:
                    selected_modules = P2_DSML_INTERMEDIATE_MODULES
                    track_label = 'Intermediate Track (Core ML & AI Engineering)'
                else:
                    selected_modules = P2_DSML_BEGINNER_MODULES
                    track_label = 'Beginner Track (Data Analytics, Python & Business ML)'
            except Exception:
                selected_modules = P2_DSML_BEGINNER_MODULES
                track_label = 'Beginner Track (Data Analytics, Python & Business ML)'

        return {
            'program_name': p_data['program_name'],
            'catalogue_url': p_data['catalogue_url'],
            'top_hiring_companies': p_data.get('top_hiring_companies', []),
            'curriculum_modules': selected_modules,
            'track_label': track_label
        }

    # 4. Track-specific resolution for AI Forward Deployed Engineer (P3)
    if p_code == 'P3_FDE':
        return {
            'program_name': p_data['program_name'],
            'catalogue_url': p_data['catalogue_url'],
            'top_hiring_companies': p_data.get('top_hiring_companies', []),
            'curriculum_modules': P3_FDE_MODULES,
            'track_label': str(track_name) if track_name else 'Enterprise AI Integration & Client Systems Track'
        }

    # For other programs (P4, P5), return their structured curriculum modules
    return {
        'program_name': p_data['program_name'],
        'catalogue_url': p_data['catalogue_url'],
        'top_hiring_companies': p_data.get('top_hiring_companies', []),
        'curriculum_modules': p_data.get('curriculum_modules', []),
        'track_label': str(track_name) if track_name else 'Standard Track'
    }
