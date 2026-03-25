import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_verify_staff_success(monkeypatch):
    """Test successful staff verification."""
    # Mock STAFF_PASSWORD in main module
    monkeypatch.setattr("backend.main.STAFF_PASSWORD", "TEST_STAFF_PASS")

    payload = {"password": "TEST_STAFF_PASS"}
    response = client.post("/api/verify-staff", json=payload)

    assert response.status_code == 200
    assert response.json() == {"status": "SUCCESS", "message": "Access granted"}

def test_verify_staff_failure(monkeypatch):
    """Test failed staff verification."""
    # Mock STAFF_PASSWORD in main module
    monkeypatch.setattr("backend.main.STAFF_PASSWORD", "TEST_STAFF_PASS")

    payload = {"password": "WRONG_PASS"}
    response = client.post("/api/verify-staff", json=payload)

    assert response.status_code == 401
    assert response.json()["detail"] == "Access denied"

def test_verify_staff_empty_password(monkeypatch):
    """Test verification with empty password."""
    monkeypatch.setattr("backend.main.STAFF_PASSWORD", "TEST_STAFF_PASS")

    payload = {"password": ""}
    response = client.post("/api/verify-staff", json=payload)

    assert response.status_code == 401
