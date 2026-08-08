import pytest


@pytest.mark.integration
def test_create_model_version_success(client):
    # Create a model first
    model_response = client.post(
        "/api/v1/models",
        json={
            "name": "fraud-detection",
            "description": "Fraud detection model",
            "owner": "mlops-team",
            "framework": "scikit-learn",
            "algorithm": "Random Forest",
        },
    )

    assert model_response.status_code == 201

    model_id = model_response.json()["id"]
    # Create model version
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

    body = response.json()
    assert body["model_id"] == model_id
    assert body["version"] == "1.0.0"
    assert body["artifact_uri"] == "s3://models/fraud-detection/1.0.0"
    assert body["training_data_uri"] == "s3://datasets/fraud/2026"


@pytest.mark.integration
def test_get_model_versions_success(client):
    # Create model
    model_response = client.post(
        "/api/v1/models",
        json={
            "name": "fraud-detection",
            "description": "Fraud detection model",
            "owner": "mlops-team",
            "framework": "scikit-learn",
            "algorithm": "Random Forest",
        },
    )

    assert model_response.status_code == 201
    model_id = model_response.json()["id"]

    # Create version
    version_response = client.post(
        f"/api/v1/models/{model_id}/versions",
        json={
            "version": "1.0.0",
            "artifact_uri": "s3://models/fraud-detection/1.0.0",
            "training_data_uri": "s3://datasets/fraud/2026",
            "tags": ["mlops"],
        },
    )

    assert version_response.status_code == 201

    # Get versions
    response = client.get(f"/api/v1/models/{model_id}/versions")
    assert response.status_code == 200

    body = response.json()
    assert isinstance(body, list)
    assert len(body) == 1
    assert body[0]["model_id"] == model_id
    assert body[0]["version"] == "1.0.0"


import pytest


@pytest.mark.integration
def test_change_stage_success(client):
    # Create model
    model_response = client.post(
        "/api/v1/models",
        json={
            "name": "fraud-detection",
            "description": "Fraud detection model",
            "owner": "mlops-team",
            "framework": "scikit-learn",
            "algorithm": "Random Forest",
        },
    )

    assert model_response.status_code == 201
    model_id = model_response.json()["id"]
    # Create model version
    version_response = client.post(
        f"/api/v1/models/{model_id}/versions",
        json={
            "version": "1.0.0",
            "artifact_uri": "s3://models/fraud-detection/1.0.0",
            "training_data_uri": "s3://datasets/fraud/2026",
            "tags": ["mlops"],
        },
    )

    assert version_response.status_code == 201
    version_id = version_response.json()["id"]

    # Change stage
    response = client.post(
        f"/api/v1/models/{model_id}/versions/{version_id}/stage",
        json={
            "stage": "VALIDATED",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == version_id
    assert body["model_id"] == model_id
    assert body["stage"] == "VALIDATED"
