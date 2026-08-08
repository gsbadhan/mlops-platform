import pytest


@pytest.mark.integration
def test_create_model_success(client):
    create_response = client.post(
        "/api/v1/models",
        json={
            "name": "fraud-detection",
            "description": "Fraud detection model",
            "owner": "mlops-team",
            "framework": "scikit-learn",
            "algorithm": "Random Forest",
        },
    )

    assert create_response.status_code == 201

    model = create_response.json()
    model_id = model["id"]

    response = client.get(f"/api/v1/models/{model_id}")

    assert response.status_code == 200

    body = response.json()

    print(body)
    assert body["id"] == model_id
    assert body["name"] == "fraud-detection"
    assert body["description"] == "Fraud detection model"
    assert body["owner"] == "mlops-team"
    assert body["framework"] == "scikit-learn"
    # assert body["algorithm"] == "Random Forest"


@pytest.mark.integration
def test_get_models_success(client):
    response = client.get("/api/v1/models")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)


@pytest.mark.integration
def test_get_model_success(client):
    create_response = client.post(
        "/api/v1/models",
        json={
            "name": "fraud-detection",
            "description": "Fraud detection model",
            "owner": "mlops-team",
            "framework": "scikit-learn",
            "algorithm": "Random Forest",
        },
    )

    assert create_response.status_code == 201
    model = create_response.json()
    model_id = model["id"]
    response = client.get(f"/api/v1/models/{model_id}")
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == model_id
    assert body["name"] == "fraud-detection"
    assert body["description"] == "Fraud detection model"
    assert body["owner"] == "mlops-team"
    assert body["framework"] == "scikit-learn"


@pytest.mark.integration
def test_get_model_not_found(client):
    model_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/api/v1/models/{model_id}")
    assert response.status_code == 404


@pytest.mark.integration
def test_create_model_validation_error(client):
    payload = {"name": "fraud-detection", "description": "short"}
    response = client.post("/api/v1/models", json=payload)
    assert response.status_code == 422
    body = response.json()
    assert "message" in body
    assert "errors" in body
    assert isinstance(body["errors"], list)
