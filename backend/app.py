from flask import Flask, jsonify
from flask_cors import CORS

from routes.suppliers import suppliers_bp
from routes.orders import orders_bp
from routes.inventory import inventory_bp
from routes.help import help_bp  # ✅ import help blueprint

app = Flask(__name__)
CORS(app)

# Register blueprints with route prefixes
app.register_blueprint(suppliers_bp, url_prefix="/api/suppliers")
app.register_blueprint(orders_bp, url_prefix="/api/orders")
app.register_blueprint(inventory_bp, url_prefix="/api/inventory")
app.register_blueprint(help_bp, url_prefix="/api/help")  # ✅ Register here

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "This route does not exist."}), 404

if __name__ == "__main__":
    app.run(debug=True)
