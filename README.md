# 🎓 VVIT Student Helpdesk Agent

A sophisticated **Multi-Agent Retrieval-Augmented Generation (RAG)** application designed for Vasireddy Venkatadri International Technological University (VVITU). This platform securely reads data from the dynamic VVIT website and serves intelligent, context-aware answers to students.

Built as a capstone project for the **SaptaMind Agentic AI Mastery Program**, this project highlights autonomous AI orchestration, semantic isolated search, and headless JavaScript web scraping.

---

## 🌟 Key Features
- **Headless React Scraping:** Bypasses legacy scraping limitations (like `requests` + `BeautifulSoup`) by utilizing **Playwright** to physically render the University's React SPA and extract hydrated content.
- **5 Specialised AI Agents:** Uses LangGraph's Supervisor pattern to cleanly route questions to 5 distinct conversational personas (Admissions, Placements, Campus Life, etc.).
- **Semantic Data Isolation:** Embeds knowledge into 5 separate **FAISS Vector Databases** to guarantee zero hallucination or cross-contamination.
- **Modern Chat Interface:** Provides a lightweight, highly-polished Streamlit UI featuring interactive tabs and real-time execution badges.

---

## ⚙️ Architecture & Tech Stack
- **AI Orchestration:** LangGraph, LangChain
- **Language Model:** OpenAI `gpt-4o`
- **Embedding Model:** `text-embedding-3-small` (OpenAI)
- **Vector Database:** FAISS (Facebook AI Similarity Search)
- **Data Engineering:** Playwright, BeautifulSoup4
- **Frontend App:** Streamlit

*For an in-depth component breakdown and Mermaid diagram, refer to `architecture.md`.*

---

## 🚀 Quickstart Guide

### 1. Prerequisites
Ensure you have Python 3.10+ installed.
Install the application dependencies:
```bash
pip install -r requirements.txt
```

**Critical Step:** Because VVIT's website relies heavily on dynamic JavaScript (React), you *must* install the Playwright Chromium binaries:
```bash
playwright install chromium
```

### 2. Environment Configuration
Copy the sample environment file:
```bash
cp .env.example .env
```
Open `.env` and configure your API keys:
- `OPENAI_API_KEY`: Required for embeddings and the primary LangGraph model.
- `LANGCHAIN_API_KEY`: Highly recommended to enable LangSmith tracing (perfect for demonstrating agent routing in real-time).

### 3. Build the Brain (Pipeline)
*(Note: If you already have the `data/` directory populated, you can skip to Step 4)*

**A. Scrape the University Data (56 Pages)**
```bash
python scraper.py
```
*Expected Output: `vvit_data.json` containing thousands of characters mapped across 5 categories.*

**B. Generate the FAISS Victor Indices**
```bash
python build_index.py
```
*Expected Output: 5 perfectly structured FAISS folders created under `data/`.*

### 4. Launch the AI Agent
Run the Streamlit interactive dashboard:
```bash
streamlit run app.py
```
Open your browser to `http://localhost:8501`.

---

## 🧪 Running Integration Tests
Before pitching to university leadership, you can silently verify that all 5 FAISS indices are mounted properly and the LLM routes correctly using our test suite:
```bash
python test_agent.py
```

---

## 📝 Demo Materials
Looking to present this to the VVIT Chairman or HODs? Open `demo_runsheet.md` for a comprehensive 15-minute pitch script, including pre-planned "wow factor" questions and sales objection handling.
