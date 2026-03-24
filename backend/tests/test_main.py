import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_recommend_garment_engine_failure(monkeypatch):
    """
    Test that the /api/recommend endpoint correctly handles failures
    from the Jules AI engine (get_jules_advice).
    """
    # 1. Mock verify_auth to allow access
    monkeypatch.setattr("backend.main.verify_auth", lambda u, t: True)

    # 2. Mock the get_jules_advice function to raise an exception
    def mock_get_jules_advice(*args, **kwargs):
        raise Exception("Simulated AI Engine Failure")

    # Use monkeypatch to replace the real function with our mock
    monkeypatch.setattr("backend.main.get_jules_advice", mock_get_jules_advice)

    # 3. Prepare the request payload matching UserScan model
    payload = {
        "user_id": "TEST_USER",
        "token": "MOCKED_TOKEN",
        "waist": 70.0,
        "event_type": "Gala"
    }

    # 4. Send the POST request to the endpoint
    response = client.post("/api/recommend?garment_id=BALMAIN_SS26_SLIM", json=payload)

    # 5. Assertions
    # Note: main.py catches the exception and provides a fallback, returning 200 SUCCESS or RESCAN
    assert response.status_code == 200
    data = response.json()
    assert "styling_advice" in data
    assert "Balmain Slim-Fit Jeans" in data["styling_advice"] or "prenda" in data["styling_advice"] or "Divineo" in data["styling_advice"]
