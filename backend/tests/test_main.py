import pytest
import hmac
import hashlib
import time
from fastapi.testclient import TestClient
from backend.main import app, SECRET_KEY

client = TestClient(app)

def test_recommend_garment_engine_fallback(monkeypatch):
    """
    Test that the /api/recommend endpoint correctly handles failures
    from the Jules AI engine (get_jules_advice) and returns a 200
    with a fallback recommendation string.
    """
    # 1. Mock the get_jules_advice function to raise an exception
    def mock_get_jules_advice(*args, **kwargs):
        raise Exception("Simulated AI Engine Failure")

    # Use monkeypatch to replace the real function with our mock
    monkeypatch.setattr("backend.main.get_jules_advice", mock_get_jules_advice)

    # 2. Prepare the request payload with valid auth
    user_id = "LAFAYETTE_USER"
    ts = str(int(time.time()))
    sig = hmac.new(SECRET_KEY.encode(), f"{user_id}:{ts}".encode(), hashlib.sha256).hexdigest()
    token = f"{ts}.{sig}"

    payload = {
        "user_id": user_id,
        "token": token,
        "waist": 70.0,
        "event_type": "Gala"
    }

    # 3. Send the POST request to the endpoint
    response = client.post("/api/recommend", json=payload)

    # 4. Assertions
    assert response.status_code == 200

    data = response.json()
    # It should contain the fallback styling advice
    assert "Divineo confirmado con" in data["styling_advice"]
