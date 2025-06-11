from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import pytest
from app.main import app
from app.core.config import settings
from app.db.session import get_db
from app.models.user import User
from app.core.security import get_password_hash

client = TestClient(app)

def test_register():
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "testpassword",
            "full_name": "Test User",
            "phone_number": "1234567890"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
    assert data["phone_number"] == "1234567890"
    assert "id" in data

def test_login():
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "test@example.com",
            "password": "testpassword"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_password_reset():
    response = client.post(
        "/api/v1/auth/password-reset",
        json={
            "email": "test@example.com"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["msg"] == "Password recovery email sent"

def test_password_reset_confirm():
    response = client.post(
        "/api/v1/auth/password-reset/confirm",
        json={
            "token": "test-token",
            "new_password": "newpassword"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["msg"] == "Password updated successfully" 