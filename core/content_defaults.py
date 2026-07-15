DEFAULT_PERSONA = {
    "heading": "Engineering Agentic Intelligence",
    "description": (
        "I'm Muhammad Abrar, an AI Automation Engineer merging backend precision with "
        "agentic intelligence. I don't just build software; I build systems that reason, "
        "retrieve, and act on their own."
    ),
    "image_role_label": "AI Automation Engineer",
}

DEFAULT_PHILOSOPHY = [
    (
        "I build production systems where Django, Next.js, and large language models meet "
        "RAG pipelines that actually retrieve the right answer, agents that take real actions "
        "instead of just chatting, and automations that remove hours of manual work from real "
        "businesses."
    ),
    (
        "Whether it's a knowledge-base chatbot, a voice-driven booking flow, or a "
        "denial-management agent that writes and sends insurance appeals on its own, I bring "
        "backend depth and AI fluency to every project — turning \"wouldn't it be cool if...\" "
        "into something a business runs on every day."
    ),
]

DEFAULT_SKILLS = [
    {
        "order": 1,
        "skill_id": "01",
        "title": "AI Automation",
        "subtitle": "Agentic Systems & LLM Orchestration",
        "proficiency": 90,
        "color": "#a855f7",
        "icon": "Bot",
        "tags": ["LangChain", "Gemini API", "Multi-Agent Workflows"],
    },
    {
        "order": 2,
        "skill_id": "02",
        "title": "Backend Engineering",
        "subtitle": "Full-Stack Development",
        "proficiency": 92,
        "color": "#06b6d4",
        "icon": "CodeXml",
        "tags": ["Django", "DRF", "Next.js"],
    },
    {
        "order": 3,
        "skill_id": "03",
        "title": "RAG & Vector Search",
        "subtitle": "Retrieval Systems & Embeddings",
        "proficiency": 88,
        "color": "#3b82f6",
        "icon": "Search",
        "tags": ["FAISS", "Embeddings", "Semantic Search"],
    },
    {
        "order": 4,
        "skill_id": "04",
        "title": "Workflow Automation",
        "subtitle": "Process & Pipeline Automation",
        "proficiency": 85,
        "color": "#ec4899",
        "icon": "Workflow",
        "tags": ["n8n", "API Integration", "Background Jobs"],
    },
    {
        "order": 5,
        "skill_id": "05",
        "title": "Web Scraping & Data Extraction",
        "subtitle": "Automated Data Collection",
        "proficiency": 85,
        "color": "#f59e0b",
        "icon": "ScanSearch",
        "tags": ["Selenium", "BeautifulSoup", "Anti-Detection"],
    },
    {
        "order": 6,
        "skill_id": "06",
        "title": "Data & Analytics",
        "subtitle": "Data Science & Visualization",
        "proficiency": 80,
        "color": "#10b981",
        "icon": "BarChart3",
        "tags": ["Pandas", "SQL", "Plotly"],
    },
    {
        "order": 7,
        "skill_id": "07",
        "title": "Cloud & Deployment",
        "subtitle": "Infrastructure & Storage",
        "proficiency": 78,
        "color": "#6366f1",
        "icon": "Cloud",
        "tags": ["Railway", "S3", "Cloudinary"],
    },
    {
        "order": 8,
        "skill_id": "08",
        "title": "API & LLM Integration",
        "subtitle": "Third-Party & Model APIs",
        "proficiency": 88,
        "color": "#ef4444",
        "icon": "PlugZap",
        "tags": ["REST APIs", "Gemini", "OAuth"],
    },
]

DEFAULT_PROJECTS = [
    {
        "order": 1,
        "slug": "ai-knowledge-base-chatbot-platform",
        "title": "AI Knowledge Base & Chatbot Platform",
        "year": 2026,
        "short_description": (
            "A Django + Next.js platform that turns unstructured sources into a searchable "
            "knowledge base powering custom chatbots."
        ),
        "architectural_vision": (
            "A Django + Next.js platform that turns unstructured sources — files, web pages, "
            "YouTube transcripts — into a searchable knowledge base powering custom chatbots. "
            "Background ingestion pipelines handle crawling, cleaning, and transcript extraction, "
            "while FAISS-backed embeddings drive fast, relevant retrieval at query time."
        ),
        "tags": ["Django", "Next.js", "LangChain", "FAISS", "Python"],
        "icon": "Network",
        "color": "#a855f7",
        "featured": True,
        "timeline": "5 weeks",
        "lead_role": "AI Automation Engineer",
        "environment": "Web / API",
        "goal": (
            "Give businesses a way to turn scattered content into a chatbot that actually knows "
            "their material, without manual data wrangling."
        ),
        "result": (
            "Delivered a production-ready RAG pipeline with resilient background processing, "
            "error-safe retries, and a dashboard exposing chatbot analytics — messages handled, "
            "answer rate, and estimated time saved."
        ),
    },
    {
        "order": 2,
        "slug": "dental-billing-ai-agent",
        "title": "Dental Billing AI Agent",
        "year": 2026,
        "short_description": (
            "A Django-based document intelligence system that reads dental billing documents "
            "and drafts professional appeal letters automatically."
        ),
        "architectural_vision": (
            "A Django-based document intelligence system that reads dental billing documents — "
            "EOPs, EOBs, pre-treatments — detects denied procedures automatically, and drafts "
            "professional appeal letters without human intervention."
        ),
        "tags": ["Django", "Gemini API", "Python", "Document AI"],
        "icon": "Activity",
        "color": "#06b6d4",
        "featured": True,
        "timeline": "6 weeks",
        "lead_role": "AI Automation Engineer",
        "environment": "Web / Document AI",
        "goal": (
            "Remove the fully manual step of reviewing denials and writing appeal letters, "
            "which was consuming hours of staff time per claim batch."
        ),
        "result": (
            "Shipped an end-to-end denial-management pipeline: automated extraction, "
            "AI-generated appeal letters, and direct email dispatch to insurance companies — "
            "reducing the process to a background job."
        ),
    },
    {
        "order": 3,
        "slug": "voice-enabled-event-booking-system",
        "title": "Voice-Enabled Event Booking System",
        "year": 2026,
        "short_description": (
            "A Next.js and Django application that lets customers book events entirely through "
            "natural voice conversation."
        ),
        "architectural_vision": (
            "A Next.js and Django application that lets customers book events entirely through "
            "natural voice conversation, powered by the Gemini Live API with real-time audio "
            "streaming and live availability checks."
        ),
        "tags": ["Next.js", "Django", "Gemini Live API", "WebSockets"],
        "icon": "HandMetal",
        "color": "#3b82f6",
        "featured": True,
        "timeline": "4 weeks",
        "lead_role": "AI/ML Engineer",
        "environment": "Web / Voice",
        "goal": (
            "Replace multi-step booking forms with a conversational, voice-first flow that "
            "feels closer to talking to a host than filling out a form."
        ),
        "result": (
            "Delivered a fully voice-driven booking experience — menu and cuisine selection, "
            "real-time availability, and confirmation — handled end to end by the AI agent."
        ),
    },
    {
        "order": 4,
        "slug": "wordpress-seo-content-automation",
        "title": "WordPress SEO & Content Automation",
        "year": 2025,
        "short_description": (
            "A Django automation tool connecting Google Keyword Planner and WordPress to automate "
            "SEO content workflows."
        ),
        "architectural_vision": (
            "A Django automation tool that connects the Google Keyword Planner API and WordPress "
            "REST API to close the loop between keyword research and content publishing — "
            "identifying gaps, rewriting content with AI, and syncing it live."
        ),
        "tags": ["Django", "WordPress REST API", "Google Keyword Planner API", "Python"],
        "icon": "Layers",
        "color": "#10b981",
        "featured": True,
        "timeline": "3 weeks",
        "lead_role": "AI Automation Engineer",
        "environment": "Web / API",
        "goal": (
            "Automate the repetitive SEO content cycle — research, rewrite, publish — so content "
            "teams stop doing it by hand for every page."
        ),
        "result": (
            "Delivered a pipeline that performs keyword-gap analysis, AI-rewrites existing content "
            "while preserving meaning, and auto-publishes updates directly to WordPress via "
            "secure admin credentials."
        ),
    },
    {
        "order": 5,
        "slug": "web-scraper-social-media-automation",
        "title": "Web Scraper & Social Media Automation",
        "year": 2025,
        "short_description": (
            "A Django platform combining scraping, generative AI, and the Facebook Graph API "
            "for automated social content."
        ),
        "architectural_vision": (
            "A Django platform combining Selenium/BeautifulSoup scraping, generative AI, and the "
            "Facebook Graph API to turn raw search data into scheduled, on-brand social content."
        ),
        "tags": [
            "Django",
            "Selenium",
            "BeautifulSoup",
            "Gemini API",
            "Facebook Graph API",
        ],
        "icon": "Rocket",
        "color": "#8b5cf6",
        "featured": True,
        "timeline": "4 weeks",
        "lead_role": "AI Automation Engineer",
        "environment": "Web / API",
        "goal": (
            "Automate content marketing end to end — from sourcing raw data to publishing "
            "finished posts — without a human touching each step."
        ),
        "result": (
            "Delivered a scraping service with anti-detection handling, Gemini-powered post "
            "generation, and automated scheduling/publishing directly to social pages."
        ),
    },
    {
        "order": 6,
        "slug": "pdf-question-answering-app",
        "title": "PDF Question-Answering App",
        "year": 2025,
        "short_description": (
            "A Streamlit application that parses PDF documents and enables natural language "
            "querying with Gemini 2.0 Flash."
        ),
        "architectural_vision": (
            "A Streamlit application that parses PDF documents and enables natural language "
            "querying over their contents using Gemini 2.0 Flash, built for fast, interactive "
            "document exploration."
        ),
        "tags": ["Streamlit", "Gemini 2.0 Flash", "Python", "PDF Parsing"],
        "icon": "Cpu",
        "color": "#f43f5e",
        "featured": True,
        "timeline": "2 weeks",
        "lead_role": "AI/ML Engineer",
        "environment": "Web / API",
        "goal": (
            "Let users ask plain-language questions of dense PDFs instead of manually searching "
            "through pages."
        ),
        "result": (
            "Delivered a lightweight, responsive Q&A tool with accurate document parsing and "
            "near-instant AI-generated answers."
        ),
    },
    {
        "order": 7,
        "slug": "priceoye-product-scraper",
        "title": "PriceOye Product Scraper",
        "year": 2025,
        "short_description": (
            "A Streamlit-based scraping tool that pulls live product data from PriceOye for "
            "structured price comparison."
        ),
        "architectural_vision": (
            "A Streamlit-based scraping tool that pulls live product data from PriceOye using "
            "BeautifulSoup, with category selection and pagination support for structured "
            "price comparison."
        ),
        "tags": ["Streamlit", "BeautifulSoup", "Python", "Pandas"],
        "icon": "Building2",
        "color": "#eab308",
        "featured": True,
        "timeline": "1 week",
        "lead_role": "Backend Developer",
        "environment": "Web / Data",
        "goal": (
            "Track pricing trends and enable quick product comparisons without manually browsing "
            "the site."
        ),
        "result": (
            "Delivered a working scraper with a clean DataFrame output, ready for price-tracking "
            "and comparison workflows."
        ),
    },
]
