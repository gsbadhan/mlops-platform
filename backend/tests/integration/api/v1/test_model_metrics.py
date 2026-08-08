import pytest

from app.model.model_metrics import ModelMetrics
from app.enums.stages import Algorithm, Framework
from app.repository.model_metrics_repository import ModelMetricsRepository


def create_model(client):
    response = client.post(
        "/api/v1/models",
        json={
            "name": "fraud-detection",
            "description": "Fraud detection model",
            "owner": "mlops-team",
            "framework": Framework.SCIKIT_LEARN,
            "algorithm": Algorithm.RANDOM_FOREST,
        },
    )
    assert response.status_code == 201
    return response.json()["id"]


def create_model_version(client, model_id):
    response = client.post(
        f"/api/v1/models/{model_id}/versions",
        json={
            "version": "1.0.0",
            "artifact_uri": "s3://models/fraud-detection/1.0.0",
            "training_data_uri": "s3://datasets/fraud/2026",
            "tags": ["mlops"],
        },
    )
    assert response.status_code == 201
    return response.json()["id"]


@pytest.mark.integration
def test_get_model_metrics_success(client, db):
    model_id = create_model(client)
    model_version_id = create_model_version(client, model_id)
    repository = ModelMetricsRepository()
    metrics = ModelMetrics(
        model_version_id=model_version_id,
        accuracy=0.95,
        precision=0.93,
        recall=0.91,
        f1_score=0.92,
    )
    created_metrics = repository.create(db, metrics)
    assert created_metrics is not None

    response = client.get(f"/api/v1/models/{model_id}/metrics")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) == 1
    assert body[0]["version"] == "1.0.0"
    assert body[0]["accuracy"] == 0.95
    assert body[0]["precision"] == 0.93
    assert body[0]["recall"] == 0.91
    assert body[0]["f1_score"] == 0.92


@pytest.mark.integration
def test_get_model_metrics_empty(client):
    model_id = create_model(client)
    response = client.get(f"/api/v1/models/{model_id}/metrics")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert body == []
