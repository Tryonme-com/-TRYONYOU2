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
        "user_id": "test_user",
        "token": "1741164800.mock_sig",
        "waist": 70.0,
        "event_type": "Gala"
    }

    # 3. Send the POST request to the endpoint
    # We need to mock verify_auth to return True as we changed SECRET_KEY to env var
    monkeypatch.setattr("backend.main.verify_auth", lambda u, t: True)

    response = client.post("/api/recommend", json=payload)

    # 4. Assertions
    assert response.status_code == 503

    data = response.json()
    assert data["detail"] == {
        "status": "error",
        "code": 503,
        "message": "Jules AI Engine is currently recalibrating or unavailable. Please try again."
    }
