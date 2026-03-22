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
    from the Jules AI engine (get_jules_advice) by returning a 200 OK
    with a fallback recommendation string.
    """
    # 1. Mock the get_jules_advice function to raise an exception
    def mock_get_jules_advice(*args, **kwargs):
        raise Exception("Simulated AI Engine Failure")

    # Use monkeypatch to replace the real function with our mock
    monkeypatch.setattr("backend.main.get_jules_advice", mock_get_jules_advice)

    # 2. Prepare valid authentication
    user_id = "test_user_123"
    ts = int(time.time())
    sig = hmac.new(SECRET_KEY.encode(), f"{user_id}:{ts}".encode(), hashlib.sha256).hexdigest()
    token = f"{ts}.{sig}"

    # 3. Prepare the request payload matching UserScan model
    payload = {
        "user_id": user_id,
        "token": token,
        "waist": 74.75, # 74.75 / (65 * 1.15) = 1.0 (Perfect fit for BALMAIN_SS26_SLIM)
        "event_type": "Gala"
    }

    # 4. Send the POST request to the endpoint
    # Note: the endpoint also takes a garment_id as a query param, defaults to "BALMAIN_SS26_SLIM"
    response = client.post("/api/recommend", json=payload)

    # 5. Assertions
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "SUCCESS"
    assert "styling_advice" in data
    assert "Balmain Slim-Fit Jeans" in data["styling_advice"]
