import pytest
from app.enums.stages import (
    ModelRegistryStages,
    DeploymentState,
    DeploymentEvent,
    DeploymentEnvironment,
)


def create_model(client):
    response = client.post(
        "/api/v1/models",
        json={
            "name": "fraud-detection",
            "description": "Fraud detection model",
            "owner": "mlops-team",
            "framework": "scikit-learn",
            "algorithm": "Random Forest",
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


def change_model_version_stage(
    client, model_id: str, model_version_id: str, stage: ModelRegistryStages
):
    response = client.post(
        f"/api/v1/models/{model_id}/versions/{model_version_id}/stage",
        json={
            "stage": stage,
        },
    )
    assert response.status_code == 200
    return response.json()


def create_deployment(client):
    model_id = create_model(client)
    model_version_id = create_model_version(client, model_id)
    change_model_version_stage(
        client, model_id, model_version_id, ModelRegistryStages.VALIDATED
    )
    change_model_version_stage(
        client, model_id, model_version_id, ModelRegistryStages.APPROVED
    )

    response = client.post(
        "/api/v1/deployments",
        json={
            "model_version_id": model_version_id,
            "environment": "DEV",
            "idempotency_key": "test-deployment-001",
        },
    )
    assert response.status_code == 201
    return response.json()


def change_deployment_state(client, deployment_id, state: DeploymentState):
    response = client.post(
        f"/api/v1/deployments/{deployment_id}/state",
        json={
            "state": state,
        },
    )
    assert response.status_code == 200
    return response.json()


@pytest.mark.integration
def test_create_deployment_success(client):
    model_id = create_model(client)
    model_version_id = create_model_version(client, model_id)
    change_model_version_stage(
        client, model_id, model_version_id, ModelRegistryStages.VALIDATED
    )
    change_model_version_stage(
        client, model_id, model_version_id, ModelRegistryStages.APPROVED
    )

    response = client.post(
        "/api/v1/deployments",
        json={
            "model_version_id": model_version_id,
            "environment": "DEV",
            "idempotency_key": "test-deployment-001",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert "deployment_id" in body
    assert body["model_id"] == model_id
    assert body["version"] == "1.0.0"
    assert body["environment"] == DeploymentEnvironment.DEV
    assert body["status"] == DeploymentState.REQUESTED
    assert body["event"] == DeploymentEvent.DEPLOYMENT_REQUESTED
    assert "timestamp" in body


@pytest.mark.integration
def test_get_deployments_success(client):
    deployment = create_deployment(client)
    response = client.get("/api/v1/deployments")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) == 1
    assert body[0]["deployment_id"] == deployment["deployment_id"]
    assert body[0]["model_id"] == deployment["model_id"]
    assert body[0]["version"] == "1.0.0"
    assert body[0]["environment"] == DeploymentEnvironment.DEV


@pytest.mark.integration
def test_get_deployment_success(client):
    deployment = create_deployment(client)
    deployment_id = deployment["deployment_id"]
    response = client.get(f"/api/v1/deployments/{deployment_id}")
    assert response.status_code == 200
    body = response.json()
    assert body["deployment_id"] == deployment_id
    assert body["model_id"] == deployment["model_id"]
    assert body["version"] == "1.0.0"
    assert body["environment"] == DeploymentEnvironment.DEV
    assert body["status"] == DeploymentState.REQUESTED


@pytest.mark.integration
def test_change_deployment_state_success(client):
    deployment = create_deployment(client)
    deployment_id = deployment["deployment_id"]
    response = client.post(
        f"/api/v1/deployments/{deployment_id}/state",
        json={
            "state": DeploymentState.VALIDATING,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["deployment_id"] == deployment_id
    assert body["status"] == DeploymentState.VALIDATING
    assert body["event"] == DeploymentEvent.VALIDATION_REQUESTED


@pytest.mark.integration
def test_retry_deployment_success(client):
    deployment = create_deployment(client)
    deployment_id = deployment["deployment_id"]
    change_deployment_state(client, deployment_id, DeploymentState.VALIDATING)
    change_deployment_state(client, deployment_id, DeploymentState.DEPLOYING)
    change_deployment_state(client, deployment_id, DeploymentState.FAILED)
    response = client.post(f"/api/v1/deployments/{deployment_id}/retry")
    assert response.status_code == 200
    body = response.json()
    assert body["deployment_id"] == deployment_id
    assert body["model_id"] == deployment["model_id"]
    assert body["version"] == "1.0.0"
    assert body["environment"] == DeploymentEnvironment.DEV
    assert body["status"] == DeploymentState.REQUESTED
    assert body["event"] == DeploymentEvent.RETRY_REQUESTED


@pytest.mark.integration
def test_rollback_deployment_success(client):
    deployment = create_deployment(client)
    deployment_id = deployment["deployment_id"]
    change_deployment_state(client, deployment_id, DeploymentState.VALIDATING)
    change_deployment_state(client, deployment_id, DeploymentState.DEPLOYING)
    change_deployment_state(client, deployment_id, DeploymentState.SUCCEEDED)
    response = client.post(f"/api/v1/deployments/{deployment_id}/rollback")
    assert response.status_code == 200
    body = response.json()
    assert body["deployment_id"] == deployment_id
    assert body["model_id"] == deployment["model_id"]
    assert body["version"] == "1.0.0"
    assert body["environment"] == DeploymentEnvironment.DEV
    assert body["status"] == DeploymentState.ROLLED_BACK
    assert body["event"] == DeploymentEvent.ROLLBACK_STARTED
