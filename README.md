# 🧠 ML Paper Interpreter

A full-stack AI web app for querying academic machine learning papers using Retrieval-Augmented Generation (RAG), built with:

- 🔍 **Frontend**: React + Tailwind CSS + Vite
- ⚙️ **Backend**: FastAPI + LangChain + Google Gemini + Hugging Face
- 🗃️ **Vector Store**: Weaviate (or FAISS optional)
- ☁️ **Deployment**: Docker + Kubernetes

---

## ✨ Features

- Ask natural language questions about ML interpretability
- Answers are generated via Gemini + LangChain using retrieved academic papers
- Sources are cited with links, titles, and authors
- Responsive, dark-mode friendly UI
- Shift+Enter for newline, Enter to submit

---

## 🚀 Quickstart (Development)

### 1. Clone the repo

```bash
git clone https://github.com/your-username/ml-interpret-rag.git
cd ml-interpret-rag
```

### 2. Set up Secrets
Create a `k8s/secret.yaml` with environment variables:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: rag-env
type: Opaque
stringData:
  GOOGLE_API_KEY: "your-gemini-api-key"
  HUGGINGFACE_EMBEDDING_MODEL: "sentence-transformers/all-MiniLM-L6-v2"
  CHUNK_SIZE: "500"
  CHUNK_OVERLAP: "50"
  ARXIV_MAX_RESULTS: "20"
  ARXIV_QUERY: "interpretability AND transformer"
```

### 3. Run development
Calling `make` in main directory will start everything including kubernetes cluster using Docker Desktop.

### 4. Visit Local Website and Use
Go to [localhost:80](http://localhost:80)