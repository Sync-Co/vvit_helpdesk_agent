"""
VVIT Student Helpdesk Agent — Streamlit Demo App (v2.0)
"""

import os
from dotenv import load_dotenv
import streamlit as st
from agents import build_graph, load_indexes, ask

load_dotenv()
APP_PASSWORD = os.environ.get("APP_PASSWORD")

st.set_page_config(
    page_title="VVIT Student Helpdesk",
    page_icon="🎓",
    layout="centered",
)

st.markdown("""
<style>
    .vvit-header {
        background: linear-gradient(135deg, #003580 0%, #0055b3 100%);
        padding: 20px 28px;
        border-radius: 12px;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .vvit-header h1 {
        color: #ffffff;
        margin: 0;
        font-size: 1.6rem;
        font-weight: 700;
    }
    .vvit-header p {
        color: #c8d8f0;
        margin: 0;
        font-size: 0.9rem;
    }
    .powered-by {
        text-align: right;
        font-size: 0.72rem;
        color: #888;
        margin-bottom: 16px;
        margin-top: -4px;
    }
    .agent-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 8px;
    }
    .badge-about       { background: #f3e8ff; color: #6b21a8; }
    .badge-admissions  { background: #e8f0fe; color: #1a56db; }
    .badge-placements  { background: #fdf6e8; color: #c27803; }
    .badge-campus      { background: #e8f9f0; color: #057a55; }
    .badge-student     { background: #e0f2fe; color: #0369a1; }
    
    .sq-title {
        font-size: 0.8rem;
        color: #555;
        margin-bottom: 6px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .stChatMessage { border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

def check_password():
    if st.session_state.get("authenticated", False):
        return True

    st.markdown("<h2 style='text-align: center; margin-top: 50px; color: #003580;'>🔒 Restricted Demo Access</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>This is a private AI demonstration. Please enter the access code.</p>", unsafe_allow_html=True)
    
    if not APP_PASSWORD:
        st.error("⚠️ App password not configured. Please set APP_PASSWORD in your .env file or Streamlit secrets.")
        st.stop()
        
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        password = st.text_input("Access Code", type="password", key="pwd_input", label_visibility="collapsed", placeholder="Enter access code here...")
        if st.button("Unlock Agent", use_container_width=True):
            if password == APP_PASSWORD:
                st.session_state["authenticated"] = True
                st.rerun()
            elif password:
                st.error("Incorrect access code.")

    return False

if not check_password():
    st.stop()

st.markdown("""
<div class="vvit-header">
    <div>🎓</div>
    <div>
        <h1>VVIT Student Helpdesk</h1>
        <p>Vasireddy Venkatadri International Technological University — AI-Powered Information Assistant</p>
    </div>
</div>
<div class="powered-by">Powered by SaptaMind Agentic AI &nbsp;|&nbsp; LangGraph + FAISS | 55 pages indexed</div>
""", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [] 

if "app" not in st.session_state:
    with st.spinner("Loading VVIT knowledge base..."):
        indexes = load_indexes()
        st.session_state.app = build_graph(indexes)

SUGGESTED_QUESTIONS = {
    "🏛️ About VVITU": [
        "Who is the Chancellor of VVIT?",
        "What are VVIT's NAAC and NBA accreditations?"
    ],
    "🎓 Admissions & Programs": [
        "What B.Tech programs are offered at VVIT?",
        "What is the fee structure for B.Tech CSE?"
    ],
    "💼 Placements": [
        "What is the highest package at VVIT placements?",
        "Which companies recruited from VVIT in 2025?"
    ],
    "🏠 Campus Facilities": [
        "Tell me about hostel facilities at VVIT",
        "What are the library hours and facilities?"
    ],
    "🎯 Student Life": [
        "What student clubs and activities does VVIT have?",
        "How does the NCC / NSS work at VVIT?"
    ]
}

st.markdown("<h4 style='font-size: 1rem; color: #444; margin-bottom: 10px;'>💡 Suggested Questions</h4>", unsafe_allow_html=True)
tabs = st.tabs(list(SUGGESTED_QUESTIONS.keys()))

for i, (section, questions) in enumerate(SUGGESTED_QUESTIONS.items()):
    with tabs[i]:
        # Using columns to layout the buttons nicely inside each tab
        cols = st.columns(len(questions))
        for col, q in zip(cols, questions):
            # The button text acts as the suggestion card
            if col.button(q, key=q, help=f"Ask about {section}", use_container_width=True):
                st.session_state["prefill_question"] = q

AGENT_LABELS = {
    "about_administration": ("About & Administration Agent", "badge-about"),
    "admissions":           ("Admissions Agent", "badge-admissions"),
    "placements_careers":   ("Placements & Careers Agent", "badge-placements"),
    "campus_facilities":    ("Campus Facilities Agent", "badge-campus"),
    "student_life":         ("Student Life & Organizations Agent", "badge-student"),
}

for turn in st.session_state.chat_history:
    with st.chat_message("user"):
        st.write(turn["human"])
    with st.chat_message("assistant"):
        agent_key   = turn.get("agent", "")
        label, css  = AGENT_LABELS.get(agent_key, ("Helpdesk Agent", "badge-admissions"))
        st.markdown(
            f"<div class='agent-badge {css}'>🤖 {label}</div>",
            unsafe_allow_html=True,
        )
        st.markdown(turn["ai"])

prefill = st.session_state.pop("prefill_question", None)
user_input = st.chat_input(placeholder="Ask anything about VVIT — admissions, placements, campus, leadership...")

query = prefill or user_input

if query:
    with st.chat_message("user"):
        st.write(query)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            history_for_agent = [
                {"human": t["human"], "ai": t["ai"]}
                for t in st.session_state.chat_history
            ]
            answer, routed_to, docs = ask(
                st.session_state.app,
                query,
                chat_history=history_for_agent,
            )

        label, css = AGENT_LABELS.get(routed_to, ("Helpdesk Agent", "badge-admissions"))
        st.markdown(
            f"<div class='agent-badge {css}'>🤖 {label}</div>",
            unsafe_allow_html=True,
        )
        st.markdown(answer)

    st.session_state.chat_history.append({
        "human": query,
        "ai":    answer,
        "agent": routed_to,
    })

with st.sidebar:
    st.markdown("## 🤖 Multi-Agent Architecture")
    st.markdown("""
**Supervisor** routes queries to:
- 🏛️ **About & Administration**
- 🎓 **Admissions**
- 💼 **Placements & Careers**
- 🏠 **Campus Facilities**
- 🎯 **Student Life**
    """)
    st.divider()
    st.markdown("## ⚙️ Tech Stack")
    st.markdown("LangGraph, FAISS (5 indexes), GPT-4o, text-embedding-3-small, LangSmith")
    st.divider()
    st.markdown("## 📊 Knowledge Base")
    st.markdown("""
55 pages scraped from vvitu.ac.in  
Covers: About, Administration, Admissions, Academics, Career Guidance, Campus Life  
🌐 [vvitu.ac.in](https://vvitu.ac.in)
    """)
    st.divider()
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()
    st.markdown("""
---
<div style='text-align:center; font-size:0.75rem; color:#888;'>
Built with SaptaMind Agentic AI Mastery Program<br>
<a href='https://bootcamp.saptamind.com' target='_blank'>bootcamp.saptamind.com</a>
</div>
""", unsafe_allow_html=True)
