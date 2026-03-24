# VVIT Student Helpdesk Agent — Advanced Master Prompt
### Version 2.0 — Full Coverage: All 6 Navigation Sections, 55 Pages, 5 FAISS Indexes

> **How to use this prompt:**
> Copy each `## PROMPT` block and paste it into your AI coding assistant (Claude, GPT-4o, Cursor, etc.)
> in sequence. Each prompt builds on the previous step.

---

## ⚠️ Critical Technical Discovery — Read Before Starting

**vvitu.ac.in is a React Single Page Application (SPA).**

Every URL returns the same 3,234-byte empty HTML shell — just `<div id="root"></div>` —
because content is rendered by JavaScript at runtime.

| Method | Result |
|--------|--------|
| `requests` + `BeautifulSoup` | ❌ Empty shell only |
| `Jina AI Reader` | ❌ 403 Forbidden |
| `Playwright` (headless Chromium) | ✅ Full content — tested & confirmed |

**The scraper MUST use Playwright. This is non-negotiable.**

---

## Overview of What Gets Built

A **Live AI Helpdesk Agent** covering ALL 6 navigation sections of VVIT's website.

| What | Detail |
|------|--------|
| Scraper | Playwright (headless) — Interaction-based for stats tabs |
| Vector DBs | 5 separate FAISS indexes with Title/URL metadata injection |
| Retrieval | MMR (Maximal Marginal Relevance) with k=15 |
| Agents | 6 total: 1 Supervisor + 5 Specialists + 1 Out-of-Scope Guardrail |
| UI | Streamlit with collapsible sources and badge-based routing |
| Tracing | LangSmith (shows live agent routing — demo highlight) |

---

## Complete Architecture

```
                        User Query
                             │
                    ┌────────▼────────┐
                    │  SUPERVISOR     │  ← classifies intent
                    │    AGENT        │    routes to specialist
                    └────────┬────────┘
           ┌─────────┬───────┼────────┬──────────┬──────────┐
           ▼         ▼       ▼        ▼           ▼          ▼
      [About &  [Admissions [Place-  [Campus    [Student    [OUT OF
      Admin     & Academic  ments &  Facili-    Life &      SCOPE]
      Agent]    Programs    Careers  ties       Organiz-    (Decline)
                Agent]      Agent]   Agent]     ations
                                                 Agent]
           │         │       │        │           │
           ▼         ▼       ▼        ▼           ▼
    faiss_about  faiss_   faiss_   faiss_      faiss_
    _admin       admis-   place-   campus_     student
                 sions    ments    facili-     _life
                          _careers ties
```

### Agent-to-Navigation-Section Mapping

| Agent | Covers Nav Section(s) | Pages | FAISS Index |
|-------|----------------------|-------|-------------|
| About & Administration | About VVITU + Administration | 11 | `faiss_about_administration` |
| Admissions & Academic Programs | Admissions + Academics | 27 | `faiss_admissions` |
| Placements & Careers | Career Guidance | 2 | `faiss_placements_careers` |
| Campus Facilities | Campus Life → Facilities | 4 | `faiss_campus_facilities` |
| Student Life & Organizations | Campus Life → Activities + Committees + Societies | 11 | `faiss_student_life` |
| **TOTAL** | **All 6 nav sections** | **55** | **5 indexes** |

---

## Confirmed URL Routes (live-tested, March 2026)

### Agent 1 — About & Administration (11 pages)
```
/about-us
/chancellor
/pro_chancellor
/vice-chancellor
/secretary
/jt-secretary
/registrar
/board_of_management
/governing_body
/accreditation-and-approvals
/mandatory-disclosures
```

### Agent 2 — Admissions & Academic Programs (27 pages)
```
/admissions
/admissions/ug-programs
/admissions/ug-programs/btech-cse
/admissions/ug-programs/btech-cse-ai-ml
/admissions/ug-programs/btech-cse-ai-ds
/admissions/ug-programs/btech-cse-iot
/admissions/ug-programs/btech-ece
/admissions/ug-programs/btech-eee
/admissions/ug-programs/btech-mec
/admissions/ug-programs/btech-civil
/admissions/ug-programs/btech-bba
/admissions/pg-programs
/admissions/pg-programs/mtech-cse
/admissions/pg-programs/mtech-cse-ai-ds
/admissions/pg-programs/mtech-cse-ai
/admissions/pg-programs/mtech-eee
/admissions/pg-programs/mtech-ece
/admissions/pg-programs/mtech-mec
/admissions/pg-programs/mtech-civil
/admissions/pg-programs/mtech-mca
/admissions/pg-programs/mtech-mba
/admissions/phd-programs
/admissions/phd-programs/phd-cse-ai
/admissions/phd-programs/phd-ece
/admissions/phd-programs/phd-eee
/admissions/phd-programs/phd-mec
/admissions/phd-programs/phd-civil
```

### Agent 3 — Placements & Careers (2 pages)
```
/placement
/statistics
```

### Agent 4 — Campus Facilities (4 pages)
```
/hostels
/library
/transport
/canteen
```

### Agent 5 — Student Life & Organizations (11 pages)
```
/student-clubs
/student-council
/NCC
/NSS
/IUCEE
/IIC
/IDEA-Labs
/UIF
/SGRC
/FSGRC
/contact-us
```

---

## Project File Structure

```
vvit_helpdesk_agent/
├── requirements.txt
├── .env.example
├── scraper.py          ← Step 1: Playwright scraper → 55 pages
├── build_index.py      ← Step 2: Chunk + embed → 5 FAISS indexes
├── agents.py           ← Step 3: Supervisor + 5 Specialist Agents
└── app.py              ← Step 4: Streamlit UI
    data/
    ├── vvit_data.json
    ├── faiss_about_administration/
    ├── faiss_admissions/
    ├── faiss_placements_careers/
    ├── faiss_campus_facilities/
    └── faiss_student_life/
```

## Full Setup Commands

```bash
pip install -r requirements.txt
playwright install chromium        # downloads ~110MB Chromium (one-time)
cp .env.example .env               # add your OPENAI_API_KEY
python scraper.py                  # scrapes 55 pages → data/vvit_data.json
python build_index.py              # builds 5 FAISS indexes
streamlit run app.py               # launches demo UI
```

---

---

## PROMPT 1 — Project Setup & Dependencies

```
You are a senior AI engineer building a production-grade multi-agent RAG chatbot.

## Project
VVIT Student Helpdesk Agent — a live AI assistant trained on real data scraped
from all 6 navigation sections of Vasireddy Venkatadri Institute of Technology's
website (vvitu.ac.in).

## IMPORTANT: Site is a React SPA
vvitu.ac.in returns a 3,234-byte empty HTML shell on every URL via requests.
The scraper MUST use Playwright (headless Chromium). Do NOT use requests/BS4/lxml.

## Task: Create two files

### 1. requirements.txt
Exact packages with minimum version pins:
- langchain>=0.3.0
- langchain-openai>=0.2.0
- langchain-community>=0.3.0
- langchain-core>=0.3.0
- langgraph>=0.2.0
- faiss-cpu>=1.8.0
- streamlit>=1.39.0
- python-dotenv>=1.0.0
- tiktoken>=0.7.0
- langsmith>=0.1.0
- playwright>=1.44.0

Add comment: "# After pip install, also run: playwright install chromium"

### 2. .env.example
- OPENAI_API_KEY=sk-...          # Required
- LANGCHAIN_TRACING_V2=true      # Optional — enables LangSmith
- LANGCHAIN_API_KEY=ls__...      # Optional — LangSmith key
- LANGCHAIN_PROJECT=vvit-helpdesk-agent

Comment: LangSmith is strongly recommended for the live demo — it displays
each agent's routing decision and retrieval steps in real time on a
separate screen, which is visually impressive to non-technical audiences.
```

---

---

## PROMPT 2 — Web Scraper (scraper.py)

```
You are a senior Python engineer. Build scraper.py for the VVIT Helpdesk Agent.

## Purpose
Crawl all 55 pages of vvitu.ac.in using Playwright and save to data/vvit_data.json.
This script runs ONCE before building the FAISS indexes.

## Why Playwright Is Mandatory
vvitu.ac.in is a React SPA. requests/urllib/BeautifulSoup only retrieve the
3,234-byte empty HTML shell (<div id="root"></div>). All content is rendered
by JavaScript. Playwright launches headless Chromium, waits for React to paint,
then extracts real content. DO NOT use any HTTP library for page fetching.

## Libraries
- playwright.sync_api: sync_playwright, TimeoutError as PlaywrightTimeout
- json, os, time (standard library)

## Browser Configuration
- Launch: p.chromium.launch(headless=True)
- Context with User-Agent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64)
  AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
- page.goto(url, wait_until="domcontentloaded", timeout=20000)
- page.wait_for_timeout(2500)   ← mandatory: wait for React render
- content = page.inner_text("body")
- time.sleep(0.5) between pages

## TARGET_PAGES Dictionary (5 categories, 55 pages total)
Define TARGET_PAGES as a dict with these exact key-value pairs:

"about_administration": [
    "/about-us", "/chancellor", "/pro_chancellor", "/vice-chancellor",
    "/secretary", "/jt-secretary", "/registrar", "/board_of_management",
    "/governing_body", "/accreditation-and-approvals", "/mandatory-disclosures"
]

"admissions": [
    "/admissions", "/admissions/ug-programs",
    "/admissions/ug-programs/btech-cse",
    "/admissions/ug-programs/btech-cse-ai-ml",
    "/admissions/ug-programs/btech-cse-ai-ds",
    "/admissions/ug-programs/btech-cse-iot",
    "/admissions/ug-programs/btech-ece",
    "/admissions/ug-programs/btech-eee",
    "/admissions/ug-programs/btech-mec",
    "/admissions/ug-programs/btech-civil",
    "/admissions/ug-programs/btech-bba",
    "/admissions/pg-programs",
    "/admissions/pg-programs/mtech-cse",
    "/admissions/pg-programs/mtech-cse-ai-ds",
    "/admissions/pg-programs/mtech-cse-ai",
    "/admissions/pg-programs/mtech-eee",
    "/admissions/pg-programs/mtech-ece",
    "/admissions/pg-programs/mtech-mec",
    "/admissions/pg-programs/mtech-civil",
    "/admissions/pg-programs/mtech-mca",
    "/admissions/pg-programs/mtech-mba",
    "/admissions/phd-programs",
    "/admissions/phd-programs/phd-cse-ai",
    "/admissions/phd-programs/phd-ece",
    "/admissions/phd-programs/phd-eee",
    "/admissions/phd-programs/phd-mec",
    "/admissions/phd-programs/phd-civil"
]

"placements_careers": [
    "/placement", "/statistics"
]

"campus_facilities": [
    "/hostels", "/library", "/transport", "/canteen"
]

"student_life": [
    "/student-clubs", "/student-council", "/NCC", "/NSS",
    "/IUCEE", "/IIC", "/IDEA-Labs", "/UIF",
    "/SGRC", "/FSGRC", "/contact-us"
]

## Text Cleaning
Strip these exact nav boilerplate strings (present on every page):
"Light Mode", "Dark Mode", "Student Login", "Staff Login",
"Examinations", "About VVITU", "Administration", "Admissions",
"Academics", "Career Guidance", "Campus Life", "Contact Us",
"Admission 2026 - Apply", "Notifications"

Also strip: empty lines, lines < 20 chars, lines of only punctuation (•·–—-|)

## Output JSON Schema
Each document: { "category": str, "title": str, "url": str, "text": str }
Title fallback: if page.title() is the generic university name, derive
title from URL path (e.g. "/board_of_management" → "Board Of Management").

Save all 55 documents to: data/vvit_data.json

## Robustness
- PlaywrightTimeout → print ✗ warning, skip page, continue
- Any other Exception → print ✗ error, skip page, continue
- Skip if cleaned text < 100 chars

## Expected Output
55 pages total:
  about_administration: 11 | admissions: 27
  placements_careers: 2   | campus_facilities: 4
  student_life: 11

Console format:
  📂 Category: [name]
  → Scraping: [url]
     ✓ Title (N chars)
     ⚠ Too little content
     ✗ Error description
```

---

---

## PROMPT 3 — FAISS Index Builder (build_index.py)

```
You are a senior AI/ML engineer. Build build_index.py for the VVIT Helpdesk Agent.

## Purpose
Load data/vvit_data.json, chunk each page, create OpenAI embeddings, build
5 separate FAISS in-memory indexes (one per agent domain), save to disk.

## Why 5 Separate Indexes
Each specialist agent searches ONLY its own index. This scopes retrieval
precisely to the relevant domain — questions about hostels never pull
placement data — and makes the multi-agent routing visibly meaningful.

## Exact Import Paths (no alternatives)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import json, os

## Chunking
- chunk_size: 500
- chunk_overlap: 80
- separators: ["\n\n", "\n", ".", " "]

## Embedding Model
OpenAIEmbeddings(model="text-embedding-3-small")

## Process — repeat for each of 5 categories
1. Filter: pages where page["category"] == category
2. Split each page["text"] with RecursiveCharacterTextSplitter
3. Wrap in Document with metadata:
   { "category": str, "title": str, "source": str (url), "chunk_id": int }
4. FAISS.from_documents(docs, embeddings)   ← in-memory build
5. vectorstore.save_local(f"data/faiss_{category}")

## 5 Categories
about_administration   → data/faiss_about_administration/
admissions             → data/faiss_admissions/
placements_careers     → data/faiss_placements_careers/
campus_facilities      → data/faiss_campus_facilities/
student_life           → data/faiss_student_life/

## Error Handling
- Missing data/vvit_data.json → raise FileNotFoundError: "Run scraper.py first"
- Category with 0 documents → print ⚠ warning, skip gracefully

## Console Output
📂 Building index: [category]
   Pages: N | Chunks: N
   🔄 Embedding and indexing...
   💾 Saved → data/faiss_[category]/

Final: "✅ 5 FAISS indexes built — 55 pages indexed"
"Next step → streamlit run app.py"
```

---

---

## PROMPT 4 — LangGraph Multi-Agent System (agents.py)

```
You are a senior AI engineer specialising in LangGraph multi-agent systems.
Build agents.py for the VVIT Helpdesk Agent.

## Architecture: Supervisor Pattern
- 1 Supervisor Agent: classifies intent, routes to correct specialist
- 5 Specialist Agents: each owns one FAISS index and answers within its domain
- LangGraph StateGraph wiring them together

## AgentState (TypedDict)
- query: str
- chat_history: list[dict]       # [{"human": ..., "ai": ...}]
- routed_to: str
- retrieved_docs: list[dict]
- answer: str

## load_indexes() Function
Load all 5 FAISS indexes using FAISS.load_local(path, embeddings,
allow_dangerous_deserialization=True).
Return dict:
{
  "about_administration": vectorstore,
  "admissions":           vectorstore,
  "placements_careers":   vectorstore,
  "campus_facilities":    vectorstore,
  "student_life":         vectorstore,
}
Print ✓ or ⚠ for each.

## RAG Helpers

retrieve(query, vectorstore, top_k=5)
  → similarity_search → list of {"content", "source", "title"}

format_context(docs)
  → numbered blocks: [Source N: Title — URL]\ncontent\n---

format_sources(docs)
  → deduplicated bullet list: • Title: URL

## Supervisor Agent
Model: ChatOpenAI(model="gpt-4o", temperature=0.2)

System prompt — route to ONE of these 5 exact strings:

about_administration
  → University history, vision, mission, leadership (Chancellor, VC, Pro-Chancellor,
    Secretary, Registrar), governance (Board, Governing Body), NAAC/NBA accreditation,
    mandatory disclosures, who founded VVIT, when was it established

admissions
  → How to apply, eligibility criteria, UG programs (B.Tech CSE/AI&ML/AI&DS/IoT/ECE/
    EEE/Mech/Civil/BBA), PG programs (M.Tech/MCA/MBA), PhD programs, fee structure,
    scholarships, VVITAT entrance exam, course curriculum, regulations

placements_careers
  → Placement statistics, companies that visited, salary packages, highest CTC,
    average CTC, career guidance cell, internships, training programs

campus_facilities
  → Hostel/accommodation, library, transport/bus routes, cafeteria/canteen,
    sports infrastructure, ATM, health facilities, laboratories

student_life
  → Student clubs, student activity council, NCC, NSS, IIC, IUCEE, IDEA Labs,
    University Innovation Fellowship (UIF), student grievance (SGRC), faculty
    grievance (FSGRC), contact information, professional societies (IEEE, ACM)

Rules:
- Respond with ONLY the exact category string — no spaces, no punctuation
- If query spans multiple domains, choose the PRIMARY domain
- Fallback: "admissions" if unclassifiable

Print: 🔀 Supervisor → routed to: [category]

## Specialist Node Factory: make_specialist_node(category, persona, scope)

Node behaviour:
1. Retrieve top-5 chunks from category's FAISS index
2. Build history string (last 4 turns of chat_history)
3. Call GPT-4o with system prompt:
   "You are the {persona} for VVIT University (vvitu.ac.in).
   Answer ONLY from the context below — do not invent information.
   If context is insufficient, acknowledge it and direct the student
   to the appropriate VVIT office or vvitu.ac.in.
   Be warm, professional, and concise. Use bullets for multi-item answers.
   Always end with source URLs."
4. Append source citations to answer
5. Return updated state with answer + retrieved_docs

## Instantiate 5 Specialists

Specialist 1 — About & Administration:
  category = "about_administration"
  persona  = "University Information Officer"
  scope    = "VVIT's history, vision, leadership profiles (Chancellor, VC,
              Pro-Chancellor, Secretary, Registrar), Board of Management,
              Governing Body, NAAC/NBA accreditation, mandatory disclosures"

Specialist 2 — Admissions & Academic Programs:
  category = "admissions"
  persona  = "Admissions & Academic Programs Advisor"
  scope    = "All UG/PG/PhD programs, eligibility criteria, admission process,
              VVITAT, fee structure, scholarships, program curriculum details,
              B.Tech/M.Tech/BBA/MCA/MBA specialisations"

Specialist 3 — Placements & Careers:
  category = "placements_careers"
  persona  = "Placements & Career Development Advisor"
  scope    = "Placement statistics (₹29 LPA highest, 600+ placed, 90+ companies),
              top recruiters, salary data, career guidance cell services,
              internship opportunities, training programs"

Specialist 4 — Campus Facilities:
  category = "campus_facilities"
  persona  = "Campus Facilities Advisor"
  scope    = "Hostel facilities (separate for boys/girls), central library,
              transport routes and timings, cafeteria/canteen services,
              sports facilities, laboratories, health centre"

Specialist 5 — Student Life & Organizations:
  category = "student_life"
  persona  = "Student Life & Activities Advisor"
  scope    = "Student clubs, NCC, NSS, IIC (Innovation & Incubation),
              IUCEE, IDEA Labs, University Innovation Fellowship,
              Student Activity Council, grievance redressal (SGRC/FSGRC),
              contact details, professional societies (IEEE, ACM)"

## StateGraph Wiring
Entry: "supervisor"
Conditional edges from supervisor:
  about_administration → about_administration_node
  admissions           → admissions_node
  placements_careers   → placements_careers_node
  campus_facilities    → campus_facilities_node
  student_life         → student_life_node
All 5 specialist nodes → END

## Public Interface
ask(app, query, chat_history=None) → tuple[str, str, list[dict]]
Returns: (answer, routed_to, retrieved_docs)
```

---

---

## PROMPT 5 — Streamlit Demo UI (app.py)

```
You are a senior full-stack Python engineer. Build app.py for the VVIT Helpdesk Agent.

## Run Command
streamlit run app.py

## Page Config
Title: "VVIT Student Helpdesk" | Icon: 🎓 | Layout: centered

## CSS (inject via st.markdown)

1. VVIT header banner:
   - Dark blue gradient: #003580 → #0055b3
   - White headline, light blue subtext, rounded corners

2. Five agent routing badges (one colour per agent):
   - about_administration → purple  (#f3e8ff bg, #6b21a8 text)
   - admissions           → blue    (#e8f0fe bg, #1a56db text)
   - placements_careers   → gold    (#fdf6e8 bg, #c27803 text)
   - campus_facilities    → green   (#e8f9f0 bg, #057a55 text)
   - student_life         → teal    (#e0f2fe bg, #0369a1 text)

3. "Powered by SaptaMind Agentic AI" — small, grey, right-aligned

## Header
- 🎓 icon + "VVIT Student Helpdesk"
- Subtitle: "Vasireddy Venkatadri International Technological University —
  AI-Powered Information Assistant"
- Below: "Powered by SaptaMind Agentic AI | LangGraph + FAISS | 55 pages indexed"

## Session State
- chat_history: []
- app: compiled LangGraph (load inside st.spinner)

## Suggested Questions (5 categories, 2 questions each = 10 buttons)

🏛️ About VVITU:
- "Who is the Chancellor of VVIT?"
- "What are VVIT's NAAC and NBA accreditations?"

🎓 Admissions & Programs:
- "What B.Tech programs are offered at VVIT?"
- "What is the fee structure for B.Tech CSE?"

💼 Placements:
- "What is the highest package at VVIT placements?"
- "Which companies recruited from VVIT in 2025?"

🏠 Campus Facilities:
- "Tell me about hostel facilities at VVIT"
- "What are the library hours and facilities?"

🎯 Student Life:
- "What student clubs and activities does VVIT have?"
- "How does the NCC / NSS work at VVIT?"

Button click → st.session_state["prefill_question"]

## Chat Display
For each turn:
- st.chat_message("user")
- st.chat_message("assistant"):
  - Colour-coded agent badge (use the 5-colour scheme above)
  - Markdown answer

## Chat Input
Placeholder: "Ask anything about VVIT — admissions, placements, campus, leadership..."
On submit: spinner → ask() → badge + answer → append to history

## Sidebar
1. 🤖 Multi-Agent Architecture
   Show the routing diagram as text art:
   Supervisor → 5 specialists with emoji labels

2. ⚙️ Tech Stack
   LangGraph, FAISS (5 indexes), GPT-4o, text-embedding-3-small, LangSmith

3. 📊 Knowledge Base
   "55 pages scraped from vvitu.ac.in"
   "Covers: About, Administration, Admissions, Academics,
   Career Guidance, Campus Life"
   Link: vvitu.ac.in

4. 🗑️ Clear Conversation button

5. SaptaMind footer
   "Built with SaptaMind Agentic AI Mastery Program"
   Link: bootcamp.saptamind.com

## Critical UX Rules
- Colour-coded agent badges on EVERY assistant response
  (this is the visual proof of multi-agent routing for the live demo)
- Sidebar routing diagram is always visible
- Suggested questions section stays expanded by default
```

---

---

## PROMPT 6 — Integration Test (test_agent.py)

```
You are a QA engineer. Write test_agent.py for the VVIT Helpdesk Agent.
Run before the live demo to confirm all 5 agents route and answer correctly.

## Routing Tests (10 tests, 2 per agent)

about_administration:
1. "Who is the Vice Chancellor of VVIT?"
2. "Is VVIT accredited by NAAC?"

admissions:
3. "What are the B.Tech CSE eligibility requirements?"
4. "What is the fee for B.Tech AI and Machine Learning?"

placements_careers:
5. "What is the highest package at VVIT?"
6. "Which companies visited VVIT for placements in 2025?"

campus_facilities:
7. "Tell me about hostel facilities at VVIT"
8. "What are the library timings at VVIT?"

student_life:
9. "What student clubs are available at VVIT?"
10. "How does the NCC unit work at VVIT?"

## Multi-Turn Test (3 turns)
Turn 1: "What departments does VVIT offer?"
Turn 2: "Which is best for AI and data science?"
Turn 3: "What are the placement stats for that program?"
Verify: coherent, contextual answers across all 3 turns.

## Edge Cases (3 tests)
- "fees?" → must not crash, must route somewhere
- "What is the weather in Guntur today?" → graceful out-of-scope response
- "asdfjkl" → graceful handling

## Output Format
  ✅ PASS — [Test] (routed: X | chars: N)
  ❌ FAIL — [Test] — reason

Final: X/13 tests passed
If any routing test fails: print the actual vs expected route.
```

---

---

## PROMPT 7 — Demo Run Sheet (demo_runsheet.md)

```
You are a sales engineer. Create demo_runsheet.md for a 20-minute live demo
to VVIT's Chairman, Vice Chancellor, HODs, and senior faculty.
Goal: secure a campus partnership — not a direct student sale.

## Opening Hook (2 min)
Srini says:
"I spent two days building something using your own website's data.
Before I tell you anything about our program — let me show you."

## Demo Question Sequence (15 min)
10 questions in strategic order across all 5 agents.
Design the sequence so it:
1. Opens with something every person in the room knows (builds trust)
2. Shows the 5 different colour badges firing for different agents
3. Includes one question only the placement cell would know (impresses HODs)
4. Ends with a multi-domain question (shows orchestration live)

For each question:
- Exact text to type
- Which agent fires + badge colour
- What Srini says while it loads (2–3 sec wait)
- Expected audience reaction
- What Srini says when answer appears

Use these confirmed real facts in the script:
  • Highest Package (2025–26): ₹29 LPA — Phasorz Technology
  • Average Package: ₹4.5 LPA | Placed: 600+ | Companies: 90+
  • Top Recruiters: Cognizant, Infosys, Deloitte, Amazon, Morgan Stanley, IBM, Salesforce
  • B.Tech: CSE, AI&ML, AI&DS, IoT, ECE, EEE, Mech, Civil, BBA
  • M.Tech: CSE, AI&DS, AI&ML, Power Electronics, VLSI, Machine Design, Structural
  • PhD programs: CSE/AI, ECE, EEE, Mech, Civil
  • Accreditation: NAAC + NBA (CSE, ECE, EEE, Mech, Civil)
  • Location: Nambur (V), Pedakakani (M), Guntur District, AP

## Architecture Reveal (2 min)
Open LangSmith on second screen showing the agent trace.
Script: "5 AI agents just processed that question. Each one searched
its own private knowledge base. Your students build systems like this
by Week 6. Every line of this code."

## The Ask (1 min)
"Can we run one free 90-minute session for your final-year CSE and
AI&ML students? No approval needed. No commitment. Let the results speak."

## Objection Handling
- "We already have AI in our curriculum"
  → "AICTE curriculum teaches theory. We teach what Cognizant and Infosys
     are interviewing for next month."
- "How is this different from Coursera / NPTEL?"
  → "Those teach concepts. We ship production code. Students leave with
     8 GitHub projects and a CAAP certification."
- "Students can't afford ₹50,000"
  → "0% EMI = ₹8,333/month. One AI Engineer salary covers the whole
     course in the first week of work."
- "We need AICTE approval for a formal tie-up"
  → "The free session needs zero approvals. Let's start there."
- "What if students don't get jobs after?"
  → "15-day full refund, no questions. And 700+ alumni with 65% average
     salary hike disagree with the premise."
```

---

---

## Full System — Single Mega Prompt (Advanced)

> Paste this entire block into Claude Opus or GPT-4o to build the complete
> project in one shot.

```
You are a senior AI engineer. Build a complete, production-ready, demo-grade
multi-agent RAG chatbot from scratch. Build all files without asking questions.

## Project
VVIT Student Helpdesk Agent — covers ALL 6 navigation sections of vvitu.ac.in

## Business Context
Live demo for VVIT leadership (Chairman, VC, HODs). The AI must answer questions
using REAL data scraped from their own website. This is the proof-of-concept
demo for SaptaMind's Agentic AI Mastery Program.

## CRITICAL: React SPA — Playwright Required
vvitu.ac.in returns an empty HTML shell via requests. Use Playwright exclusively.
DO NOT use requests, urllib, BeautifulSoup, or lxml for any page fetching.

## Tech Stack (non-negotiable)
- Scraping:   Playwright (headless Chromium)
- Vector DB:  FAISS × 5 (in-memory, saved to disk) — NO ChromaDB or Qdrant
- Splitter:   langchain_text_splitters.RecursiveCharacterTextSplitter
- Embeddings: OpenAI text-embedding-3-small
- LLM:        GPT-4o, temperature=0.2
- Agents:     LangGraph Supervisor Pattern
- UI:         Streamlit
- Tracing:    LangSmith (optional)

## Files to Build
1. requirements.txt   (playwright, no requests/bs4/lxml)
2. .env.example
3. scraper.py         (Playwright, 55 pages, 5 categories)
4. build_index.py     (5 FAISS indexes)
5. agents.py          (1 Supervisor + 5 Specialists)
6. app.py             (Streamlit, 5 badge colours, 10 demo buttons)

## 5 Agents & Their Domains

Agent 1 — About & Administration → faiss_about_administration (11 pages)
  Routes: /about-us, /chancellor, /pro_chancellor, /vice-chancellor,
  /secretary, /jt-secretary, /registrar, /board_of_management,
  /governing_body, /accreditation-and-approvals, /mandatory-disclosures
  Handles: leadership, NAAC/NBA, history, governance

Agent 2 — Admissions & Academic Programs → faiss_admissions (27 pages)
  Routes: all /admissions/* routes (UG/PG/PhD programs)
  Handles: how to apply, eligibility, all programs, fees, VVITAT

Agent 3 — Placements & Careers → faiss_placements_careers (2 pages)
  Routes: /placement, /statistics
  Handles: stats (₹29 LPA, 600+ placed, 90+ companies), recruiters

Agent 4 — Campus Facilities → faiss_campus_facilities (4 pages)
  Routes: /hostels, /library, /transport, /canteen
  Handles: accommodation, library, buses, food

Agent 5 — Student Life & Organizations → faiss_student_life (11 pages)
  Routes: /student-clubs, /student-council, /NCC, /NSS, /IUCEE,
  /IIC, /IDEA-Labs, /UIF, /SGRC, /FSGRC, /contact-us
  Handles: clubs, NCC/NSS, IIC, grievances, contact info

## Supervisor Routing
Classify query into one of 5 exact strings:
about_administration | admissions | placements_careers |
campus_facilities | student_life
Output ONLY the string. Fallback: "admissions"

## Scraper Nav Noise to Strip (present on every page)
"Light Mode", "Dark Mode", "Student Login", "Staff Login",
"Examinations", "About VVITU", "Administration", "Admissions",
"Academics", "Career Guidance", "Campus Life", "Contact Us",
"Admission 2026 - Apply", "Notifications"

## Streamlit Badge Colours (5 agents)
about_administration: purple  (#f3e8ff / #6b21a8)
admissions:           blue    (#e8f0fe / #1a56db)
placements_careers:   gold    (#fdf6e8 / #c27803)
campus_facilities:    green   (#e8f9f0 / #057a55)
student_life:         teal    (#e0f2fe / #0369a1)

## Quality Requirements
- No hardcoded mock data
- Graceful failure on timeout or missing index
- Multi-turn memory (last 4 turns)
- Source citations on every answer
- 10 routing tests pass before done
```

---

## Appendix — Confirmed Live Data (from scrape, March 2026)

### Placements 2025–26 (as of 17 Feb 2026)
- Highest: ₹29 LPA (Phasorz Technology)
- Average: ₹4.5 LPA | Placed: 600+ | Companies: 90+
- Top recruiters: Cognizant (₹4–6.8 LPA), Infosys (₹4–6.3 LPA), Deloitte (₹4.6 LPA),
  Amazon (historical), Morgan Stanley (historical), IBM, Salesforce, NxtWave

### UG Programs
B.Tech: CSE, CSE (AI&ML), CSE (AI&DS), CSE (IoT & Cyber Security), ECE, EEE, Mech, Civil
BBA: BBA (Hons) with AI specialisation

### PG Programs
M.Tech: CSE, AI&DS, AI&ML, Power Electronics & Electrical Drives, VLSI & Embedded Systems,
Machine Design, Structural Engineering
MBA (AI), MCA

### PhD Programs
CSE/AI, ECE, EEE, Mechanical Engineering, Civil Engineering

### Accreditation
NAAC Accredited | NBA: CSE, ECE, EEE, Mechanical, Civil

### Campus
Nambur (V), Pedakakani (M), Guntur District, Andhra Pradesh
ERP: vvit-erp.edunxt.co.in | VVITAT 2026: March 22 & 28

### Leadership
- Chancellor, Pro-Chancellor, Vice-Chancellor, Secretary, Joint Secretary, Registrar
- Board of Management, Governing Body

---

*Prompt engineered by SaptaMind — VVIT Chairman Demo, March 2026*
*v2.0: Expanded from 3 to 5 agents | 32 → 55 pages | React SPA confirmed*
*Agentic AI Mastery Program | bootcamp.saptamind.com*
