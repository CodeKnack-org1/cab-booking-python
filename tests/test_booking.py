from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import pytest
from app.main import app
from app.core.config import settings
from app.db.session import get_db
from app.models.user import User
from app.models.booking import Booking, BookingStatus
from app.core.security import get_password_hash, create_access_token

client = TestClient(app)

@pytest.fixture
def user_token():
    return create_access_token(data={"sub": "test@example.com"})

@pytest.fixture
def auth_headers(user_token):
    return {"Authorization": f"Bearer {user_token}"}

def test_create_booking(auth_headers):
    response = client.post(
        "/api/v1/bookings/",
        headers=auth_headers,
        json={
            "pickup_location": "37.7749,-122.4194",
            "dropoff_location": "37.7833,-122.4167",
            "scheduled_time": "2024-01-01T12:00:00Z"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["pickup_location"] == "37.7749,-122.4194"
    assert data["dropoff_location"] == "37.7833,-122.4167"
    assert data["status"] == BookingStatus.PENDING
    assert "id" in data

def test_get_bookings(auth_headers):
    response = client.get(
        "/api/v1/bookings/",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_booking(auth_headers):
    # First create a booking
    create_response = client.post(
        "/api/v1/bookings/",
        headers=auth_headers,
        json={
            "pickup_location": "37.7749,-122.4194",
            "dropoff_location": "37.7833,-122.4167"
        }
    )
    booking_id = create_response.json()["id"]
    
    # Then get the booking
    response = client.get(
        f"/api/v1/bookings/{booking_id}",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == booking_id

def test_cancel_booking(auth_headers):
    # First create a booking
    create_response = client.post(
        "/api/v1/bookings/",
        headers=auth_headers,
        json={
            "pickup_location": "37.7749,-122.4194",
            "dropoff_location": "37.7833,-122.4167"
        }
    )
    booking_id = create_response.json()["id"]
    
    # Then cancel the booking
    response = client.put(
        f"/api/v1/bookings/{booking_id}/cancel",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == BookingStatus.CANCELLED 