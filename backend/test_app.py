import pytest
from app import app as flask_app
from firebase_config import db

@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client

# ---------- SUPPLIERS ROUTES TESTS ----------

def test_suppliers_root(client):
    response = client.get("/api/suppliers/")
    assert response.status_code == 200
    assert response.get_json() == {"message": "Suppliers route is working"}

def test_add_supplier(client):
    response = client.post("/api/suppliers/add", json={
        "name": "Test Supplier",
        "items": ["onions"],
        "location": {"lat": 28.6139, "lon": 77.2090},
        "rating": 4.5
    })
    assert response.status_code == 201
    assert response.get_json()["message"] == "Supplier added successfully"

def test_add_supplier_missing_fields(client):
    response = client.post("/api/suppliers/add", json={"name": "Incomplete"})
    assert response.status_code == 400

def test_get_nearby_suppliers_missing_params(client):
    response = client.get("/api/suppliers/nearby")
    assert response.status_code == 400

def test_get_all_suppliers(client):
    response = client.get("/api/suppliers/all")
    assert response.status_code == 200
    assert "suppliers" in response.get_json()

# ---------- ORDERS ROUTES TESTS ----------

def test_orders_root(client):
    response = client.get("/api/orders/")
    assert response.status_code == 200
    assert response.get_json() == {"message": "orders route is working"}

def test_place_order(client):
    response = client.post("/api/orders/place", json={
        "vendor_id": "dummy_vendor_id",
        "item": "onions",
        "quantity": 10,
        "buyer": "Test Buyer"
    })
    assert response.status_code in (201, 200, 400)  # 400 if vendor_id doesn't exist

def test_place_order_missing_fields(client):
    response = client.post("/api/orders/place", json={"vendor_id": "x"})
    assert response.status_code == 400

def test_order_history_missing_param(client):
    response = client.get("/api/orders/history")
    assert response.status_code == 400

# ---------- INVENTORY ROUTES TESTS ----------

def test_inventory_root(client):
    response = client.get("/api/inventory/")
    assert response.status_code == 200
    assert response.get_json() == {"message": "inventory route is working"}

def test_add_inventory(client):
    response = client.post("/api/inventory/add", json={
        "vendor_id": "test_vendor",
        "item": "Tomatoes",
        "quantity": 100,
        "price": 20.0
    })
    assert response.status_code == 200
    assert "inventory_id" in response.get_json()

def test_add_inventory_missing_fields(client):
    response = client.post("/api/inventory/add", json={"vendor_id": "x"})
    assert response.status_code == 400

def test_get_vendor_inventory(client):
    response = client.get("/api/inventory/vendor/test_vendor")
    assert response.status_code == 200
    assert "vendor_inventory" in response.get_json()

def test_update_after_order_invalid(client):
    response = client.post("/api/inventory/update_after_order", json={
        "vendor_id": "test_vendor",
        "item": "Tomatoes",
        "quantity": 9999
    })
    assert response.status_code in (200, 400)

def test_edit_inventory_invalid_fields(client):
    response = client.patch("/api/inventory/edit/some_fake_id", json={})
    assert response.status_code == 400

def test_delete_inventory_fake(client):
    response = client.delete("/api/inventory/delete/some_fake_id")
    assert response.status_code in (200, 404)

# ---------- HELP/FAQ ROUTE ----------

def test_faqs(client):
    response = client.get("/api/help/faqs")
    assert response.status_code == 200
    assert "faqs" in response.get_json()

# ---------- 404 ROUTE ----------

def test_invalid_route(client):
    response = client.get("/non-existent-route")
    assert response.status_code == 404
    assert "error" in response.get_json()
