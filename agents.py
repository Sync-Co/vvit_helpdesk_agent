"""
VVIT Helpdesk — LangGraph Multi-Agent System (v2.0)
Architecture: Supervisor Pattern (1 Supervisor + 5 Specialist Agents)
"""

import os
from typing import TypedDict, Literal
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END

load_dotenv()

BASE_DIR   = os.path.dirname(__file__)
INDEX_DIR  = os.path.join(BASE_DIR, "data")
LLM_MODEL        = "gpt-4o"
EMBEDDING_MODEL  = "text-embedding-3-small"
RETRIEVAL_TOP_K  = 15

class AgentState(TypedDict):
    query: str
    chat_history: list[dict]
    routed_to: str
    retrieved_docs: list[dict]
    answer: str

def load_indexes() -> dict:
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    indexes = {}

    categories = [
        "about_administration",
        "admissions",
        "placements_careers",
        "campus_facilities",
        "student_life",
    ]

    for cat in categories:
        path = os.path.join(INDEX_DIR, f"faiss_{cat}")
        if os.path.exists(path):
            indexes[cat] = FAISS.load_local(
                path, embeddings, allow_dangerous_deserialization=True
            )
            print(f"✓ Loaded FAISS index: {cat}")
        else:
            print(f"⚠ Index not found: {path} — run build_index.py first")

    return indexes

def retrieve(query: str, vectorstore: FAISS, top_k: int = RETRIEVAL_TOP_K) -> list[dict]:
    results = vectorstore.similarity_search(query, k=top_k)
    return [
        {
            "content": doc.page_content,
            "source":  doc.metadata.get("source", ""),
            "title":   doc.metadata.get("title", ""),
        }
        for doc in results
    ]

def format_context(docs: list[dict]) -> str:
    parts = []
    for i, doc in enumerate(docs, 1):
        parts.append(
            f"[Source {i}: {doc['title']} — {doc['source']}]\n{doc['content']}"
        )
    return "\n\n---\n\n".join(parts)

def format_sources(docs: list[dict]) -> str:
    seen = set()
    sources = []
    for doc in docs:
        url = doc["source"]
        if url and url not in seen:
            seen.add(url)
            sources.append(f"• {doc['title']}: {url}")
    return "\n".join(sources) if sources else ""

def build_graph(indexes: dict) -> any:
    llm = ChatOpenAI(model=LLM_MODEL, temperature=0.2)

    def supervisor_node(state: AgentState) -> AgentState:
        query = state["query"]
        history = state.get("chat_history", [])
        
        system_prompt = """You are the routing supervisor for the VVIT University Student Helpdesk.

Your ONLY job is to read the student's question and decide which specialist agent should handle it.

The five specialist agents are:
1. about_administration → University history, vision, mission, leadership (Chancellor, VC, Pro-Chancellor, Secretary, Registrar), governance, NAAC/NBA accreditation, disclosures
2. admissions           → How to apply, eligibility, UG/PG/PhD programs (B.Tech, M.Tech, MBA, MCA), fees, scholarships, entrance exams, curriculum
3. placements_careers   → Placement statistics, companies visited, salary packages, career guidance, internships
4. campus_facilities    → Hostel, library, transport, canteen, sports facilities, ATM, health centre
5. student_life         → Student clubs, NCC, NSS, IIC, IUCEE, IDEA Labs, UIF, student councils, grievance (SGRC/FSGRC), contact details

Respond with ONLY one of these exact words:
about_administration
admissions
placements_careers
campus_facilities
student_life"""

        messages = [SystemMessage(content=system_prompt)]
        for turn in history[-2:]:  # Provide recent context for pronouns like "it" or "there"
            messages.append(HumanMessage(content=turn["human"]))
            messages.append(AIMessage(content=turn["ai"]))
        messages.append(HumanMessage(content=query))

        response = llm.invoke(messages)

        route = response.content.strip().lower()
        valid_routes = {
            "about_administration", "admissions", "placements_careers",
            "campus_facilities", "student_life"
        }
        if route not in valid_routes:
            route = "admissions"

        print(f"\n🔀 Supervisor → routed to: [{route}]")
        return {**state, "routed_to": route}

    def make_specialist_node(category: str, persona: str, scope: str):
        def specialist_node(state: AgentState) -> AgentState:
            query   = state["query"]
            history = state.get("chat_history", [])

            vectorstore = indexes.get(category)
            if not vectorstore:
                return {
                    **state,
                    "retrieved_docs": [],
                    "answer": "I'm sorry, I don't have information on that topic right now. Please contact the VVIT helpdesk directly at the university.",
                }

            docs    = retrieve(query, vectorstore)
            context = format_context(docs)
            sources = format_sources(docs)

            system_prompt = f"""You are the {persona} for VVIT University (vvitu.ac.in).

Your scope: {scope}

Rules:
- Answer ONLY using the provided context below — do not invent information.
- If the context doesn't contain enough information, acknowledge it and direct the student to the appropriate VVIT office or vvitu.ac.in.
- Be warm, professional, and concise. Use bullets for multi-item answers.
- Always end with source URLs.

Context from VVIT website:
{context}"""

            messages = [SystemMessage(content=system_prompt)]
            for turn in history[-4:]:
                messages.append(HumanMessage(content=turn["human"]))
                messages.append(AIMessage(content=turn["ai"]))
            messages.append(HumanMessage(content=query))

            response = llm.invoke(messages)

            answer = response.content.strip()
            if sources:
                answer += f"\n\n📎 **Sources:**\n{sources}"

            print(f"✅ [{category}] agent answered ({len(answer)} chars)")
            return {**state, "retrieved_docs": docs, "answer": answer}

        specialist_node.__name__ = f"{category}_node"
        return specialist_node

    def route_to_specialist(state: AgentState) -> str:
        route_map = {
            "about_administration": "about_administration_node",
            "admissions":           "admissions_node",
            "placements_careers":   "placements_careers_node",
            "campus_facilities":    "campus_facilities_node",
            "student_life":         "student_life_node",
        }
        return route_map.get(state["routed_to"], "admissions_node")

    graph = StateGraph(AgentState)

    graph.add_node("supervisor", supervisor_node)

    graph.add_node("about_administration_node", make_specialist_node(
        category="about_administration",
        persona="University Information Officer",
        scope="VVIT's history, vision, leadership profiles, Board of Management, Governing Body, NAAC/NBA accreditation, mandatory disclosures"
    ))

    graph.add_node("admissions_node", make_specialist_node(
        category="admissions",
        persona="Admissions & Academic Programs Advisor",
        scope="All UG/PG/PhD programs, eligibility criteria, admission process, VVITAT, fee structure, scholarships, program curriculum details"
    ))

    graph.add_node("placements_careers_node", make_specialist_node(
        category="placements_careers",
        persona="Placements & Career Development Advisor",
        scope="Placement statistics, top recruiters, salary data, career guidance cell services, internship opportunities, training programs"
    ))

    graph.add_node("campus_facilities_node", make_specialist_node(
        category="campus_facilities",
        persona="Campus Facilities Advisor",
        scope="Hostel facilities, central library, transport routes and timings, cafeteria/canteen services, sports facilities, laboratories, health centre"
    ))

    graph.add_node("student_life_node", make_specialist_node(
        category="student_life",
        persona="Student Life & Activities Advisor",
        scope="Student clubs, NCC, NSS, IIC, IUCEE, IDEA Labs, University Innovation Fellowship, Student Activity Council, grievance redressal, professional societies"
    ))

    graph.set_entry_point("supervisor")

    graph.add_conditional_edges(
        "supervisor",
        route_to_specialist,
        {
            "about_administration_node": "about_administration_node",
            "admissions_node":           "admissions_node",
            "placements_careers_node":   "placements_careers_node",
            "campus_facilities_node":    "campus_facilities_node",
            "student_life_node":         "student_life_node",
        },
    )

    graph.add_edge("about_administration_node", END)
    graph.add_edge("admissions_node",           END)
    graph.add_edge("placements_careers_node",   END)
    graph.add_edge("campus_facilities_node",    END)
    graph.add_edge("student_life_node",         END)

    return graph.compile()

def ask(app, query: str, chat_history: list[dict] | None = None) -> tuple[str, str, list[dict]]:
    initial_state: AgentState = {
        "query":         query,
        "chat_history":  chat_history or [],
        "routed_to":     "",
        "retrieved_docs": [],
        "answer":        "",
    }
    final_state = app.invoke(initial_state)
    return (
        final_state["answer"],
        final_state["routed_to"],
        final_state["retrieved_docs"],
    )
