import pytest
import hmac
import hashlib
import time
from fastapi.testclient import TestClient
from backend.main import app, SECRET_KEY

client = TestClient(app)

def generate_test_token(user_id: str):
    ts = str(int(time.time()))
    sig = hmac.new(SECRET_KEY.encode(), f"{user_id}:{ts}".encode(), hashlib.sha256).hexdigest()
    return f"{ts}.{sig}"

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
    user_id = "test_user_123"
    payload = {
        "user_id": user_id,
        "token": generate_test_token(user_id),
        "waist": 72.0,
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
