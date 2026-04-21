import redis
import time
import signal
from os import getenv as env
from redis.backoff import ExponentialBackoff
from redis.retry import Retry
from redis.exceptions import TimeoutError, ConnectionError, RedisError

REDIS_HOST = env("REDIS_HOST", "redis")
REDIS_PORT = int(env("REDIS_PORT", 6379))
QUEUE_NAME = env("QUEUE_NAME", "job")

retry = Retry(
    backoff=ExponentialBackoff(),
    retries=8,
    supported_errors=(TimeoutError, ConnectionError)
)

def get_redis():
    while True:
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
            print("Waiting for Redis...")
            time.sleep(2)


r = get_redis()

running = True

def shutdown_handler(signum, frame):
    global running
    print("Shutting down worker...")
    running = False

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)


def process_job(job_id):
    print(f"Processing job {job_id}")
    time.sleep(2)
    r.hset(f"job:{job_id}", "status", "completed")
    print(f"Done: {job_id}")


while running:
    try:
        job = r.brpop(QUEUE_NAME, timeout=5)
        if job:
            _, job_id = job
            process_job(job_id)
    except Exception as e:
        print(f"Error: {e}")

print("Worker stopped")
