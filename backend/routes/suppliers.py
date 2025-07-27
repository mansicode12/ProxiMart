from flask import Blueprint, request, jsonify
from firebase_config import db
from utils.geo_utils import calculate_distance

suppliers_bp = Blueprint("suppliers", __name__)

def paginate(items, page, limit):
    start = (page - 1) * limit
    return items[start:start + limit]

def filter_suppliers(suppliers, items_filter, min_rating, min_quantity, min_price, max_price, search_term, require_all_items):
    filtered = []

    for supplier in suppliers:
        supplier_name = supplier.get("name", "").lower()
        supplier_id = supplier.get("id", "").lower()

        if search_term and search_term not in supplier_name and search_term not in supplier_id:
            continue

        if min_rating and supplier.get("rating", 0) < min_rating:
            continue

        supplier_items = supplier.get("items", [])
        matched_items = []

        for item in supplier_items:
            name = item.get("name", "").lower()
            quantity = item.get("quantity", 0)
            price = item.get("price", 0)

            if items_filter and name not in items_filter:
                continue
            if min_quantity and quantity < min_quantity:
                continue
            if min_price and price < min_price:
                continue
            if max_price and price > max_price:
                continue

            matched_items.append(item)

        if items_filter:
            item_names_matched = [item["name"].lower() for item in matched_items]
            if require_all_items:
                if not all(item in item_names_matched for item in items_filter):
                    continue
            else:
                if not any(item in item_names_matched for item in items_filter):
                    continue

        if (items_filter or min_price or max_price or min_quantity) and not matched_items:
            continue

        # Override supplier items only if filters are applied
        if items_filter or min_price or max_price or min_quantity:
            supplier['items'] = matched_items

        filtered.append(supplier)

    return filtered


# ✅ Supplier add / registration route
@suppliers_bp.route("/add", methods=["POST"])
def add_supplier():
    data = request.get_json()
    required_fields = ["supplier_id", "name", "location", "items"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    supplier_id = data["supplier_id"].strip()
    name = data["name"].strip()
    location = data["location"]
    items = data["items"]

    # Check if supplier_id already exists
    existing_doc = db.collection("suppliers").document(supplier_id).get()
    if existing_doc.exists:
        return jsonify({"error": "Supplier ID already exists"}), 400

    if not isinstance(location, dict) or "lat" not in location or "lon" not in location:
        return jsonify({"error": "Location must be a dict with 'lat' and 'lon'"}), 400

    if not isinstance(items, list) or len(items) == 0:
        return jsonify({"error": "Items must be a non-empty list"}), 400

    for item in items:
        if not all(k in item for k in ["name", "price", "quantity"]):
            return jsonify({"error": "Each item must have name, price, and quantity"}), 400
        try:
            item["price"] = float(item["price"])
            item["quantity"] = int(item["quantity"])
        except ValueError:
            return jsonify({"error": "Price must be float and quantity must be int"}), 400
        item["name"] = item["name"].strip()

    rating = float(data.get("rating", 0))

    supplier_data = {
        "name": name,
        "location": location,
        "items": items,
        "rating": rating
    }
    db.collection("suppliers").document(supplier_id).set(supplier_data)
    supplier_data["id"] = supplier_id

    return jsonify({"message": "Supplier added successfully", "supplier": supplier_data}), 201


# ✅ Get all suppliers with filters
@suppliers_bp.route("/all", methods=["GET"])
def get_all_suppliers():
    all_docs = db.collection("suppliers").stream()
    suppliers = []
    for doc in all_docs:
        data = doc.to_dict()
        data["id"] = doc.id
        suppliers.append(data)

    # Query parameters
    item_param = request.args.get("items")
    items_filter = [i.strip().lower() for i in item_param.split(",")] if item_param else None
    min_rating = float(request.args.get("min_rating", 0))
    min_quantity = int(request.args.get("min_quantity", 0))
    min_price = float(request.args.get("min_price", 0))
    max_price = float(request.args.get("max_price", float("inf")))
    sort_by = request.args.get("sort_by", "").lower()
    search_term = request.args.get("search", "").lower()
    require_all_items = request.args.get("require_all", "true").lower() == "true"
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))

    filtered = filter_suppliers(suppliers, items_filter, min_rating, min_quantity, min_price, max_price, search_term, require_all_items)

    if sort_by == "rating":
        filtered.sort(key=lambda x: x.get("rating", 0), reverse=True)

    paginated = paginate(filtered, page, limit)

    total = len(filtered)
    total_pages = (total + limit - 1) // limit

    return jsonify({
        "suppliers": paginated,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": total_pages
    })


# ✅ Get nearby suppliers with filters and distance
@suppliers_bp.route("/nearby", methods=["GET"])
def get_nearby_suppliers():
    try:
        lat = float(request.args.get("lat"))
        lon = float(request.args.get("lon"))
    except (TypeError, ValueError):
        return jsonify({"error": "Latitude and longitude must be provided and valid floats"}), 400

    all_docs = db.collection("suppliers").stream()
    suppliers = []
    for doc in all_docs:
        data = doc.to_dict()
        data["id"] = doc.id
        location = data.get("location")
        if location and "lat" in location and "lon" in location:
            dist = calculate_distance(lat, lon, location["lat"], location["lon"])
            data["distance_km"] = round(dist, 2)
            suppliers.append(data)

    item_param = request.args.get("items") or request.args.get("item")
    items_filter = [i.strip().lower() for i in item_param.split(",")] if item_param else None
    min_rating = float(request.args.get("min_rating", 0))
    min_quantity = int(request.args.get("min_quantity", 0))
    min_price = float(request.args.get("min_price", 0))
    max_price = float(request.args.get("max_price", float("inf")))
    search_term = request.args.get("search", "").lower()
    require_all_items = request.args.get("require_all", "true").lower() == "true"
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))

    filtered = filter_suppliers(suppliers, items_filter, min_rating, min_quantity, min_price, max_price, search_term, require_all_items)

    filtered.sort(key=lambda x: x.get("distance_km", float("inf")))

    paginated = paginate(filtered, page, limit)

    total = len(filtered)
    total_pages = (total + limit - 1) // limit

    return jsonify({
        "suppliers": paginated,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": total_pages
    })


# ✅ Test route
@suppliers_bp.route("/", methods=["GET"])
def test_suppliers():
    return jsonify({"message": "suppliers route is working"})