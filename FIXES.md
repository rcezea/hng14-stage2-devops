# 📄 `FIXES.md`

---

## 🔧 `main.py`

---

**Line 8–9**
**Problem:** Redis connection was hardcoded to `localhost:6379`, which fails in a containerized environment because services communicate via service names, not localhost.

**Fix:** Replaced hardcoded values with environment variables:

```python
REDIS_HOST = env("REDIS_HOST", "redis")
REDIS_PORT = int(env("REDIS_PORT", 6379))
```

**Impact:** Allows API to connect to Redis correctly in Docker Compose.

---

**Line 11–18**
**Problem:** Redis connection was created at import time and would crash the app if Redis was unavailable at startup.

**Fix:** Moved connection logic into a `get_redis()` function with retry and error handling.
**Impact:** Prevents application crash and enables graceful handling of Redis downtime.

---

**Line 22**
**Problem:** Queue name `"job"` was hardcoded, creating risk of inconsistency across services.

**Fix:** Introduced environment variable:

```python
QUEUE_NAME = env("QUEUE_NAME", "job")
```

**Impact:** Ensures consistency between API and worker services.

---

**Line 30–32**
**Problem:** Missing proper error handling for invalid job IDs; returned 200 OK with error message.

**Fix:** Replaced with HTTP exception:

```python
raise HTTPException(status_code=404, detail="not found")
```

**Impact:** Ensures correct HTTP semantics and improves API reliability.

---

**Line 36**
**Problem:** Redis returned byte strings, requiring manual decoding.

**Fix:** Enabled automatic decoding:

```python
decode_responses=True
```

**Impact:** Simplifies response handling and avoids runtime errors.

---

**Line 41**
**Problem:** Missing health check endpoint required for container health monitoring.

**Fix:** Added:

```python
@app.get("/api/health")
def health():
    return {"status": "ok"}
```

**Impact:** Enables Docker HEALTHCHECK and service monitoring.

---

---

## 🔧 `worker.py`

---

**Line 7–8**
**Problem:** Redis connection used hardcoded `localhost`, which breaks in Docker networking.

**Fix:** Replaced with environment variables:

```python
REDIS_HOST = env("REDIS_HOST", "redis")
REDIS_PORT = int(env("REDIS_PORT", 6379))
```

**Impact:** Enables worker to connect to Redis container correctly.

---

**Line 10–18**
**Problem:** Worker attempted Redis connection once and failed permanently if Redis was not ready.

**Fix:** Implemented retry loop:

```python
def get_redis():
    while True:
        try:
            ...
            return client
        except RedisError:
            time.sleep(2)
```

**Impact:** Handles startup race conditions between services.

---

**Line 22**
**Problem:** Queue name `"job"` was hardcoded.

**Fix:** Introduced:

```python
QUEUE_NAME = env("QUEUE_NAME", "job")
```

**Impact:** Prevents mismatch with API queue.

---

**Line 30–34**
**Problem:** Worker used `signal.pause()`, which blocks execution and prevents job processing.

**Fix:** Removed `signal.pause()` and implemented proper signal handlers.
**Impact:** Ensures worker actually processes jobs.

---

**Line 36–40**
**Problem:** Infinite loop lacked graceful shutdown mechanism.

**Fix:** Added signal handling with `SIGINT` and `SIGTERM`:

```python
running = True
```

**Impact:** Enables clean shutdown during container stop or deploy.

---

**Line 45**
**Problem:** Redis returned byte strings requiring manual decoding.

**Fix:** Enabled `decode_responses=True`.
**Impact:** Simplifies job processing logic.

---

---

## 🔧 `app.js`

---

**Line 6**
**Problem:** Used bitwise OR (`|`) instead of logical OR (`||`) when setting API URL.

**Fix:** Replaced with:

```javascript
const API_URL = process.env.API_URL || "http://localhost:8000";
```

**Impact:** Prevents incorrect URL resolution and runtime failure.

---

**Line 6**
**Problem:** Default API URL pointed to `localhost`, which fails in Docker since services communicate via service names.

**Fix:** Updated default to:

```javascript
"http://localhost:8000"
```

**Impact:** Enables frontend to communicate with API container.

---

**Line 4**
**Problem:** Unused import (`url`) increased code clutter.

**Fix:** Removed unused import.
**Impact:** Improves code cleanliness and lint compliance.

---

**Line 24**
**Problem:** Missing health check endpoint for frontend service.

**Fix:** Added:

```javascript
app.get('/api/health', ...)
```

**Impact:** Enables container health monitoring and integration testing.

---

## 🔧 `index.html`

---


**Line 35-37 Problem:**
`pollJob` would continue polling indefinitely even when the backend could no longer return a valid job status (e.g., if the Redis cache was cleared and the key no longer existed). In such cases, the endpoint might return a non-200 HTTP status, but the code ignored that and kept retrying.


**Fix:**
Added a guard to only continue polling when the HTTP response status is `200`, ensuring polling stops if the job no longer exists or the request fails.

```js
if (res.status === 200)
  if (data.status !== 'completed')
    setTimeout(() => pollJob(id), 2000);
```

