from fastapi import FastAPI, HTTPException
import redis
from redis.retry import Retry
from redis.backoff import ExponentialBackoff
from redis.exceptions import TimeoutError, ConnectionError, RedisError
import uuid
from os import getenv as env

app = FastAPI()

REDIS_HOST = env("REDIS_HOST", "redis")
REDIS_PORT = int(env("REDIS_PORT", 6379))
QUEUE_NAME = env("QUEUE_NAME", "job")

retry = Retry(
    backoff=ExponentialBackoff(),
    retries=8,
    supported_errors=(TimeoutError, ConnectionError)
)

def get_redis():
    try:
        client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            retry=retry,
            decode_responses=True
        )
        client.ping()
        return client
    except RedisError:
        raise HTTPException(status_code=503, detail="Redis unavailable")


@app.post("/jobs")
def create_job():
    r = get_redis()
    job_id = str(uuid.uuid4())

    r.lpush(QUEUE_NAME, job_id)
    r.hset(f"job:{job_id}", "status", "queued")

    return {"job_id": job_id}


@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    r = get_redis()
    status = r.hget(f"job:{job_id}", "status")

    if not status:
        raise HTTPException(status_code=404, detail="not found")

    return {"job_id": job_id, "status": status}


@app.get("/api/health")
def health():
    return {"status": "ok"}
