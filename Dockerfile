FROM python:3.12

# Set working dir to backend
WORKDIR /app/backend

# System deps (for PDF parsing etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Copy backend and static site (assumes frontend has already been built!)
COPY ./backend /app/backend
COPY ./frontend/dist /app/backend/static

# Install Python deps
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Set environment and expose port
ENV PYTHONPATH=/app
EXPOSE 8000

# Serve FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
