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

    # Mock verify_auth to bypass security handshake for this test
    monkeypatch.setattr("backend.main.verify_auth", lambda u, t: True)

    # Use monkeypatch to replace the real function with our mock
    monkeypatch.setattr("backend.main.get_jules_advice", mock_get_jules_advice)

    # 2. Prepare the request payload
    # Must match UserScan model in backend/models.py
    payload = {
        "user_id": "TEST_USER",
        "token": "0.TEST_TOKEN", # This will fail verify_auth due to timestamp, but get_jules_advice is called later
        "waist": 70.0,
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
