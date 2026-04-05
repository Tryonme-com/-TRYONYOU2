import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_verify_staff_success():
    """Test successful staff verification with correct password."""
    response = client.post("/api/verify-staff", json={"password": "SAC_MUSEUM_2026"})
    assert response.status_code == 200
    assert response.json() == {"status": "SUCCESS", "message": "Acceso concedido al búnker."}

def test_verify_staff_failure():
    """Test failed staff verification with incorrect password."""
    response = client.post("/api/verify-staff", json={"password": "WRONG_PASSWORD"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Credencial de acceso denegada."}

def test_verify_staff_empty():
    """Test staff verification with empty password."""
    response = client.post("/api/verify-staff", json={"password": ""})
    assert response.status_code == 401
    assert response.json() == {"detail": "Credencial de acceso denegada."}
