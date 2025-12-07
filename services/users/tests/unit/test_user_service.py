import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "OK"

def test_register_user():
    """Test user registration"""
    response = client.post(
        "/api/users/register",
        json={
            "email": "test@example.com",
            "password": "TestPass123!",
            "name": "Test User"
        }
    )
    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["email"] == "test@example.com"

def test_register_duplicate_email():
    """Test duplicate email registration fails"""
    # Register first user
    client.post(
        "/api/users/register",
        json={
            "email": "duplicate@example.com",
            "password": "TestPass123!",
            "name": "Test User"
        }
    )
    
    # Try to register with same email
    response = client.post(
        "/api/users/register",
        json={
            "email": "duplicate@example.com",
            "password": "TestPass123!",
            "name": "Test User 2"
        }
    )
    assert response.status_code == 400

def test_login_success():
    """Test successful login"""
    # First register
    client.post(
        "/api/users/register",
        json={
            "email": "login@example.com",
            "password": "TestPass123!",
            "name": "Login Test"
        }
    )
    
    # Then login
    response = client.post(
        "/api/users/login",
        json={
            "email": "login@example.com",
            "password": "TestPass123!"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_credentials():
    """Test login with invalid credentials"""
    response = client.post(
        "/api/users/login",
        json={
            "email": "nonexistent@example.com",
            "password": "WrongPassword"
        }
    )
    assert response.status_code == 401