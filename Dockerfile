# syntax=docker/dockerfile:1
FROM python:3.11-slim

LABEL org.opencontainers.image.title="konfiva" \
      org.opencontainers.image.description="Network configuration backup and asset management dashboard" \
      org.opencontainers.image.vendor="OneByJorah" \
      org.opencontainers.image.version="1.0.0"

WORKDIR /app

# Install build dependencies for cryptography/paramiko
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libffi-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Persist SQLite database and config store outside the container layer
RUN mkdir -p /app/instance /var/lib/konfiva/configs

EXPOSE 8103

ENV PYTHONUNBUFFERED=1 \
    FLASK_ENV=production \
    FLASK_DEBUG=0 \
    SQLALCHEMY_DATABASE_URI=sqlite:///instance/konfiva.db

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8103/api/v1/health', timeout=5)" || exit 1

CMD ["python", "app.py"]
