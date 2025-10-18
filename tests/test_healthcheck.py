from fastapi.testclient import TestClient

from app.main import app


def test_root_endpoint_returns_hello():
    with TestClient(app) as client:
        resp = client.get("/")
        data = resp.json()

        assert resp.status_code == 200
        assert data["message"].startswith("Hello")
