from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from backend.utils.config import HUGGINGFACE_EMBEDDING_MODEL
from backend.utils.loaders import fetch_arxiv_papers, split_documents

def build_retriever(query: str = "interpretability AND transformer", max_results: int = 10):
    papers = fetch_arxiv_papers(query, max_results)
    assert papers, "⚠️ No papers loaded from arXiv."

    chunks = split_documents(papers)
    assert chunks, "⚠️ No chunks created from the fetched papers."

    embedding = HuggingFaceEmbeddings(model_name=HUGGINGFACE_EMBEDDING_MODEL)
    vectorstore = FAISS.from_documents(chunks, embedding)
    
    retriever = vectorstore.as_retriever()
    assert retriever is not None, "⚠️ Failed to create retriever."

    return retriever