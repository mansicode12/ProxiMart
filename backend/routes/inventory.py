from flask import Blueprint, request, jsonify
from firebase_config import db

inventory_bp = Blueprint("inventory", __name__)

# ✅ Test route
@inventory_bp.route("/", methods=["GET"])
def test_inventory():
    return jsonify({"message": "inventory route is working"})


# ✅ Add a new inventory item for a vendor
@inventory_bp.route("/add", methods=["POST"])
def add_inventory():
    data = request.get_json()
    required_fields = ["vendor_id", "name", "price", "quantity"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    name = data["name"].strip().lower()
    vendor_id = data["vendor_id"].strip()

    try:
        price = float(data["price"])
        quantity = int(data["quantity"])
        threshold = int(data.get("threshold", 0))
    except ValueError:
        return jsonify({"error": "Price must be float, quantity and threshold must be integers"}), 400

    # Check for duplicate
    existing_items = db.collection("inventory") \
        .where("vendor_id", "==", vendor_id) \
        .where("name", "==", name) \
        .limit(1).stream()

    if any(existing_items):
        return jsonify({"error": "Item already exists for this vendor"}), 400

    doc_ref = db.collection("inventory").document()
    item_data = {
        "id": doc_ref.id,
        "vendor_id": vendor_id,
        "name": name,
        "price": price,
        "quantity": quantity,
        "threshold": threshold
    }

    doc_ref.set(item_data)

    return jsonify({"message": "Inventory item added", "item": item_data}), 201


# ✅ Get all inventory items for a given vendor
@inventory_bp.route("/vendor/<vendor_id>", methods=["GET"])
def get_inventory(vendor_id):
    vendor_id = vendor_id.strip()

    inventory_docs = db.collection("inventory") \
        .where("vendor_id", "==", vendor_id).stream()

    items = [doc.to_dict() for doc in inventory_docs]

    return jsonify({"inventory": items}), 200


# ✅ Update inventory by item name and vendor_id
@inventory_bp.route("/update_by_item", methods=["PATCH"])
def update_inventory_by_name():
    data = request.get_json()
    required_fields = ["vendor_id", "name"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing vendor_id or item name"}), 400

    vendor_id = data["vendor_id"].strip()
    name = data["name"].strip().lower()

    query = db.collection("inventory") \
              .where("vendor_id", "==", vendor_id) \
              .where("name", "==", name) \
              .limit(1).stream()

    item_doc = next(query, None)

    if not item_doc:
        return jsonify({"error": "Item not found"}), 404

    item_ref = db.collection("inventory").document(item_doc.id)
    update_data = {}

    if "price" in data:
        try:
            update_data["price"] = float(data["price"])
        except ValueError:
            return jsonify({"error": "Price must be a float"}), 400

    if "quantity" in data:
        try:
            quantity = int(data["quantity"])
            if quantity < 0:
                return jsonify({"error": "Quantity cannot be negative"}), 400
            update_data["quantity"] = quantity
        except ValueError:
            return jsonify({"error": "Quantity must be an integer"}), 400

    if "threshold" in data:
        try:
            threshold = int(data["threshold"])
            if threshold < 0:
                return jsonify({"error": "Threshold cannot be negative"}), 400
            update_data["threshold"] = threshold
        except ValueError:
            return jsonify({"error": "Threshold must be an integer"}), 400

    if not update_data:
        return jsonify({"error": "No valid fields to update"}), 400

    item_ref.update(update_data)
    return jsonify({"message": "Inventory updated", "updated_fields": update_data}), 200


# ✅ Delete inventory item
# ✅ Delete inventory item by vendor_id and item name
@inventory_bp.route("/delete_by_item", methods=["DELETE"])
def delete_inventory_by_item():
    data = request.get_json()

    if not data or "vendor_id" not in data or "name" not in data:
        return jsonify({"error": "Missing 'vendor_id' or 'name' in request body"}), 400

    vendor_id = data["vendor_id"].strip()
    name = data["name"].strip().lower()

    # Search for the item
    query = db.collection("inventory") \
        .where("vendor_id", "==", vendor_id) \
        .where("name", "==", name).limit(1).stream()

    item = next(query, None)

    if not item:
        return jsonify({"error": f"Item '{name}' not found for vendor '{vendor_id}'"}), 404

    db.collection("inventory").document(item.id).delete()

    return jsonify({"message": f"Item '{name}' deleted successfully for vendor '{vendor_id}'"}), 200

# ✅ Get low-stock alerts for a vendor
@inventory_bp.route("/stock_alert/<vendor_id>", methods=["GET"])
def get_stock_alerts(vendor_id):
    vendor_id = vendor_id.strip()

    items = db.collection("inventory").where("vendor_id", "==", vendor_id).stream()

    low_stock_items = []
    for doc in items:
        data = doc.to_dict()
        if "quantity" in data and "threshold" in data:
            if data["quantity"] <= data["threshold"]:
                low_stock_items.append(data)

    return jsonify({"low_stock_items": low_stock_items}), 200

@inventory_bp.route("/add_from_order", methods=["POST"])
def add_from_order():
    data = request.get_json()
    vendor_id = data.get("vendor_id")
    order_id = data.get("order_id")

    if not vendor_id or not order_id:
        return jsonify({"error": "vendor_id and order_id are required"}), 400

    # 1. Get the order
    order_ref = db.collection("orders").document(order_id)
    order = order_ref.get()
    if not order.exists:
        return jsonify({"error": "Order not found"}), 404

    order_data = order.to_dict()
    if order_data.get("status") != "accepted":
        return jsonify({"error": "Order is not accepted yet"}), 400

    if order_data.get("vendor_id") != vendor_id:
        return jsonify({"error": "This order does not belong to the vendor"}), 403

    ordered_items = order_data.get("items", [])

    # 2. Get vendor inventory
    inventory_ref = db.collection("inventory").where("vendor_id", "==", vendor_id)
    inventory_docs = inventory_ref.stream()
    inventory = [doc.to_dict() | {"id": doc.id} for doc in inventory_docs]

    updated_items = []
    for item in ordered_items:
        name = item["name"].lower()
        quantity = item["quantity"]
        price = item.get("price", 0)
        threshold = item.get("threshold", 5)

        # Check if item exists
        match = next((i for i in inventory if i["name"].lower() == name), None)
        if match:
            # Update quantity
            new_quantity = match["quantity"] + quantity
            db.collection("inventory").document(match["id"]).update({
                "quantity": new_quantity
            })
            updated_items.append(f"Updated {name} to {new_quantity}")
        else:
            # Add new item
            new_item = {
                "vendor_id": vendor_id,
                "name": name,
                "quantity": quantity,
                "price": price,
                "threshold": threshold
            }
            db.collection("inventory").add(new_item)
            updated_items.append(f"Added new item: {name}")

    return jsonify({
        "message": "Inventory updated from accepted order.",
        "details": updated_items
    }), 200