"""
Tests for the Churn Prediction API.

Run with:
    pytest tests/ -v
    pytest tests/ -v --cov=app --cov=main --cov-report=term-missing
"""

import pytest

from app.model_utils import predict_churn

# ---------------------------------------------------------------------------
# Function Tests
# ---------------------------------------------------------------------------


# TODO 1: Write a test that calls predict_churn() directly with sample features
#         and asserts the result is 0 or 1
#         Hint: import predict_churn from app.model_utils
def test_predict_churn_direct():
    sample = [619.0, "France", "Female", 42.0, 2.0, 0.0, 1.0, 1.0, 1.0, 101348.88]
    # If your model utils expects exactly 10 features natively
    prediction = predict_churn(sample)
    assert prediction in (0, 1), f"Expected 0 or 1, got {prediction}"


# TODO 2 (bonus): Write another function test with edge-case inputs
def test_predict_churn_edge_case():

    edge_sample = [10.0, "Germany", "Female", "big", 1.0, 1000.0, 1.0, 1.0, 1.0, 500.0]

    with pytest.raises(ValueError):
        predict_churn(edge_sample)
    # make it accepted when fails due to input validation, which is also a valid outcome using with pytest.raises(ValueError):
    #     predict_churn(edge_sample)


# ---------------------------------------------------------------------------
# Endpoint Tests
# ---------------------------------------------------------------------------


# # TODO 3: Write a test that POSTs to /predict with valid JSON
# #         and checks the status code and response body
# #         Hint: Litestar POST returns 201, not 200
# #         Hint: use `with TestClient(app=app) as client:`\
# def test_predict_endpoint_valid():
#     valid_payload = {
#         "CreditScore": 619,
#         "Geography": "France",
#         "Gender": "Female",
#         "Age": 42,
#         "Tenure": 2,
#         "Balance": 0,
#         "NumOfProducts": 1,
#         "HasCrCard": 1,
#         "IsActiveMember": 1,
#         "EstimatedSalary": 101348.88,
#     }
#     with TestClient(app=app) as client:
#         response = client.post("/predict", json=valid_payload)
#         assert response.status_code == 201
#         assert "prediction" in response.json()
#         assert response.json()["prediction"] in (0, 1)


# # TODO 4: Write a test for GET /health
# def test_health_endpoint():
#     with TestClient(app=app) as client:
#         response = client.get("/health")
#         assert response.status_code == 200
#         assert response.json() == {"status": "healthy"}


# # TODO 5: Write a test for GET /
# def test_home_endpoint():
#     with TestClient(app=app) as client:
#         response = client.get("/")
#         assert response.status_code == 200
#         assert response.json() == {"message": "Welcome to the Churn Prediction API!"}


# # TODO 6 (bonus): Test that invalid input returns status 400
# def test_predict_endpoint_invalid():
#     invalid_payload = {
#         "CreditScore": "invalid_string_instead_of_number"
#         # Missing other required fields as well will trigger a validation error
#     }
#     with TestClient(app=app) as client:
#         response = client.post("/predict", json=invalid_payload)
#         assert response.status_code == 400
