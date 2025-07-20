import arxiv, tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from backend.utils.config import CHUNK_SIZE, CHUNK_OVERLAP

def fetch_arxiv_papers(query: str, max_results: int = 10):
    """
    Fetches arXiv papers based on a query and returns them as a list of documents.
    """
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )
    
    docs = []
    for result in search.results():
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            result.download_pdf(filename=tmp.name)
            tmp.flush()
            loader = PyPDFLoader(tmp.name)
            docs.extend(loader.load())
    return docs

def split_documents(documents):
    """
    Splits documents into smaller chunks for processing.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    return text_splitter.split_documents(documents)