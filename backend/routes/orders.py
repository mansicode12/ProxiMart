from flask import Blueprint, request, jsonify
from firebase_config import db
from datetime import datetime

orders_bp = Blueprint("orders", __name__)

# ✅ Test route
@orders_bp.route("/", methods=["GET"])
def test_orders():
    return jsonify({"message": "orders route is working"})


# ✅ Place a new order (NO deduction from supplier inventory here)
@orders_bp.route("/place", methods=["POST"])
def place_order():
    data = request.get_json()
    vendor_id = data.get("vendor_id")
    items = data.get("items", [])  # List of {name, quantity, supplier_id}

    if not vendor_id or not items:
        return jsonify({"error": "Missing vendor_id or items"}), 400

    supplier_orders = {}
    for item in items:
        name = item.get("name", "").strip().lower()
        quantity = item.get("quantity")
        supplier_id = item.get("supplier_id")

        if not name or not quantity or not supplier_id:
            return jsonify({"error": f"Missing fields in item: {item}"}), 400

        if supplier_id not in supplier_orders:
            supplier_orders[supplier_id] = []

        supplier_orders[supplier_id].append({"name": name, "quantity": quantity})

    all_orders = []

    for supplier_id, order_items in supplier_orders.items():
        supplier_ref = db.collection("suppliers").document(supplier_id)
        supplier_doc = supplier_ref.get()

        if not supplier_doc.exists:
            return jsonify({"error": f"Supplier '{supplier_id}' not found"}), 404

        supplier_data = supplier_doc.to_dict()
        inventory = supplier_data.get("items", [])

        fulfilled_items = []
        total_cost = 0.0

        for order_item in order_items:
            name = order_item["name"]
            quantity = order_item["quantity"]

            matched_item = next(
                (i for i in inventory if i["name"].strip().lower() == name), None)

            if not matched_item:
                return jsonify({"error": f"Item '{name}' not found in supplier '{supplier_id}' inventory"}), 404

            if matched_item["quantity"] < quantity:
                return jsonify({"error": f"Not enough quantity for '{name}' in supplier '{supplier_id}'"}), 400

            price = matched_item["price"]
            total_cost += price * quantity
            fulfilled_items.append({"name": name, "quantity": quantity, "price": price})

        # Save order (no inventory change yet)
        order_data = {
            "vendor_id": vendor_id,
            "supplier_id": supplier_id,
            "items": fulfilled_items,
            "total_cost": total_cost,
            "status": "pending",
            "timestamp": datetime.utcnow().isoformat()
        }

        order_ref = db.collection("orders").document()
        order_ref.set(order_data)

        order_data["order_id"] = order_ref.id
        all_orders.append(order_data)

    return jsonify({"message": "Orders placed successfully", "orders": all_orders})


# ✅ Accept order by supplier (Deduct supplier inventory + Add to vendor inventory)
@orders_bp.route("/accept", methods=["POST"])
def accept_order():
    data = request.get_json()
    order_id = data.get("order_id")
    supplier_id = data.get("supplier_id")

    if not order_id or not supplier_id:
        return jsonify({"error": "order_id and supplier_id are required"}), 400

    order_ref = db.collection("orders").document(order_id)
    order_doc = order_ref.get()

    if not order_doc.exists:
        return jsonify({"error": "Order not found"}), 404

    order_data = order_doc.to_dict()

    if order_data["supplier_id"] != supplier_id:
        return jsonify({"error": "Unauthorized supplier"}), 403

    vendor_id = order_data["vendor_id"]
    order_items = order_data["items"]

    # ✅ Step 1: Deduct from supplier inventory
    supplier_ref = db.collection("suppliers").document(supplier_id)
    supplier_doc = supplier_ref.get()

    if not supplier_doc.exists:
        return jsonify({"error": "Supplier not found"}), 404

    supplier_data = supplier_doc.to_dict()
    supplier_inventory = supplier_data.get("items", [])

    for item in order_items:
        name = item["name"].strip().lower()
        quantity = item["quantity"]

        matched_item = next((i for i in supplier_inventory if i["name"].strip().lower() == name), None)

        if not matched_item:
            return jsonify({"error": f"Item '{name}' not found in supplier '{supplier_id}'"}), 404

        if matched_item["quantity"] < quantity:
            return jsonify({"error": f"Not enough stock of '{name}' with supplier '{supplier_id}'"}), 400

        matched_item["quantity"] -= quantity

    supplier_ref.update({"items": supplier_inventory})

    # ✅ Step 2: Add to vendor inventory
    inventory_ref = db.collection("inventory").document(vendor_id)
    inventory_doc = inventory_ref.get()
    existing_items = inventory_doc.to_dict().get("items", []) if inventory_doc.exists else []
    inventory_map = {item["name"].lower(): item for item in existing_items}

    for item in order_items:
        name = item["name"].strip().lower()
        quantity = item["quantity"]
        price = item.get("price", 0.0)

        if name in inventory_map:
            inventory_map[name]["quantity"] += quantity
        else:
            inventory_map[name] = {
                "name": name,
                "quantity": quantity,
                "price": price,
                "threshold": 0
            }

    inventory_ref.set({"items": list(inventory_map.values())})

    # ✅ Step 3: Mark order as accepted
    order_ref.update({
        "status": "accepted",
        "accepted_at": datetime.utcnow()
    })

    return jsonify({"message": "Order accepted. Inventory updated."}), 200


# ✅ Order history for a vendor
@orders_bp.route("/history", methods=["GET"])
def get_order_history():
    vendor_id = request.args.get("vendor_id")
    if not vendor_id:
        return jsonify({"error": "Missing vendor_id"}), 400

    try:
        orders_ref = db.collection("orders").where("vendor_id", "==", vendor_id)
        docs = orders_ref.stream()

        history = []
        for doc in docs:
            order = doc.to_dict()
            order["order_id"] = doc.id
            history.append(order)

        return jsonify({"orders": sorted(history, key=lambda x: x.get("timestamp", ""), reverse=True)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500