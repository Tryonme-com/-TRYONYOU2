import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_recommend_garment_engine_failure(monkeypatch):
    """
    Test that the /api/recommend endpoint correctly handles failures
    from the Jules AI engine (get_jules_advice) and returns a 503
    Service Unavailable with a gracefully structured JSON error.
    """
    # 1. Mock the get_jules_advice function to raise an exception
    def mock_get_jules_advice(*args, **kwargs):
        raise Exception("Simulated AI Engine Failure")

    # Use monkeypatch to replace the real function with our mock
    monkeypatch.setattr("backend.main.get_jules_advice", mock_get_jules_advice)

    # 2. Prepare the request payload
    payload = {
        "height": 175.0,
        "weight": 68.0,
        "event_type": "Gala"
    }

    # 3. Send the POST request to the endpoint
    response = client.post("/api/recommend", json=payload)

    # 4. Assertions
    assert response.status_code == 503

    data = response.json()
    assert data == {
        "status": "error",
        "code": 503,
        "message": "Jules AI Engine is currently recalibrating or unavailable. Please try again."
    }

def test_recommend_garment_validation_error():
    """
    Test that the /api/recommend endpoint rejects invalid inputs with a 422
    Unprocessable Entity response due to the Pydantic constraints.
    """
    # 1. Prepare invalid request payloads
    invalid_payloads = [
        {"height": 20.0, "weight": 68.0, "event_type": "Gala"},  # Height too small
        {"height": 350.0, "weight": 68.0, "event_type": "Gala"}, # Height too large
        {"height": 175.0, "weight": 10.0, "event_type": "Gala"},  # Weight too small
        {"height": 175.0, "weight": 600.0, "event_type": "Gala"}, # Weight too large
        {"height": 175.0, "weight": 68.0, "event_type": "A" * 101} # Event type too long
    ]

    for payload in invalid_payloads:
        response = client.post("/api/recommend", json=payload)
        assert response.status_code == 422
