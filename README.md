

# 📦 Stage 2: Containerized Microservices Application

This project is a production-ready containerized system consisting of:

* **Frontend (Node.js)** – user interface for submitting and tracking jobs
* **API (FastAPI)** – handles job creation and status retrieval
* **Worker (Python)** – processes jobs asynchronously
* **Redis** – message broker between API and worker

All services are containerized and orchestrated using Docker.

---

# 🚀 Prerequisites

Ensure the following are installed on your machine:

* **Docker** (v20+)
* **Docker Compose** (v2+)
* **Git**

Verify:

```bash
docker --version
docker compose version
git --version
```

---

# 📥 Setup Instructions

## 1. Clone the repository

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

---

## 2. Create environment variables

Copy the example file:

```bash
cp .env.example .env
```

Edit `.env` if needed.

---

## 3. Build and start the system

```bash
docker compose up -d
```

---

## 4. Verify services are running

```bash
docker compose ps
```

Expected output (all services running):

```text
redis       → healthy
api         → healthy
worker      → healthy
frontend    → running
```

---

# 🌐 Access the Application

Open your browser:

```text
http://localhost:3000
```

---

# 🔄 How the System Works

1. User submits a job via the frontend
2. Frontend sends request to API
3. API stores job in Redis queue
4. Worker picks job from Redis and processes it
5. Worker updates job status
6. Frontend polls API until job is completed

---

# 🧪 Test the Flow Manually

Submit a job:

```bash
curl -X POST http://localhost:3000/submit
```

Check status:

```bash
curl http://localhost:3000/status/<job_id>
```

---

# 🛑 Stop the System

```bash
docker compose down
```

---

# 🧹 Clean Up (Optional)

Remove volumes and unused resources:

```bash
docker system prune -f
```

---

# ✅ What a Successful Startup Looks Like

* All containers are running (`docker compose ps`)
* No restart loops or crashes
* Frontend loads in browser
* Job submission returns a valid `job_id`
* Job progresses from `queued → processing → completed`

---

# 📌 Notes

* All services communicate over an internal Docker network
* Redis is not exposed publicly
* Images are built and tagged using Git SHA for consistency
* Health checks ensure service readiness before dependency startup

