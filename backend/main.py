from fastapi import FastAPI, Request
from pydantic import BaseModel
from contextlib import asynccontextmanager
from backend.utils.vectorstore import build_retriever
from backend.utils.qa_chain import get_qa_chain

class Question(BaseModel):
    query: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔷 Initializing backend...")
    retriever = build_retriever()
    qa_chain = get_qa_chain(retriever)

    app.state.retriever = retriever
    app.state.qa_chain = qa_chain

    yield
    print("🔷 Backend shutting down...")

app = FastAPI(lifespan=lifespan)

@app.post("/query")
def query(request_body: Question, request: Request):
    retriever = request.app.state.retriever
    qa_chain = request.app.state.qa_chain

    question_text = request_body.query

    answer = qa_chain.invoke(question_text)
    sources = retriever.get_relevant_documents(question_text)

    return {
        "answer": answer.content,
        "sources": [doc.metadata.get("source", "") for doc in sources]
    }
