import pytest
from fastapi.testclient import TestClient
from backend.main import app
import os

client = TestClient(app)

def test_verify_staff_success(monkeypatch):
    # Set a known staff password for testing
    monkeypatch.setenv("STAFF_PASSWORD", "TEST_STAFF_PASS")
    # Reload the app's STAFF_PASSWORD from env
    import backend.main
    monkeypatch.setattr(backend.main, "STAFF_PASSWORD", "TEST_STAFF_PASS")

    response = client.post("/api/verify-staff", json={"password": "TEST_STAFF_PASS"})
    assert response.status_code == 200
    assert response.json()["status"] == "SUCCESS"

def test_verify_staff_failure(monkeypatch):
    monkeypatch.setenv("STAFF_PASSWORD", "TEST_STAFF_PASS")
    import backend.main
    monkeypatch.setattr(backend.main, "STAFF_PASSWORD", "TEST_STAFF_PASS")

    response = client.post("/api/verify-staff", json={"password": "WRONG_PASSWORD"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Acceso denegado"

def test_verify_staff_empty_password(monkeypatch):
    monkeypatch.setenv("STAFF_PASSWORD", "TEST_STAFF_PASS")
    import backend.main
    monkeypatch.setattr(backend.main, "STAFF_PASSWORD", "TEST_STAFF_PASS")

    response = client.post("/api/verify-staff", json={"password": ""})
    assert response.status_code == 401
