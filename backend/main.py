from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from contextlib import asynccontextmanager
import os

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

# ✅ CORS (not strictly needed now, but harmless here)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ API route — defined before static mount
@app.post("/query")
def query(request_body: Question, request: Request):
    retriever = request.app.state.retriever
    qa_chain = request.app.state.qa_chain

    question_text = request_body.query
    answer = qa_chain.invoke(question_text)
    retrieved_docs = retriever.invoke(question_text)

    unique_sources = {}
    for doc in retrieved_docs:
        key = doc.metadata.get("source", "")
        if key not in unique_sources:
            unique_sources[key] = {
                "title": doc.metadata.get("title", ""),
                "authors": doc.metadata.get("authors", []),
                "source": key,
            }

    return {
        "answer": answer.content,
        "sources": list(unique_sources.values())
    }

# ✅ Serve static frontend at the very end
app.mount("/", StaticFiles(directory="static", html=True), name="static")
