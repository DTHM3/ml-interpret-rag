from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from backend.utils.config import HUGGINGFACE_EMBEDDING_MODEL, ARXIV_MAX_RESULTS, ARXIV_QUERY
from backend.utils.loaders import fetch_arxiv_papers, split_documents

from backend.utils.logging_utils import setup_logger

logger = setup_logger(__name__)

def build_retriever(query: str = ARXIV_QUERY, max_results: int = ARXIV_MAX_RESULTS):
    logger.info(f"🔍 Fetching papers from arXiv with query: {query} (max_results={max_results})")
    papers = fetch_arxiv_papers(query, max_results)
    assert papers, "⚠️ No papers loaded from arXiv."

    logger.info(f"📄 Fetched {len(papers)} papers from arXiv. Splitting into chunks...")

    chunks = split_documents(papers)
    assert chunks, "⚠️ No chunks created from the fetched papers."

    logger.info(f"📚 Split into {len(chunks)} chunks. Creating HuggingFace embeddings...")
    embedding = HuggingFaceEmbeddings(model_name=HUGGINGFACE_EMBEDDING_MODEL)
    assert embedding is not None, "⚠️ Failed to create HuggingFace embeddings."
    logger.info("✅ HuggingFace embeddings created successfully. Building FAISS vectorstore...")

    vectorstore = FAISS.from_documents(chunks, embedding)
    assert vectorstore is not None, "⚠️ Failed to create FAISS vectorstore."
    logger.info("✅ Vectorstore created successfully. Building retriever...")
    
    retriever = vectorstore.as_retriever()
    assert retriever is not None, "⚠️ Failed to create retriever."
    logger.info("✅ Retriever built successfully.")

    return retriever