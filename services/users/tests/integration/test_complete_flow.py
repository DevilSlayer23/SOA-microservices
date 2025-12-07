import requests
import pytest
import time

BASE_URL = "http://localhost"

def test_complete_ecommerce_flow():
    """Test complete flow: Register -> Add Product -> Cart -> Order"""
    
    # Step 1: Register User
    print("\n1. Registering user...")
    user_response = requests.post(
        f"{BASE_URL}:8001/api/users/register",
        json={
            "email": f"e2e_test_{int(time.time())}@example.com",
            "password": "TestPass123!",
            "name": "E2E Test User"
        }
    )
    assert user_response.status_code == 201
    user_id = user_response.json()["id"]
    print(f"✓ User created: {user_id}")

    # Step 2: Login User
    print("\n2. Logging in...")
    login_response = requests.post(
        f"{BASE_URL}:8001/api/users/login",
        json={
            "email": user_response.json()["email"],
            "password": "TestPass123!"
        }
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    print(f"✓ Login successful, token received")

    # Step 3: Create Product
    print("\n3. Creating product...")
    product_response = requests.post(
        f"{BASE_URL}:8002/api/products",
        json={
            "name": "E2E Test Laptop",
            "description": "Test laptop for E2E testing",
            "price": 999.99,
            "stock": 50,
            "category": "Electronics"
        }
    )
    assert product_response.status_code == 201
    product_id = product_response.json()["id"]
    print(f"✓ Product created: {product_id}")

    # Step 4: Add to Cart
    print("\n4. Adding product to cart...")
    cart_response = requests.post(
        f"{BASE_URL}:8003/api/cart",
        json={
            "userId": user_id,
            "productId": product_id,
            "quantity": 2
        }
    )
    assert cart_response.status_code == 201
    assert len(cart_response.json()["cart"]["items"]) == 1
    print(f"✓ Added to cart, total: ${cart_response.json()['cart']['total']}")

    # Step 5: Get Cart
    print("\n5. Retrieving cart...")
    get_cart_response = requests.get(f"{BASE_URL}:8003/api/cart/{user_id}")
    assert get_cart_response.status_code == 200
    assert len(get_cart_response.json()["items"]) == 1
    print(f"✓ Cart retrieved with {len(get_cart_response.json()['items'])} items")

    # Step 6: Create Order
    print("\n6. Creating order...")
    order_response = requests.post(
        f"{BASE_URL}:8004/api/orders",
        json={
            "userId": user_id,
            "shippingAddress": {
                "street": "123 E2E Test Street",
                "city": "Toronto",
                "postalCode": "M5H 2N2",
                "country": "Canada"
            },
            "paymentMethod": "credit_card"
        }
    )
    assert order_response.status_code == 201
    order_id = order_response.json()["order"]["id"]
    print(f"✓ Order created: {order_id}")

    # Step 7: Verify Cart is Cleared
    print("\n7. Verifying cart was cleared...")
    cleared_cart = requests.get(f"{BASE_URL}:8003/api/cart/{user_id}")
    assert cleared_cart.json()["total"] == 0
    print(f"✓ Cart cleared successfully")

    # Step 8: Verify Product Stock Updated
    print("\n8. Verifying product stock decreased...")
    updated_product = requests.get(f"{BASE_URL}:8002/api/products/{product_id}")
    assert updated_product.json()["stock"] == 48  # 50 - 2
    print(f"✓ Stock updated: {updated_product.json()['stock']}")

    # Step 9: Get Order Details
    print("\n9. Getting order details...")
    order_details = requests.get(f"{BASE_URL}:8004/api/orders/{order_id}")
    assert order_details.status_code == 200
    assert order_details.json()["status"] == "confirmed"
    print(f"✓ Order status: {order_details.json()['status']}")

    print("\n✅ E2E Test Complete - All steps passed!")