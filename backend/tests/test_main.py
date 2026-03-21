import pytest
import hmac
import hashlib
import time
from fastapi.testclient import TestClient
from backend.main import app, SECRET_KEY

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

    # 2. Prepare the request payload with a valid HMAC token
    user_id = "TEST_USER"
    ts = int(time.time())
    sig = hmac.new(SECRET_KEY.encode(), f"{user_id}:{ts}".encode(), hashlib.sha256).hexdigest()
    token = f"{ts}.{sig}"

    payload = {
        "user_id": user_id,
        "token": token,
        "waist": 70.0,
        "event_type": "Gala"
    }

    # 3. Send the POST request to the endpoint
    response = client.post("/api/recommend?garment_id=BALMAIN_SS26_SLIM", json=payload)

    # 4. Assertions
    # We expect 200 OK because the backend implements a fallback for AI engine failures
    assert response.status_code == 200

    data = response.json()
    assert "styling_advice" in data
    assert "Balmain Slim-Fit Jeans" in data["styling_advice"]
