import uuid
import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException
from redis.exceptions import RedisError

import api.main as main

client = TestClient(main.app)


@pytest.fixture()
def redis_mock(mocker):
    mock_redis_class = mocker.patch("api.main.redis.Redis")
    return mock_redis_class


def test_create_job(redis_mock):
    mock_redis_instance = redis_mock.return_value

    response = client.post("/jobs")

    assert response.status_code == 200
    assert "job_id" in response.json()
    mock_redis_instance.lpush.assert_called_once()
    mock_redis_instance.hset.assert_called_once()


def test_get_job(redis_mock):
    job_id = str(uuid.uuid4())

    mock_redis_instance = redis_mock.return_value
    mock_redis_instance.hget.return_value = "queued"
    #
    response = client.get(f"/jobs/{job_id}")

    assert response.status_code == 200
    assert response.json() == {"job_id": job_id, "status": "queued"}
    mock_redis_instance.hget.assert_called_once_with(f"job:{job_id}", "status")


def test_get_job_not_found(redis_mock):
    job_id = str(uuid.uuid4())

    mock_redis_instance = redis_mock.return_value
    mock_redis_instance.hget.return_value = None

    response = client.get(f"/jobs/{job_id}")

    assert response.status_code == 404
    mock_redis_instance.hget.assert_called_once()


def test_get_redis_failure(mocker):
    mock_redis_class = mocker.patch("api.main.redis.Redis")

    # - fail early
    # mock_redis_class.side_effect = RedisError()

    mock_instance = mock_redis_class.return_value
    mock_instance.ping.side_effect = RedisError("connection failed")

    from api.main import get_redis

    with pytest.raises(HTTPException) as exc:
        get_redis()

    assert exc.value.status_code == 503
    assert exc.value.detail == "Redis unavailable"


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
