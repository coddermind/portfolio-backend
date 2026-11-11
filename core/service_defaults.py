"""Seed copy for freelance services. Idempotent: update/create by slug, never delete."""

DEFAULT_SERVICES = [
    {
        "slug": "ai-automation",
        "title": "AI Automation & Workflow Automation",
        "tagline": "Replace copy-paste work with systems that run the same way every time.",
        "description": (
            "If your team still moves data between tools by hand — exporting CSVs, updating "
            "spreadsheets, chasing status in three dashboards — that work is slow, easy to "
            "get wrong, and expensive to scale.\n\n"
            "I design and build automations that sit on top of the tools you already use. "
            "Typical work includes scheduled jobs, webhook-driven flows, document intake, "
            "and human-in-the-loop steps where a person should still approve before anything "
            "is sent or published.\n\n"
            "You get a working pipeline, not a slide deck: something you can run, monitor, "
            "and hand to your team with clear failure paths when an API is down or an input "
            "is messy."
        ),
        "icon": "account_tree",
        "cta_text": "Tell me the workflow you want off your plate",
        "tech_stack": ["Python", "Django", "n8n", "REST APIs", "Background Jobs"],
        "order": 0,
        "is_published": True,
        "deliverables": [
            {
                "order": 0,
                "title": "Mapped workflow",
                "description": "Current steps, systems involved, and where a person still needs to approve.",
            },
            {
                "order": 1,
                "title": "Production automation",
                "description": "A scheduled or event-driven pipeline that moves data and triggers the next action.",
            },
            {
                "order": 2,
                "title": "Error handling & retries",
                "description": "Failed jobs surface clearly instead of failing silently overnight.",
            },
            {
                "order": 3,
                "title": "Handoff notes",
                "description": "How to run it, what to watch, and how to change a prompt, template, or destination.",
            },
        ],
        "process_steps": [
            {
                "order": 0,
                "title": "Walk the real process",
                "description": "We start from how the work is done today — tools, edge cases, and who owns each step.",
            },
            {
                "order": 1,
                "title": "Design the happy path and the failures",
                "description": "Agree what “done” looks like, and what should happen when an input is incomplete.",
            },
            {
                "order": 2,
                "title": "Build against live APIs",
                "description": "Integrate the actual systems, with logging so you can see each run.",
            },
            {
                "order": 3,
                "title": "Run together, then hand off",
                "description": "You watch it work on real data before I leave you with runbooks.",
            },
        ],
        "use_cases": [
            {
                "order": 0,
                "title": "Intake that used to be email",
                "description": "Forms, documents, or leads land in a structured queue instead of an inbox.",
            },
            {
                "order": 1,
                "title": "Status that used to be a spreadsheet",
                "description": "Updates flow from the source of truth into Slack, email, or a dashboard.",
            },
            {
                "order": 2,
                "title": "Publishing that used to be copy-paste",
                "description": "Approved content syncs to WordPress, a CMS, or social APIs without a manual hop.",
            },
        ],
        "faqs": [
            {
                "order": 0,
                "question": "Do I need n8n, or do you write this in Django?",
                "answer": (
                    "Either. Lightweight, visual flows often live in n8n. Anything that needs "
                    "a real data model, permissions, or a long-running worker is better as a "
                    "Django service. I will recommend based on the workflow, not a preferred tool."
                ),
            },
            {
                "order": 1,
                "question": "What if one of our tools has a flaky API?",
                "answer": (
                    "Then the automation has to expect that: retries, idempotent writes, and a "
                    "place to inspect failed runs. I will not pretend every vendor API is reliable."
                ),
            },
            {
                "order": 2,
                "question": "Will this fully replace my team?",
                "answer": (
                    "No. The useful pattern is taking repetitive steps off people so they can "
                    "review exceptions and make decisions. Fully unattended send/publish is only "
                    "in scope when you explicitly want it."
                ),
            },
        ],
    },
    {
        "slug": "ai-agents",
        "title": "Agentic AI for Business Operations",
        "tagline": "Agents that call your APIs, respect roles, and confirm before they create anything.",
        "description": (
            "A chatbot that only talks is a demo. An agent that books, dispatches, drafts, "
            "or updates records — using the same APIs your staff already use — is an operations tool.\n\n"
            "I build role-aware agents with tool calling: the model chooses a structured action, "
            "your backend executes it, and unsafe writes wait for confirmation. Sessions stay "
            "stateful so a multi-step booking or intake does not reset mid-conversation.\n\n"
            "This is the same shape of work as the operations copilots and document agents in "
            "my portfolio: Django (or a similar backend), an LLM with function calling, and "
            "hard permission checks so a driver, customer, or junior user cannot trigger admin actions."
        ),
        "icon": "smart_toy",
        "cta_text": "Describe the job you want an agent to do",
        "tech_stack": [
            "Django",
            "OpenAI",
            "Gemini API",
            "Tool Calling",
            "LangChain",
            "Redis",
        ],
        "order": 1,
        "is_published": True,
        "deliverables": [
            {
                "order": 0,
                "title": "Scoped tools",
                "description": "Each action the agent may take is a real API method with inputs you can audit.",
            },
            {
                "order": 1,
                "title": "Role and permission gates",
                "description": "What the agent can see and do is tied to the signed-in user’s role, not the prompt.",
            },
            {
                "order": 2,
                "title": "Confirm-before-write flows",
                "description": "Creates and updates show a draft first when the action is hard to undo.",
            },
            {
                "order": 3,
                "title": "Embedded or standalone UI",
                "description": "A chat surface in your admin, a customer page, or a small iframe — whichever fits.",
            },
        ],
        "process_steps": [
            {
                "order": 0,
                "title": "List the actions that matter",
                "description": "We write down the verbs — look up, draft, create, assign — and who is allowed to run them.",
            },
            {
                "order": 1,
                "title": "Wire tools to your backend",
                "description": "Each tool hits a real endpoint with the user’s credentials, not a shared god-mode key where we can avoid it.",
            },
            {
                "order": 2,
                "title": "Tune routing and fallbacks",
                "description": "Intent routing for common jobs; a slower tool-calling path for the messy ones.",
            },
            {
                "order": 3,
                "title": "Test with real roles",
                "description": "We sit down as admin, staff, and a restricted user and try to break the boundaries.",
            },
        ],
        "use_cases": [
            {
                "order": 0,
                "title": "Internal ops copilot",
                "description": "Staff ask “what’s open for this customer?” and get an answer from live data, not a wiki.",
            },
            {
                "order": 1,
                "title": "Guided create flows",
                "description": "Bookings, tickets, or work orders drafted in chat, then confirmed before they hit the database.",
            },
            {
                "order": 2,
                "title": "Document-to-action agents",
                "description": "A PDF or email in; a structured record, draft letter, or task list out.",
            },
        ],
        "faqs": [
            {
                "order": 0,
                "question": "Can the agent send email or WhatsApp on its own?",
                "answer": (
                    "It can, if you want that. Default is a human approve step before anything "
                    "leaves the building. Unguarded auto-send is a product decision, not a default."
                ),
            },
            {
                "order": 1,
                "question": "Which model do you use?",
                "answer": (
                    "Whatever fits the job and your budget — OpenAI, Gemini, or another provider "
                    "behind one tool interface. I do not lock the design to a single vendor."
                ),
            },
            {
                "order": 2,
                "question": "Will it hallucinate a booking that does not exist?",
                "answer": (
                    "The model can still invent language. Writes go through your API and your "
                    "validation, and confirm-before-create is there so a bad draft does not become "
                    "a real record."
                ),
            },
        ],
    },
    {
        "slug": "rag-ai-chatbots",
        "title": "RAG & AI Chatbots on Your Data",
        "tagline": "Answers grounded in your files, pages, and transcripts — with a path back to the source.",
        "description": (
            "Generic chatbots guess. A retrieval system looks up the chunks that actually "
            "belong to your business, then generates an answer from those chunks.\n\n"
            "I build knowledge-base chatbots on Django + embeddings (FAISS in the projects "
            "you will see on this site): ingest files, URLs, and transcripts, chunk them, "
            "index them, and serve a chat UI with citations. Background jobs handle crawl, "
            "resync, and retries so a bad PDF does not take down the whole index.\n\n"
            "If you need multi-tenant bots or an internal playground for your team, that is "
            "in scope. What is not in scope is promising “zero hallucination” — retrieval "
            "reduces made-up answers; it does not make a language model omniscient."
        ),
        "icon": "manage_search",
        "cta_text": "Show me the documents the bot should know",
        "tech_stack": ["Django", "Next.js", "LangChain", "FAISS", "Embeddings", "Python"],
        "order": 2,
        "is_published": True,
        "deliverables": [
            {
                "order": 0,
                "title": "Ingestion pipeline",
                "description": "Files, site pages, and optional YouTube transcripts into a searchable index.",
            },
            {
                "order": 1,
                "title": "Retrieval + answer API",
                "description": "Hybrid search, optional re-ranking, and a streamed or standard chat response.",
            },
            {
                "order": 2,
                "title": "Source-aware replies",
                "description": "Answers that point back to the passage or page they came from.",
            },
            {
                "order": 3,
                "title": "Admin for sources",
                "description": "Add, resync, or drop documents without redeploying the app.",
            },
        ],
        "process_steps": [
            {
                "order": 0,
                "title": "Inventory the corpus",
                "description": "What should the bot know, what must it never see, and how often does it change?",
            },
            {
                "order": 1,
                "title": "Chunk and index",
                "description": "Choose chunk size, metadata, and an embedding model that fits the content.",
            },
            {
                "order": 2,
                "title": "Evaluate on real questions",
                "description": "We try the questions your team actually asks — not a vanity demo prompt.",
            },
            {
                "order": 3,
                "title": "Ship the chat surface",
                "description": "Dashboard or embed, with basic usage so you can see what people asked.",
            },
        ],
        "use_cases": [
            {
                "order": 0,
                "title": "Internal knowledge bot",
                "description": "Policies, runbooks, and product docs in one place instead of a buried drive.",
            },
            {
                "order": 1,
                "title": "Customer support assist",
                "description": "Draft answers for your team from the help center, with the source attached.",
            },
            {
                "order": 2,
                "title": "Site or docs Q&A",
                "description": "A public chat that stays inside the pages you chose to index.",
            },
        ],
        "faqs": [
            {
                "order": 0,
                "question": "Can it read our private Google Drive / Notion overnight?",
                "answer": (
                    "If there is an API and you grant access, yes. I will not scrape a logged-in "
                    "product in a way that violates its terms. We pick an official export or API first."
                ),
            },
            {
                "order": 1,
                "question": "Do you train a custom model on our data?",
                "answer": (
                    "Usually no. RAG keeps your content in an index and retrieves it at question time. "
                    "Fine-tuning is a different, heavier project and only worth it for a clear gap retrieval cannot cover."
                ),
            },
            {
                "order": 2,
                "question": "What happens when a document is updated?",
                "answer": (
                    "The pipeline re-embeds that source on resync or a schedule. Stale chunks are the "
                    "usual failure mode if nobody reruns ingestion — that is why admin resync is part of the build."
                ),
            },
        ],
    },
    {
        "slug": "api-integrations",
        "title": "API Integrations",
        "tagline": "OAuth, webhooks, and retries so your tools stay in sync without a person in the middle.",
        "description": (
            "Most “integration” pain is not the happy-path GET. It is tokens that expire, "
            "webhooks that fire twice, rate limits, and two systems that disagree on what "
            "an ID means.\n\n"
            "I connect third-party APIs to a Django (or similar) backend: OAuth2, signed "
            "webhooks, background workers, and a clear mapping between your records and theirs. "
            "That includes LLM providers, WordPress, Shopify Admin, Google APIs, email/SMS "
            "providers, and Meta Graph-style social APIs — the same families of integrations "
            "already in this portfolio.\n\n"
            "You should be able to see the last successful sync, the last error, and replay "
            "a failed event without me SSH-ing into the server."
        ),
        "icon": "api",
        "cta_text": "List the two systems that should talk",
        "tech_stack": [
            "Django",
            "REST APIs",
            "OAuth",
            "Webhooks",
            "Redis",
            "Python",
        ],
        "order": 3,
        "is_published": True,
        "deliverables": [
            {
                "order": 0,
                "title": "Authenticated connection",
                "description": "OAuth or API-key handling with token refresh, not a key pasted in a spreadsheet.",
            },
            {
                "order": 1,
                "title": "Sync or webhook worker",
                "description": "Inbound events and outbound updates with idempotency so retries do not duplicate work.",
            },
            {
                "order": 2,
                "title": "Field mapping",
                "description": "A documented map of your objects to theirs, including the ugly optional fields.",
            },
            {
                "order": 3,
                "title": "Failure visibility",
                "description": "Logs or an admin list of failed payloads you can inspect and retry.",
            },
        ],
        "process_steps": [
            {
                "order": 0,
                "title": "Read the real API, not the marketing page",
                "description": "Scopes, rate limits, sandbox vs live, and whether webhooks are actually reliable.",
            },
            {
                "order": 1,
                "title": "Model the mapping",
                "description": "Agree what a “customer” or “order” means on both sides before writing code.",
            },
            {
                "order": 2,
                "title": "Implement and soak in sandbox",
                "description": "Duplicate events, expired tokens, and partial payloads get tests, not hope.",
            },
            {
                "order": 3,
                "title": "Go live with a rollback",
                "description": "A way to pause the worker if the vendor has a bad day.",
            },
        ],
        "use_cases": [
            {
                "order": 0,
                "title": "CMS or commerce sync",
                "description": "WordPress or Shopify content and catalog updates without copy-paste.",
            },
            {
                "order": 1,
                "title": "Lead and message channels",
                "description": "Email or WhatsApp providers wired into your own data model, with inbound threading.",
            },
            {
                "order": 2,
                "title": "LLM vendor swap",
                "description": "One internal tool interface so you can change model providers without rewriting the product.",
            },
        ],
        "faqs": [
            {
                "order": 0,
                "question": "The vendor has no official API. Can you scrape it?",
                "answer": (
                    "Scraping is a last resort and it breaks. If the product is core to your "
                    "business, we push for an API or export. I will say no to brittle login-scraping "
                    "of a tool that forbids it."
                ),
            },
            {
                "order": 1,
                "question": "Do you need our production credentials on day one?",
                "answer": (
                    "No. Sandbox or a restricted key first. Production credentials stay in your "
                    "environment (or a secret manager), not in my laptop notes."
                ),
            },
            {
                "order": 2,
                "question": "What if the vendor changes their payload?",
                "answer": (
                    "Then the worker should fail loudly on unknown required fields, not write garbage. "
                    "Versioning and a dead-letter view are part of doing this for real."
                ),
            },
        ],
    },
    {
        "slug": "django-backend-development",
        "title": "Python, Django & DRF Backends",
        "tagline": "APIs, admin, and data models you can still change six months later.",
        "description": (
            "A frontend is only as trustworthy as the API behind it. I build Django and "
            "Django REST Framework backends: auth, permissions, background jobs, file storage, "
            "and an admin that a non-engineer can actually use.\n\n"
            "This is the core of almost every project on this site — public JSON APIs, "
            "superuser admin, Postgres, and media on object storage (Cloudflare R2 in production "
            "here). I care about boring things that keep products alive: migrations, clear "
            "error payloads, and not deleting customer data because a seed script was too aggressive.\n\n"
            "If you already have a Next.js or Nuxt app that is talking to a mess of serverless "
            "functions, I can put a proper domain model under it."
        ),
        "icon": "dns",
        "cta_text": "Send the API you wish you had",
        "tech_stack": [
            "Python",
            "Django",
            "Django REST Framework",
            "PostgreSQL",
            "Redis",
            "Cloudflare R2",
        ],
        "order": 4,
        "is_published": True,
        "deliverables": [
            {
                "order": 0,
                "title": "Domain models & migrations",
                "description": "Tables that match how the business talks, with migrations you can run on deploy.",
            },
            {
                "order": 1,
                "title": "REST API",
                "description": "Auth, permissions, and resource endpoints the frontend can depend on.",
            },
            {
                "order": 2,
                "title": "Admin for operators",
                "description": "List filters, inlines, and media uploads — not a raw table dump.",
            },
            {
                "order": 3,
                "title": "Deployable app",
                "description": "Gunicorn (or similar), env-based config, and migrate-on-deploy so Coolify/Docker hosts work.",
            },
        ],
        "process_steps": [
            {
                "order": 0,
                "title": "Agree the resources",
                "description": "What is a user, a project, an order — and who may read or write each field.",
            },
            {
                "order": 1,
                "title": "Schema first, then endpoints",
                "description": "Models and migrations before a thicket of one-off views.",
            },
            {
                "order": 2,
                "title": "Wire storage and jobs",
                "description": "Media, email, and background work using the host you already have.",
            },
            {
                "order": 3,
                "title": "Harden for production",
                "description": "CORS, HTTPS behind the proxy, and a health endpoint your host can ping.",
            },
        ],
        "use_cases": [
            {
                "order": 0,
                "title": "Product API for a JS frontend",
                "description": "Next.js or Nuxt talks to a versioned Django API instead of mixing business logic in the browser.",
            },
            {
                "order": 1,
                "title": "Operator admin",
                "description": "Your team publishes content, reviews messages, or manages catalog data without a deploy.",
            },
            {
                "order": 2,
                "title": "Rebuild a fragile prototype",
                "description": "A notebook or no-code stack that needs real auth, files, and a database.",
            },
        ],
        "faqs": [
            {
                "order": 0,
                "question": "Can you work on an existing Django app?",
                "answer": (
                    "Yes. I would rather extend a healthy codebase than rewrite it. A rewrite is "
                    "only on the table if the current app cannot be migrated safely."
                ),
            },
            {
                "order": 1,
                "question": "Do you use Django Ninja / FastAPI instead?",
                "answer": (
                    "Django + DRF is the default because admin, auth, and ORM come with it. "
                    "FastAPI is fine for a narrow service if that is already your stack."
                ),
            },
            {
                "order": 2,
                "question": "Will you support the server after launch?",
                "answer": (
                    "Launch includes a working deploy path. Ongoing retainers are a separate "
                    "conversation — I will not vanish on deploy day, and I will not pretend "
                    "unlimited ops is included in a build quote."
                ),
            },
        ],
    },
    {
        "slug": "nextjs-nuxt-websites",
        "title": "Next.js & Nuxt Website Development",
        "tagline": "Fast marketing and product UIs that talk to a real backend — not a folder of static lies.",
        "description": (
            "I build Next.js and Nuxt frontends for sites that have to do something: "
            "case studies, dashboards, voice or chat widgets, and admin consoles that "
            "consume a Django API.\n\n"
            "The public site you are on is this pattern: a JavaScript frontend, JSON from "
            "the backend, and media from object storage. I care about loading the data "
            "that is actually published, sensible routing by slug, and not hard-coding "
            "copy that your admin cannot edit.\n\n"
            "I am not a brand studio. If you need illustration systems and a 40-page design "
            "ops wiki, hire that separately. If you need a sharp site that ships against an "
            "API and can be updated without a rebuild for every typo, that is this service."
        ),
        "icon": "web",
        "cta_text": "Share the pages that have to exist at launch",
        "tech_stack": ["Next.js", "Nuxt", "Django REST Framework", "REST APIs"],
        "order": 5,
        "is_published": True,
        "deliverables": [
            {
                "order": 0,
                "title": "Routed frontend",
                "description": "Pages for home, services, project/case-study detail, and whatever else is in scope.",
            },
            {
                "order": 1,
                "title": "API-backed content",
                "description": "Copy and media come from the backend so you can edit them without a deploy for every change.",
            },
            {
                "order": 2,
                "title": "Forms that actually send",
                "description": "Contact or intake wired to the backend, with basic validation and spam-aware handling.",
            },
            {
                "order": 3,
                "title": "Production build",
                "description": "Environment-based API URL, preview, and a deploy path on your host.",
            },
        ],
        "process_steps": [
            {
                "order": 0,
                "title": "Sitemap and components",
                "description": "Which pages, which blocks, and which data is CMS/API vs hard-coded chrome.",
            },
            {
                "order": 1,
                "title": "Build against the real contract",
                "description": "The frontend uses the same JSON the public API already returns — no mock that drifts.",
            },
            {
                "order": 2,
                "title": "States that usually get skipped",
                "description": "Empty, loading, unpublished, and 404 — not only the happy screenshot.",
            },
            {
                "order": 3,
                "title": "Launch checklist",
                "description": "Metadata, production env, and a pass on mobile widths that matter to your traffic.",
            },
        ],
        "use_cases": [
            {
                "order": 0,
                "title": "Portfolio or agency site",
                "description": "Services and work driven from an admin, not a markdown folder only you can edit.",
            },
            {
                "order": 1,
                "title": "Product dashboard",
                "description": "Authenticated UI on top of the Django API: queues, chat, or content tools.",
            },
            {
                "order": 2,
                "title": "Marketing site in front of an existing API",
                "description": "A public Next.js or Nuxt layer without rewriting the backend.",
            },
        ],
        "faqs": [
            {
                "order": 0,
                "question": "Next.js or Nuxt — which do you recommend?",
                "answer": (
                    "Match the team that will maintain it. I work in both. If you have no preference "
                    "and the backend is Django, either is fine; we pick based on hosting and any "
                    "existing code."
                ),
            },
            {
                "order": 1,
                "question": "Do you do visual design from a blank file?",
                "answer": (
                    "I can implement a clear layout and a consistent system. If you already have "
                    "Figma, even better. I will not invent a full brand identity as part of an "
                    "engineering engagement."
                ),
            },
            {
                "order": 2,
                "question": "Can this be a static export?",
                "answer": (
                    "Some pages can. Anything that must reflect unpublished/published state from "
                    "the API should fetch at runtime or on a short revalidate — otherwise your "
                    "admin edits will not show up."
                ),
            },
        ],
    },
    {
        "slug": "shopify-technical-seo-automation",
        "title": "Shopify & Technical SEO Automation",
        "tagline": "Find and fix the technical SEO issues that hide your catalog — then keep watching.",
        "description": (
            "Large Shopify catalogs collect broken redirects, missing alt text, thin or duplicate "
            "metadata, and schema that does not match the page. Doing that by hand across thousands "
            "of products is slow and easy to drop.\n\n"
            "I build an audit-and-fix pipeline on Django plus the Shopify Admin API: crawl the "
            "store, surface technical issues with a priority order, apply approved fixes "
            "(redirects, schema, alt text, titles and descriptions), and re-check on a schedule.\n\n"
            "Live writes go through a human approval step unless you explicitly want them "
            "unattended. This is technical SEO operations — crawl health, structured data, "
            "and on-page completeness. It is not a ranking package, and I will not promise "
            "positions, traffic, or revenue."
        ),
        "icon": "query_stats",
        "cta_text": "Send a store URL and the issues you already see",
        "tech_stack": [
            "Django",
            "Shopify Admin API",
            "Nuxt",
            "Background Jobs",
            "Python",
        ],
        "order": 6,
        "is_published": True,
        "deliverables": [
            {
                "order": 0,
                "title": "Catalog and URL audit",
                "description": "A pass over products, collections, and key templates for redirects, metadata, alt text, and schema.",
            },
            {
                "order": 1,
                "title": "Prioritised issue list",
                "description": "What to fix first — broken paths and missing required fields ahead of polish.",
            },
            {
                "order": 2,
                "title": "Approved fix application",
                "description": "Redirects, schema, alt text, and metadata written back through the Shopify Admin API after you sign off.",
            },
            {
                "order": 3,
                "title": "Scheduled re-check",
                "description": "A recurring crawl so new 404s and blank fields show up without another manual sweep.",
            },
        ],
        "process_steps": [
            {
                "order": 0,
                "title": "Connect a staff or custom app",
                "description": "Shopify Admin API access with the scopes the audit and the fixes actually need — nothing extra.",
            },
            {
                "order": 1,
                "title": "Crawl and classify",
                "description": "Collect URLs, status codes, titles, descriptions, alt text, and schema; group by issue type.",
            },
            {
                "order": 2,
                "title": "Review before write",
                "description": "You see the proposed redirects and field changes. Nothing hits the live store until that step is done.",
            },
            {
                "order": 3,
                "title": "Apply and monitor",
                "description": "Approved mutations go out in batches; the scheduler watches for regressions.",
            },
        ],
        "use_cases": [
            {
                "order": 0,
                "title": "Catalog with missing media text",
                "description": "Product images shipping without alt text, updated in bulk after a review pass.",
            },
            {
                "order": 1,
                "title": "Theme or app leftover 404s",
                "description": "Old collection and product paths mapped to current URLs instead of dying in Search Console.",
            },
            {
                "order": 2,
                "title": "Schema that does not match the page",
                "description": "Product and collection structured data brought in line with what the template actually renders.",
            },
        ],
        "faqs": [
            {
                "order": 0,
                "question": "Will this get me to page one?",
                "answer": (
                    "No, and I will not sell it that way. This work makes the store easier for "
                    "crawlers to understand and removes technical blockers. Rankings depend on "
                    "content, links, competition, and Google — none of which I control."
                ),
            },
            {
                "order": 1,
                "question": "Can it edit live products without me?",
                "answer": (
                    "Only if you ask for that. The default is a review queue. Unattended writes "
                    "to a live catalog are a product decision, not a default."
                ),
            },
            {
                "order": 2,
                "question": "Does this replace a content SEO retainer?",
                "answer": (
                    "No. It does not write blog posts, build links, or manage ads. It is the "
                    "technical layer: redirects, schema, alt text, metadata, and a repeating audit."
                ),
            },
        ],
    },
]


CHILD_RELATIONS = (
    ("deliverables", "core", "ServiceDeliverable", ("title", "description")),
    ("process_steps", "core", "ServiceProcessStep", ("title", "description")),
    ("use_cases", "core", "ServiceUseCase", ("title", "description")),
    ("faqs", "core", "ServiceFAQ", ("question", "answer")),
)


def seed_services(apps=None, *, overwrite=True) -> dict:
    """Create or update services by slug. Never deletes services or unrelated rows."""
    from django.apps import apps as django_apps

    apps = apps or django_apps
    Service = apps.get_model("core", "Service")

    created = 0
    updated = 0
    skipped = 0

    for payload in DEFAULT_SERVICES:
        children = {
            key: payload[key]
            for key, *_ in CHILD_RELATIONS
        }
        defaults = {
            "title": payload["title"],
            "tagline": payload["tagline"],
            "description": payload["description"],
            "tech_stack": payload["tech_stack"],
            "cta_text": payload["cta_text"],
            "icon": payload["icon"],
            "order": payload["order"],
            "is_published": payload["is_published"],
        }
        existing = Service.objects.filter(slug=payload["slug"]).first()
        if existing and not overwrite:
            skipped += 1
            continue
        _, was_created = Service.objects.update_or_create(
            slug=payload["slug"],
            defaults=defaults,
        )
        if was_created:
            created += 1
        else:
            updated += 1

        service = Service.objects.get(slug=payload["slug"])
        for key, _app, model_name, fields in CHILD_RELATIONS:
            Model = apps.get_model("core", model_name)
            for item in children[key]:
                item_defaults = {field: item[field] for field in fields}
                Model.objects.update_or_create(
                    service=service,
                    order=item["order"],
                    defaults=item_defaults,
                )

    return {
        "created": created,
        "updated": updated,
        "skipped": skipped,
        "total": len(DEFAULT_SERVICES),
    }
