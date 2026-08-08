from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)


@pytest.mark.integration
def test_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "UP"
