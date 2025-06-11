from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import pytest
from app.main import app
from app.core.config import settings
from app.db.session import get_db
from app.models.user import User
from app.models.booking import Booking
from app.models.payment import Payment, PaymentStatus, PaymentMethod
from app.core.security import get_password_hash, create_access_token

client = TestClient(app)

@pytest.fixture
def user_token():
    return create_access_token(data={"sub": "test@example.com"})

@pytest.fixture
def auth_headers(user_token):
    return {"Authorization": f"Bearer {user_token}"}

@pytest.fixture
def booking_id(auth_headers):
    # Create a booking first
    response = client.post(
        "/api/v1/bookings/",
        headers=auth_headers,
        json={
            "pickup_location": "37.7749,-122.4194",
            "dropoff_location": "37.7833,-122.4167"
        }
    )
    return response.json()["id"]

def test_create_payment(auth_headers, booking_id):
    response = client.post(
        "/api/v1/payments/",
        headers=auth_headers,
        json={
            "booking_id": booking_id,
            "amount": 25.50,
            "payment_method": PaymentMethod.CREDIT_CARD
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["booking_id"] == booking_id
    assert data["amount"] == 25.50
    assert data["payment_method"] == PaymentMethod.CREDIT_CARD
    assert data["status"] == PaymentStatus.PENDING
    assert "id" in data

def test_get_payments(auth_headers):
    response = client.get(
        "/api/v1/payments/",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_payment(auth_headers, booking_id):
    # First create a payment
    create_response = client.post(
        "/api/v1/payments/",
        headers=auth_headers,
        json={
            "booking_id": booking_id,
            "amount": 25.50,
            "payment_method": PaymentMethod.CREDIT_CARD
        }
    )
    payment_id = create_response.json()["id"]
    
    # Then get the payment
    response = client.get(
        f"/api/v1/payments/{payment_id}",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == payment_id

def test_refund_payment(auth_headers, booking_id):
    # First create a payment
    create_response = client.post(
        "/api/v1/payments/",
        headers=auth_headers,
        json={
            "booking_id": booking_id,
            "amount": 25.50,
            "payment_method": PaymentMethod.CREDIT_CARD
        }
    )
    payment_id = create_response.json()["id"]
    
    # Then refund the payment
    response = client.put(
        f"/api/v1/payments/{payment_id}/refund",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == PaymentStatus.REFUNDED 