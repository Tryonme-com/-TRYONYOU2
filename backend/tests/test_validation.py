import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_recommend_garment_validation_error():
    """
    Test that the /api/recommend endpoint returns a 422 Unprocessable Entity
    when invalid data is provided (violating Pydantic constraints).
    """
    # 1. Prepare invalid request payloads
    invalid_payloads = [
        {"height": 10.0, "weight": 68.0, "event_type": "Gala"},  # height too small
        {"height": 175.0, "weight": 500.0, "event_type": "Gala"}, # weight too large
        {"height": 175.0, "weight": 68.0, "event_type": ""},      # event_type too short
    ]

    for payload in invalid_payloads:
        # 2. Send the POST request to the endpoint
        response = client.post("/api/recommend", json=payload)

        # 3. Assertions
        assert response.status_code == 422
