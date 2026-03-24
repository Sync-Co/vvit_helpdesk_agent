"""
FAISS Index Builder
===================
Reads scraped VVIT data (5 categories), chunks the text, creates embeddings,
and builds 5 separate FAISS in-memory indexes.
Run this ONCE after scraper.py.
"""

import json
import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

load_dotenv()

BASE_DIR     = os.path.dirname(__file__)
DATA_FILE    = os.path.join(BASE_DIR, "data", "vvit_data.json")
INDEX_DIR    = os.path.join(BASE_DIR, "data")

CATEGORIES = [
    "about_administration",
    "admissions",
    "placements_careers",
    "campus_facilities",
    "student_life",
]

CHUNK_SIZE    = 1000
CHUNK_OVERLAP = 200
EMBEDDING_MODEL = "text-embedding-3-small"

def load_scraped_data() -> list[dict]:
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(f"❌ {DATA_FILE} not found. Run scraper.py first.")
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"📄 Loaded {len(data)} pages from {DATA_FILE}")
    return data

def build_documents(raw_pages: list[dict], category: str) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " "],
    )
    pages = [p for p in raw_pages if p["category"] == category]
    print(f"   Pages in category: {len(pages)}")

    documents = []
    for page in pages:
        chunks = splitter.split_text(page["text"])
        for i, chunk in enumerate(chunks):
            # PROBLEM 1 & 2 FIX: Context Enrichment
            # Injecting the page title directly into the chunk ensures that even if 
            # the raw text misses a keyword (like 'Registrar'), the semantic vector 
            # still heavily binds to it.
            enriched_content = f"Page Title: {page['title']}\nSource: {page['url']}\n\n{chunk}"
            
            doc = Document(
                page_content=enriched_content,
                metadata={
                    "category": category,
                    "title":    page["title"],
                    "source":   page["url"],
                    "chunk_id": i,
                },
            )
            documents.append(doc)
    print(f"   Total chunks created: {len(documents)}")
    return documents

def build_and_save_index(documents: list[Document], category: str, embeddings: OpenAIEmbeddings):
    if not documents:
        print(f"   ⚠ No documents for [{category}] — skipping index creation.")
        return

    print(f"   🔄 Creating embeddings and building FAISS index...")
    vectorstore = FAISS.from_documents(documents, embeddings)

    save_path = os.path.join(INDEX_DIR, f"faiss_{category}")
    vectorstore.save_local(save_path)
    print(f"   💾 Saved index → {save_path}")

def main():
    print("=" * 60)
    print("VVIT Helpdesk Agent — FAISS Index Builder (v2.0)")
    print("=" * 60)

    raw_pages = load_scraped_data()

    print(f"\n🔑 Initialising OpenAI embeddings ({EMBEDDING_MODEL})...")
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    for category in CATEGORIES:
        print(f"\n📂 Building index: [{category}]")
        docs = build_documents(raw_pages, category)
        build_and_save_index(docs, category, embeddings)

    print(f"\n{'='*60}")
    print("✅ All 5 FAISS indexes built successfully!")
    print("Next step → Run:  streamlit run app.py")

if __name__ == "__main__":
    main()
