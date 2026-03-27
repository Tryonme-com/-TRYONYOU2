import pytest
from fastapi.testclient import TestClient
from backend.main import app
import os

client = TestClient(app)

def test_verify_staff_success():
    """Test successful staff verification."""
    # The default password in main.py if STAFF_PASSWORD is not set is 'SAC_MUSEUM_2026'
    payload = {"password": "SAC_MUSEUM_2026"}
    response = client.post("/api/verify-staff", json=payload)
    assert response.status_code == 200
    assert response.json() == {"status": "SUCCESS", "message": "ACCESO CONCEDIDO"}

def test_verify_staff_failure():
    """Test failed staff verification with wrong password."""
    payload = {"password": "WRONG_PASSWORD"}
    response = client.post("/api/verify-staff", json=payload)
    assert response.status_code == 401
    assert response.json()["detail"] == "ACCESO DENEGADO"

def test_verify_staff_empty():
    """Test staff verification with empty password."""
    payload = {"password": ""}
    response = client.post("/api/verify-staff", json=payload)
    assert response.status_code == 401
    assert response.json()["detail"] == "ACCESO DENEGADO"

def test_verify_staff_custom_env(monkeypatch):
    """Test staff verification with a custom environment variable password."""
    monkeypatch.setenv("STAFF_PASSWORD", "CUSTOM_SECRET_123")
    # We need to reload the app or at least the STAFF_PASSWORD variable in main.py
    # Since STAFF_PASSWORD is a module-level variable in main.py, we patch it directly
    monkeypatch.setattr("backend.main.STAFF_PASSWORD", "CUSTOM_SECRET_123")

    payload = {"password": "CUSTOM_SECRET_123"}
    response = client.post("/api/verify-staff", json=payload)
    assert response.status_code == 200
    assert response.json() == {"status": "SUCCESS", "message": "ACCESO CONCEDIDO"}
