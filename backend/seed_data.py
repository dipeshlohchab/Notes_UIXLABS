"""Seed script to populate MongoDB with ~50 realistic, diverse notes.
Can be executed directly: `python backend/seed_data.py`
"""
import os
from datetime import datetime, timedelta, timezone
from pymongo import MongoClient

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")

SEED_NOTES = [
    # 1-10: Software Architecture, Backend & Distributed Systems
    {
        "title": "FastAPI Performance Optimization & Async Best Practices",
        "body": "When building high-throughput APIs with FastAPI, ensure connection pooling with asyncpg or Motor. Use Pydantic v2 schemas for fast validation serialization. Offload CPU-heavy computation to Celery or background tasks, and keep route handlers non-blocking.",
        "days_ago": 1,
        "hours_ago": 2,
    },
    {
        "title": "MongoDB Indexing Strategies for Full-Text and Multi-Word Search",
        "body": "Compound indexes should follow the Equality, Sort, Range (ESR) rule. For multi-word text search, compound text indexes support weightings across title and body fields. Regular expressions with case-insensitivity can bypass indexes if not prefixed.",
        "days_ago": 2,
        "hours_ago": 4,
    },
    {
        "title": "React 19 Architecture: Server Components and Concurrent Mode",
        "body": "React 19 introduces Actions, useActionState, useOptimistic, and native document metadata. Transitioning from client-only state management to server components reduces bundle payload while boosting initial paint times.",
        "days_ago": 2,
        "hours_ago": 11,
    },
    {
        "title": "Microservices Communication: gRPC vs REST vs Event-Driven Pub/Sub",
        "body": "Synchronous inter-service calls often lead to cascading latency failures. For internal telemetry and RPCs, Protocol Buffers and gRPC offer lower overhead. For decoupling services, Kafka or RabbitMQ events ensure high resilience and eventual consistency.",
        "days_ago": 3,
        "hours_ago": 6,
    },
    {
        "title": "Designing Idempotent RESTful APIs",
        "body": "Idempotency keys (UUIDv4 sent in headers like Idempotency-Key) allow payment or order endpoints to safely retry on network drops. Store response payloads in Redis with a TTL of 24 hours to prevent duplicate state mutations.",
        "days_ago": 4,
        "hours_ago": 3,
    },
    {
        "title": "Redis Caching Patterns: Cache-Aside vs Write-Through",
        "body": "Cache-aside lets the application query cache first, and fetch from database on cache miss. Beware of cache stampedes using distributed locks or probabilistic early expiration (XFetch algorithm).",
        "days_ago": 5,
        "hours_ago": 8,
    },
    {
        "title": "Docker Multi-Stage Builds for Lean Python & Node Containers",
        "body": "Reduce container image size from 1.2GB to under 150MB by utilizing multi-stage Docker builds. Compile wheels and dependencies in a builder stage, then copy clean binaries into a distroless or alpine runtime environment.",
        "days_ago": 6,
        "hours_ago": 1,
    },
    {
        "title": "Kubernetes Pod Autoscaling and Zero-Downtime Deployments",
        "body": "Configure Horizontal Pod Autoscalers (HPA) targeting CPU utilization at 70% and custom Prometheus request rate metrics. Use rolling updates with maxSurge: 25% and maxUnavailable: 0 for seamless rollouts.",
        "days_ago": 7,
        "hours_ago": 5,
    },
    {
        "title": "PostgreSQL Query Optimization & EXPLAIN ANALYZE Breakdown",
        "body": "Run EXPLAIN (ANALYZE, BUFFERS) to detect sequential scans on large tables. Check whether planner estimates match actual rows. Create partial indexes for frequent filtered subsets such as status = 'ACTIVE'.",
        "days_ago": 8,
        "hours_ago": 14,
    },
    {
        "title": "WebSocket Architecture for Real-Time Collaborative Canvas",
        "body": "WebSockets maintain bi-directional full-duplex TCP channels. Combine with Conflict-free Replicated Data Types (CRDTs) like Yjs or Automerge to resolve concurrent editing conflicts without central master lock contention.",
        "days_ago": 9,
        "hours_ago": 2,
    },

    # 11-20: Frontend Engineering, CSS & UX Systems
    {
        "title": "Modern CSS Systems: OKLCH Colors, Fluid Typography & Container Queries",
        "body": "OKLCH delivers perceptual uniformity across dark and light modes, avoiding muddy gray gradients in color interpolation. Pair clamp() with viewport units for fluid typography that scales without rigid breakpoint snapping.",
        "days_ago": 10,
        "hours_ago": 7,
    },
    {
        "title": "Web Performance Checklist: Core Web Vitals & LCP Optimization",
        "body": "Largest Contentful Paint (LCP) must stay under 2.5 seconds. Preload critical hero images, self-host WOFF2 fonts with font-display: swap, and eliminate render-blocking CSS via critical inline extraction.",
        "days_ago": 11,
        "hours_ago": 3,
    },
    {
        "title": "Vite Build Pipeline: Plugins, Code Splitting & Manual Chunks",
        "body": "Configure rollupOptions in vite.config.js to split heavy vendor modules (like Three.js, Lucide, or Lodash) into isolated chunk caches. Leverage dynamic import() for route-based lazy loading.",
        "days_ago": 12,
        "hours_ago": 9,
    },
    {
        "title": "Accessibility (a11y) Guidelines for Interactive Component Design",
        "body": "Ensure 4.5:1 contrast ratios for standard text. Interactive elements require descriptive aria-labels, keyboard navigation via Tab and arrow keys, and clear :focus-visible outlines that meet WCAG 2.2 AA compliance.",
        "days_ago": 13,
        "hours_ago": 4,
    },
    {
        "title": "TypeScript 5.x Const Type Parameters & Satisfies Operator",
        "body": "The satisfies operator validates that an expression matches a type without widening its specific inferred types. Const type parameters on generic functions preserve literal types without needing 'as const' assertions.",
        "days_ago": 14,
        "hours_ago": 8,
    },
    {
        "title": "State Management Patterns: Zustand vs Redux Toolkit vs Signals",
        "body": "Zustand provides boilerplate-free minimal stores with selector-based re-rendering. Signals offer fine-grained reactivity directly in the DOM tree, bypassing full virtual DOM diffing for high-frequency updates.",
        "days_ago": 15,
        "hours_ago": 6,
    },
    {
        "title": "CSS Glassmorphism & Backdrop Filters Design Guide",
        "body": "Create translucent surfaces using background: rgba(255, 255, 255, 0.08) paired with backdrop-filter: blur(16px) saturate(180%). Add a subtle 1px border with rgba(255, 255, 255, 0.12) to create depth without flat borders.",
        "days_ago": 16,
        "hours_ago": 10,
    },
    {
        "title": "Micro-Animations and Spring Physics in Web UI",
        "body": "Cubic-bezier timing functions and spring physics give interfaces a tactile, responsive feel. Use transform and opacity exclusively to trigger GPU-accelerated compositing without re-triggering layout recalculations.",
        "days_ago": 17,
        "hours_ago": 5,
    },
    {
        "title": "PWA Implementation: Service Workers and Offline Notes Caching",
        "body": "Implement a Cache-First strategy for static assets and Stale-While-Revalidate for API responses. IndexedDB handles local drafts offline, syncing back with the server once navigator.onLine triggers.",
        "days_ago": 18,
        "hours_ago": 2,
    },
    {
        "title": "Tailwind vs Pure Vanilla CSS Design Systems: Comparative Analysis",
        "body": "While utility-first Tailwind speeds up prototyping, well-structured Vanilla CSS with CSS custom properties (variables) provides cleaner DOM markup, zero build tool lock-in, and superior runtime theming agility.",
        "days_ago": 19,
        "hours_ago": 12,
    },

    # 21-30: Productivity, Product Management & Workflows
    {
        "title": "Building a Second Brain: The PARA Organization Method",
        "body": "Organize notes into Projects (active with deadlines), Areas of responsibility (ongoing standards), Resources (topics of ongoing interest), and Archives (inactive items from the other three categories).",
        "days_ago": 20,
        "hours_ago": 4,
    },
    {
        "title": "Deep Work Protocols: Minimizing Context Switching and Shallow Tasks",
        "body": "Carve out unbroken 90-minute blocks for deep cognitive tasks. Group administrative communication (emails, Slack threads) into two predetermined 30-minute batches per day to guard flow state.",
        "days_ago": 21,
        "hours_ago": 8,
    },
    {
        "title": "Sprint Retrospective Framework: What Went Well & Action Items",
        "body": "Use the 4Ls retrospective format: Liked, Learned, Lacked, Longed For. Ensure every identified improvement is paired with a single accountable owner and measurable completion criteria for the upcoming sprint.",
        "days_ago": 22,
        "hours_ago": 1,
    },
    {
        "title": "Weekly Review Checklist for Peak Productivity",
        "body": "1. Clear physical and digital inboxes to zero. 2. Review calendar two weeks back and three weeks ahead. 3. Update project outcome milestones. 4. Choose top 3 high-impact objectives for the coming week.",
        "days_ago": 23,
        "hours_ago": 7,
    },
    {
        "title": "Product Discovery Interviews: The Mom Test Framework",
        "body": "Never ask users if they think an idea is good. Ask about concrete past behaviors: how they currently solve the problem, what tools they pay for, and the specific frustrations they encountered in the last month.",
        "days_ago": 24,
        "hours_ago": 3,
    },
    {
        "title": "Pomodoro Technique Variations: 50-10 vs 25-5 Cycles",
        "body": "For coding and complex problem solving, 25-minute intervals can prematurely interrupt concentration. A 50-minute work session followed by a 10-minute break matches natural ultradian cognitive rhythms better.",
        "days_ago": 25,
        "hours_ago": 11,
    },
    {
        "title": "Effective One-on-One Meeting Agenda for Engineering Leads",
        "body": "Focus 1-on-1s on employee growth and blockers rather than status reports. Discussion prompts: What part of your job feels most energizing? Where are you experiencing organizational friction? How can I support your career targets?",
        "days_ago": 26,
        "hours_ago": 5,
    },
    {
        "title": "Time Blocking Method: Google Calendar vs Analog Planners",
        "body": "Treat your calendar as a physical inventory of finite hours. Budget buffer blocks between meetings to digest notes and capture immediate action items before jumping into subsequent discussions.",
        "days_ago": 27,
        "hours_ago": 9,
    },
    {
        "title": "Async Communication Playbook for Remote Engineering Teams",
        "body": "Default to writing detailed RFCs and pull request descriptions before initiating sync calls. Provide complete context, code snippets, alternatives considered, and explicit feedback deadlines.",
        "days_ago": 28,
        "hours_ago": 6,
    },
    {
        "title": "Decision Log: Architectural Decision Records (ADR) Template",
        "body": "Document architectural decisions in lightweight Markdown ADRs. Include Title, Status (Proposed/Accepted/Deprecated), Context, Decision, and Consequences. Keeps engineering rationale transparent for future onboarders.",
        "days_ago": 29,
        "hours_ago": 2,
    },

    # 31-40: Books, Philosophy, Mindset & Learning
    {
        "title": "Book Summary: Designing Data-Intensive Applications by Martin Kleppmann",
        "body": "A masterclass on reliability, scalability, and maintainability. Covers storage engines (LSM-trees vs B-trees), encoding formats, replication lag, partitioning strategies, and consensus algorithms like Raft and Paxos.",
        "days_ago": 30,
        "hours_ago": 10,
    },
    {
        "title": "Book Summary: Atomic Habits by James Clear - Notes & Quotes",
        "body": "You do not rise to the level of your goals, you fall to the level of your systems. The 4 laws of behavior change: make it obvious, make it attractive, make it easy, and make it satisfying. Habit stacking drives consistency.",
        "days_ago": 31,
        "hours_ago": 4,
    },
    {
        "title": "Book Summary: Thinking, Fast and Slow by Daniel Kahneman",
        "body": "System 1 operates automatically and quickly with little or no effort (heuristics, bias). System 2 allocates attention to effortful mental operations. Understanding anchoring, availability bias, and loss aversion improves engineering estimation.",
        "days_ago": 32,
        "hours_ago": 7,
    },
    {
        "title": "Book Summary: The Pragmatic Programmer 20th Anniversary Edition",
        "body": "Key principles: DRY (Don't Repeat Yourself), Orthogonality, Tracer Bullets, Good-Enough Software, Broken Windows Theory, and continuous investment in your knowledge portfolio across languages and domains.",
        "days_ago": 33,
        "hours_ago": 3,
    },
    {
        "title": "Mental Models: Inversion, First Principles Thinking, and Second-Order Effects",
        "body": "Inversion: Instead of asking how to succeed, ask what would cause catastrophic failure and avoid it. First principles: Boil down problems to fundamental truths and reason up. Second-order effects: Ask 'And then what?'",
        "days_ago": 34,
        "hours_ago": 12,
    },
    {
        "title": "Stoicism & Seneca's Letters: On the Shortness of Life",
        "body": "It is not that we have a short time to live, but that we waste a lot of it. Life is long if you know how to use it. Guard your attention with the same fierceness you guard your property.",
        "days_ago": 35,
        "hours_ago": 5,
    },
    {
        "title": "Sapiens by Yuval Noah Harari: The Power of Shared Fictions",
        "body": "Humans dominate the globe because we are the only animal capable of cooperating flexibly in large numbers via collective imagination—nations, money, corporations, and human rights are shared mythologies.",
        "days_ago": 36,
        "hours_ago": 9,
    },
    {
        "title": "Learning How to Learn: Focused vs Diffuse Thinking Modes",
        "body": "The brain toggles between focused mode (tightly concentrated neural pathways) and diffuse mode (relaxed daydreaming connections). Real problem solving happens when resting after intense focused bouts.",
        "days_ago": 37,
        "hours_ago": 1,
    },
    {
        "title": "Clean Code & Refactoring Patterns by Robert C. Martin",
        "body": "Functions should do one thing and do it well. Keep argument lists short. Name variables with clear intent over brevity. Refactor continuously as you explore domain complexity.",
        "days_ago": 38,
        "hours_ago": 8,
    },
    {
        "title": "The Innovator's Dilemma: Clayton Christensen Notes",
        "body": "Successful incumbents fail not because of bad management, but because they listen to existing customers and pursue sustaining innovations while nimble startups capture low-end disruptive wedges.",
        "days_ago": 39,
        "hours_ago": 6,
    },

    # 41-50: Lifestyle, Health, Cooking & Travel
    {
        "title": "Kyoto & Tokyo 10-Day Travel Itinerary and Hidden Ramen Spots",
        "body": "Day 1-4 Tokyo: Shinjuku Omoide Yokocho, Akihabara electronics, TeamLab Borderless, and Fuunji Tsukemen. Day 5-8 Kyoto: Fushimi Inari morning climb, Arashiyama bamboo grove, Gion tea houses, and Nishiki Market snacks.",
        "days_ago": 40,
        "hours_ago": 2,
    },
    {
        "title": "Artisan Sourdough Bread Formula: 75% Hydration & Cold Fermentation",
        "body": "Formula: 400g bread flour, 50g whole wheat, 340g water (75%), 90g active levain (20%), 9g sea salt (2%). Autolyse 45 mins. 4 stretch-and-folds over 2 hours. Shape into banneton and cold retard in fridge for 16 hours before baking in Dutch oven.",
        "days_ago": 41,
        "hours_ago": 7,
    },
    {
        "title": "Swiss Alps Hiking Trail Guide: Lauterbrunnen and Grindelwald",
        "body": "Stunning alpine trails: Northface Trail from Murren, Panorama trail from Mannlichen to Kleine Scheidegg with Eiger views, and Bachalpsee alpine lake hike. Pack waterproof layers and sturdy trail runners.",
        "days_ago": 42,
        "hours_ago": 3,
    },
    {
        "title": "Cold Brew Coffee Brewing Protocol: Ratio, Grind Size & Steep Time",
        "body": "Coarse grind (kosher salt consistency) to prevent over-extraction bitterness. 1:8 brew ratio for concentrate (100g coffee to 800ml cold filtered water). Steep at room temp for 14 hours or in fridge for 20 hours. Dilute 1:1 with water or milk.",
        "days_ago": 43,
        "hours_ago": 10,
    },
    {
        "title": "5K Running Training Plan for Beginners: 8-Week Progression",
        "body": "Weeks 1-2: 60s jog / 90s walk intervals for 20 mins. Weeks 3-4: 3 mins jog / 2 mins walk. Weeks 5-6: Continuous 15-20 min runs. Week 7: 25 min steady run. Week 8: Full 5K race pace simulation. Prioritize dynamic stretching.",
        "days_ago": 44,
        "hours_ago": 5,
    },
    {
        "title": "Sleep Hygiene Protocols: Light, Temperature and Circadian Optimization",
        "body": "View morning sunlight within 30 minutes of waking to anchor cortisol. Keep bedroom temperature at 66-68°F (19°C). Cut caffeine intake 9 hours before bed, and dim overhead lights 2 hours prior to sleep.",
        "days_ago": 45,
        "hours_ago": 9,
    },
    {
        "title": "Authentic Italian Creamy Tuscan Garlic Chicken Recipe",
        "body": "Sear seasoned chicken cutlets in olive oil. In the same pan, saute minced garlic, sun-dried tomatoes, and baby spinach. Deglaze with chicken broth, stir in heavy cream and freshly grated Parmigiano-Reggiano until velvety.",
        "days_ago": 46,
        "hours_ago": 4,
    },
    {
        "title": "Personal Finance & Investment Strategy: The Three-Fund Portfolio",
        "body": "Simplicity wins long term. Allocate across: 1. Total US Stock Market Index (VTI), 2. Total International Stock Index (VXUS), 3. Total Bond Market Index (BND). Rebalance annually and automate monthly DCA contributions.",
        "days_ago": 47,
        "hours_ago": 8,
    },
    {
        "title": "Strength Training Routine: Compound Lifts & Progressive Overload",
        "body": "Focus on the big 4 compound movements: Squat, Bench Press, Deadlift, and Overhead Press. Track weights and reps weekly. Aim for 3-5 sets of 5-8 reps, increasing load by 2.5kg whenever top set reps are achieved with clean form.",
        "days_ago": 48,
        "hours_ago": 6,
    },
    {
        "title": "Minimalist Packing Checklist for Digital Nomads and Solo Travel",
        "body": "One 35L carry-on backpack: 1. Laptop + 65W GaN multi-port charger + universal plug. 2. 4 merino wool tees, 1 tech pants, 1 shorts. 3. Noise-canceling headphones. 4. Minimal toiletry kit in TSA pouch. 5. Passport, backup credit card, and eSIM profile.",
        "days_ago": 49,
        "hours_ago": 11,
    },
    # 51-52: Bonus specific test notes for search ranking verification
    {
        "title": "FastAPI React Fullstack Integration Notes",
        "body": "Details connecting FastAPI backend on port 8000 with React Vite frontend on port 5173. Testing search ranking when both FastAPI and React appear in the title vs appearing in the body.",
        "days_ago": 0,
        "hours_ago": 1,
    },
    {
        "title": "MongoDB Search Algorithms and Text Ranking Heuristics",
        "body": "Comparing MongoDB regex multi-word search versus Atlas Search Lucene analyzers. Evaluates title keyword matching weights and recency sorting tiebreakers.",
        "days_ago": 0,
        "hours_ago": 3,
    },
]


def seed_database():
    client = MongoClient(MONGO_URL, tz_aware=True)
    db = client["notes_app"]
    notes_col = db["notes"]

    existing_count = notes_col.count_documents({})
    print(f"Connected to MongoDB at {MONGO_URL}. Current notes count in notes_app: {existing_count}")

    now = datetime.now(timezone.utc)
    docs_to_insert = []

    for item in SEED_NOTES:
        created = now - timedelta(days=item.get("days_ago", 0), hours=item.get("hours_ago", 0), minutes=15)
        updated = now - timedelta(days=item.get("days_ago", 0), hours=item.get("hours_ago", 0))
        docs_to_insert.append({
            "title": item["title"],
            "body": item["body"],
            "created_at": created,
            "updated_at": updated,
        })

    # Clear existing if user wants clean seeding or append
    # Let's drop and re-seed to give exactly fresh 52 rich notes
    notes_col.delete_many({})
    result = notes_col.insert_many(docs_to_insert)
    print(f"Successfully seeded {len(result.inserted_ids)} notes into database 'notes_app'!")

    # Also seed into searchable_notes_db if present for safety
    try:
        db_alt = client["searchable_notes_db"]
        db_alt["notes"].delete_many({})
        db_alt["notes"].insert_many(docs_to_insert)
        print("Also synced 52 notes into searchable_notes_db.")
    except Exception as e:
        print("Note: optional sync to searchable_notes_db skipped:", e)

    total = notes_col.count_documents({})
    print(f"Total notes in notes_app.notes collection: {total}")
    return total


if __name__ == "__main__":
    seed_database()
