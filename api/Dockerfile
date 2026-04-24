# Stage 1: builder
FROM python:3.11-slim AS builder

WORKDIR /opt/api

RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

# hadolint ignore=DL3013
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


# Stage 2: runtime
FROM python:3.11-slim

WORKDIR /opt/api

# Copy installed dependencies
COPY --from=builder /usr/local /usr/local

# Copy application code
COPY . .

RUN useradd -m appuser
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
CMD python -c "import urllib.request; urllib.request.urlopen('http://api:8000/api/health')" || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]