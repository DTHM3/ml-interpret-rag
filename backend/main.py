from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import asynccontextmanager
from backend.utils.vectorstore import build_retriever
from backend.utils.qa_chain import get_qa_chain

class Question(BaseModel):
    query: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔷 Initializing backend...")
    retriever = build_retriever(max_results=20)
    qa_chain = get_qa_chain(retriever)

    app.state.retriever = retriever
    app.state.qa_chain = qa_chain

    yield
    print("🔷 Backend shutting down...")

app = FastAPI(lifespan=lifespan)

# Add CORS middleware
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/query")
def query(request_body: Question, request: Request):
    retriever = request.app.state.retriever
    qa_chain = request.app.state.qa_chain

    question_text = request_body.query

    answer = qa_chain.invoke(question_text)
    retrieved_docs = retriever.get_relevant_documents(question_text)

    unique_sources = {}
    for doc in retrieved_docs:
        key = doc.metadata.get("source", "")
        if key not in unique_sources:
            unique_sources[key] = {
                "title": doc.metadata.get("title", ""),
                "authors": doc.metadata.get("authors", []),
                "source": key,
            }

    # Build enriched sources
    sources = list(unique_sources.values())

    return {
        "answer": answer.content,
        "sources": sources
    }
