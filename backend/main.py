from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.llms import GoogleGenerativeAI
import arxiv
import os
import tempfile

load_dotenv()
# Ensure the environment variable for Google API key is set
if "GOOGLE_API_KEY" not in os.environ:
    raise ValueError("GOOGLE_API_KEY environment variable is not set")

app = FastAPI()
retriever = None

class Question(BaseModel):
    query: str

@app.on_event("startup")
def load_arxiv_papers():
    global retriever
    # Download top ML interpretability papers from arXiv
    search = arxiv.Search(
        query="interpretability AND transformer",
        max_results=3,
        sort_by=arxiv.SortCriterion.Relevance
    )

    documents = []

    for result in search.results():
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(result.download_pdf())
            tmp_file.flush()
            loader = PyPDFLoader(tmp_file.name)
            docs = loader.load()
            documents.extend(docs)

    # Chunk documents
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = splitter.split_documents(documents)

    # Embed and index using HuggingFace
    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(split_docs, embedding)
    retriever = vectorstore.as_retriever()

@app.post("/query")
def answer_question(q: Question):
    if retriever is None:
        return {"error": "Retriever not initialized"}

    qa_chain = RetrievalQA.from_chain_type(
        llm=GoogleGenerativeAI(model="gemini-pro"),
        retriever=retriever,
        return_source_documents=True
    )
    result = qa_chain({"query": q.query})
    return {"answer": result["result"]}