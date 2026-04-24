# Stage 1: builder
FROM python:3.11-slim AS builder

WORKDIR /opt/worker

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


# Stage 2: runtime
FROM python:3.11-slim

WORKDIR /opt/worker

# Copy installed deps
COPY --from=builder /usr/local /usr/local

# Copy app
COPY worker.py .

RUN useradd -m appuser
USER appuser

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import redis, os; r=redis.Redis(host=os.getenv('REDIS_HOST','redis'), port=6379); exit(0 if r.ping() else 1)"

CMD ["python", "worker.py"]