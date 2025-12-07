import requests;
import pytest
import time
from decouple import config

BASE_URL = config("BASE_URL", default="http://localhost:8001") # pip or use minikube IP for k8s

@pytest.fixture(scope="module")
def setup_test_data():
    """Create test user and product before running tests"""
    # Create user
    user_response = requests.post(
        f"{BASE_URL}:8001/api/users/register",
        json={
            "email": f"integration_test_{int(time.time())}@example.com",
            "password": "TestPass123!",
            "name": "Integration Test User"
        }
    )
    assert user_response.status_code == 201
    user_id = user_response.json()["id"]

    # Create product
    product_response = requests.post(
        f"{BASE_URL}:8002/api/products",
        json={
            "name": "Test Product",
            "description": "Integration test product",
            "price": 99.99,
            "stock": 100,
            "category": "Test"
        }
    )
    assert product_response.status_code == 201
    product_id = product_response.json()["id"]

    yield {"user_id": user_id, "product_id": product_id}

def test_cart_validates_user(setup_test_data):
    """Test that cart service validates user exists"""
    response = requests.post(
        f"{BASE_URL}:8003/api/cart",
        json={
            "userId": "non-existent-user",
            "productId": setup_test_data["product_id"],
            "quantity": 1
        }
    )
    assert response.status_code == 404
    assert "user" in response.json()["error"].lower()

def test_cart_validates_product(setup_test_data):
    """Test that cart service validates product exists"""
    response = requests.post(
        f"{BASE_URL}:8003/api/cart",
        json={
            "userId": setup_test_data["user_id"],
            "productId": "non-existent-product",
            "quantity": 1
        }
    )
    assert response.status_code == 404
    assert "product" in response.json()["error"].lower()

def test_add_to_cart_success(setup_test_data):
    """Test successful add to cart with valid user and product"""
    response = requests.post(
        f"{BASE_URL}:8003/api/cart",
        json={
            "userId": setup_test_data["user_id"],
            "productId": setup_test_data["product_id"],
            "quantity": 2
        }
    )
    assert response.status_code == 201
    assert response.json()["cart"]["items"][0]["quantity"] == 2

def test_orders_validates_cart(setup_test_data):
    """Test that orders service validates cart exists"""
    response = requests.post(
        f"{BASE_URL}:8004/api/orders",
        json={
            "userId": setup_test_data["user_id"],
            "shippingAddress": {
                "street": "123 Test St",
                "city": "TestCity",
                "postalCode": "12345",
                "country": "TestCountry"
            },
            "paymentMethod": "credit_card"
        }
    )
    # Should fail if cart is empty
    assert response.status_code in [400, 404]