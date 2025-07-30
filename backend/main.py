from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from contextlib import asynccontextmanager
import os

from backend.utils.vectorstore import build_retriever
from backend.utils.qa_chain import get_qa_chain

from backend.utils.logging_utils import setup_logger

logger = setup_logger(__name__)

class Question(BaseModel):
    query: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🔷 Initializing backend...")
    retriever = build_retriever(max_results=20)
    qa_chain = get_qa_chain(retriever)

    app.state.retriever = retriever
    app.state.qa_chain = qa_chain

    yield
    logger.info("🔷 Backend shutting down...")

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
    logger.info(f"🔍 Received query: {question_text}")

    try:
        answer = qa_chain.invoke(question_text)
        logger.info(f"✅ Answer generated (length={len(answer.content)} chars)")

        retrieved_docs = retriever.invoke(question_text)
        logger.info(f"📚 Retrieved {len(retrieved_docs)} documents")

        unique_sources = {}
        for doc in retrieved_docs:
            key = doc.metadata.get("source", "")
            if key not in unique_sources:
                unique_sources[key] = {
                    "title": doc.metadata.get("title", ""),
                    "authors": doc.metadata.get("authors", []),
                    "source": key,
                }

        response = {
            "answer": answer.content,
            "sources": list(unique_sources.values())
        }

        logger.info(f"📦 Returning response with {len(response['sources'])} sources")
        return response

    except Exception as e:
        logger.exception("❌ Error processing query")
        raise

# ✅ Serve static frontend at the very end
app.mount("/", StaticFiles(directory="static", html=True), name="static")
