import json
from urllib import request
import time

BASE_URL = "http://localhost:3000"

try:
    # Step 1: Create job
    req = request.Request(f"{BASE_URL}/submit", method="POST")
    response = request.urlopen(req)
    assert response.status == 200
    job_id = json.loads(response.read())["job_id"]
    print(f"Job ID: {job_id}")

    # Step 2: Poll with timeout
    MAX_ATTEMPTS = 15
    #
    for i in range(MAX_ATTEMPTS):
        res = request.urlopen(f"{BASE_URL}/status/{job_id}")
        assert res.status == 200

        status = json.loads(res.read())["status"]
        print(f"Attempt {i}: {status}")

        if status == "completed":
            print("Job completed successfully")
            exit(0)
        if i == MAX_ATTEMPTS - 1:
            print("Job failed")
            exit(1)
        time.sleep(2)
except Exception as e:
    print(f"Exception: {e}")
    exit(1)
