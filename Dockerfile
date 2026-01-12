# Use official Python runtime as base image
FROM python:3.14-slim

# Set working directory in container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY train.py serve.py ./
COPY src/ ./src/
COPY data/ ./data/

# Create mlruns directory for MLFlow
RUN mkdir -p mlruns

# Expose ports
# 8000 for FastAPI server
# 5000 for MLFlow UI
EXPOSE 8000 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV MLFLOW_TRACKING_URI=file:./mlruns

# Default command runs FastAPI server
CMD ["python", "serve.py"]
