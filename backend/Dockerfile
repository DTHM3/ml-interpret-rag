# Python 3.12 base image
FROM python:3.12

# Set the working directory
WORKDIR /app

# Install OS-level dependencies (optional but useful for PDFs)
RUN apt-get update && apt-get install -y \
    build-essential \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code into /app/backend
COPY . /app/backend

# Expose the port
EXPOSE 8000

# Run uvicorn pointing to backend.main
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
