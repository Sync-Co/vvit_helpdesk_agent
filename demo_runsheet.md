# VVIT SaptaMind Demo — Live Run Sheet (v2.0)

**Target Audience:** VVIT Leadership (Chairman, Vice Chancellor, HODs, senior faculty)
**Goal:** Prove the power of Agentic AI using their own university data to secure a campus partnership.

## 1. Opening Hook (2 min)

*Action: Open laptop, connect to projector. Start Streamlit app (`localhost:8501`). The screen shows a "Restricted Demo Access" encrypted login.*

**Script:**
> "I spent two days building something using your own website's data. Everything is restricted and private to this room. Let me unlock it to show you."

*Action: Type your configured access code and hit Enter. The 5-agent UI unveils itself.*

---

## 2. Demo Question Sequence (15 min)

Type these questions LIVE into the chat box.

### Overview Questions (Administration & Admissions)
**Type:** `Who is the Vice Chancellor of VVIT?`
**Expected Agent:** 🤖 About & Administration Agent (Purple Badge)
**Speak:** "Let's start with a simple administrative lookup."
**Reaction:** Nods.

**Type:** `What B.Tech programs are offered at VVIT?`
**Expected Agent:** 🤖 Admissions Agent (Blue Badge)
**Speak:** "Now let's ask about core academic offerings."
**Reaction:** Verifying accuracy of the exact branches.

### Depth Extraction & Temporal Accuracy
**Type:** `What was the highest package at VVIT in 2024-2025?`
**Expected Agent:** 🤖 Placements & Careers Agent (Gold Badge)
**Speak:** "The system isn't just pulling today's dashboard. It understands history. Watch it differentiate between the current 29 LPA and the 2024 records."
**Reaction:** Significant interest in the temporal accuracy.

**Type:** `What student clubs and activities does VVIT have?`
**Expected Agent:** 🤖 Student Life & Organizations Agent (Teal Badge)
**Speak:** "It can even pull from student affairs and clubs like NCC, NSS, and IDEA Labs."

### The Multi-Turn Transition & Guardrails
**Type:** `Does the CSE department have a good placement record?`
**Expected Agent:** 🤖 Placements & Careers Agent (Gold Badge)
**Speak:** "Notice I didn't say VVIT. It understands the context from my previous turns."

**Type:** `Can you write a Python script for a snake game?`
**Expected Agent:** 🛡️ Out of Scope Guardrail (Neutral Badge)
**Speak:** "Finally, notice how it protects your resources. It politely refuses non-university queries, ensuring it stays a professional academic helper."

---

## 3. The Architecture Reveal (2 min)

*Action: Open LangSmith on second screen showing the agent trace.*

**Script:**
> "6 specialized agents just processed that. We've implemented **Maximal Marginal Relevance (MMR)** search to ensure it finds information from every department, not just the front page. Every line of this code is production-grade."

---

## 4. The Ask (1 min)

*Action: Close the laptop screen slightly.*

**Script:**
> "Can we run one free 90-minute session for your final-year CSE and AI&ML students? No approval needed. No commitment. Let the results speak."

---

## 5. Objection Handling Cheat Sheet

**"We already have AI in our curriculum"**
> "AICTE curriculum teaches theory. We teach what Cognizant and Infosys are interviewing for next month."

**"How is this different from Coursera / NPTEL?"**
> "Those teach concepts. We ship production code. Students leave with 8 GitHub projects and a CAAP certification."

**"Students can't afford ₹50,000"**
> "0% EMI = ₹8,333/month. One AI Engineer salary covers the whole course in the first week of work."

**"We need AICTE approval for a formal tie-up"**
> "The free session needs zero approvals. Let's start there."

**"What if students don't get jobs after?"**
> "15-day full refund, no questions. And 700+ alumni with 65% average salary hike disagree with the premise."
