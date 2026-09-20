"""API-тесты без сети: TestClient."""

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture()
def client() -> TestClient:
    return TestClient(create_app())


def test_health(client: TestClient) -> None:
    resp = client.get("/api/v1/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_skills(client: TestClient) -> None:
    resp = client.get("/api/v1/skills")
    assert resp.status_code == 200
    assert "python" in resp.json()["skills"]


def test_match(client: TestClient) -> None:
    resp = client.post(
        "/api/v1/match",
        json={"job_description": "Python FastAPI Docker", "resume": "Python FastAPI SQL"},
    )
    assert resp.status_code == 200
    payload = resp.json()
    assert payload["match_score"] == 0.67
    assert payload["verdict"] == "fit"


def test_match_rejects_empty(client: TestClient) -> None:
    resp = client.post("/api/v1/match", json={"job_description": "", "resume": "Python"})
    assert resp.status_code == 422


@pytest.mark.integration()
def test_match_explicit_shape(client: TestClient) -> None:
    """Интеграционный по маркеру: явные требования, без сети."""
    resp = client.post(
        "/api/v1/match",
        json={"job_description": "x", "resume": "I know Go", "required_skills": ["Go", "Rust"]},
    )
    assert resp.status_code == 200
    assert resp.json()["missing"] == ["rust"]
