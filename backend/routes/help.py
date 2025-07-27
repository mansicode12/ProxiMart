# routes/help.py
from flask import Blueprint, jsonify

help_bp = Blueprint("help", __name__)

@help_bp.route("/faqs", methods=["GET"])
def get_faqs():
    faqs = [
        {"question": "How do I register as a supplier?", "answer": "Use /api/suppliers/add"},
        {"question": "How do I place an order?", "answer": "Use /api/orders/place with buyer_name, items, etc."},
        {"question": "How are nearby suppliers found?", "answer": "Based on item match and location within radius."},
    ]
    return jsonify({"faqs": faqs})
