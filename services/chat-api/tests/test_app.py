from chat_api.app import app
from fastapi.testclient import TestClient


def test_liveness_does_not_require_external_services() -> None:
    with TestClient(app) as client:
        response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
