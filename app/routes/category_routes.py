from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.category_service import add_category, get_categories

category_bp = Blueprint("category", __name__)

# Add a new category
@category_bp.route("/add", methods=["POST"])
@jwt_required()
def add_cat():
    user_id = int(get_jwt_identity())  # convert string back to int
    data = request.get_json()
    name = data.get("name")
    c_type = data.get("type")  # 'income' or 'expense'

    if not name or not c_type:
        return jsonify({"error": "Name and type are required"}), 400

    response, status_code = add_category(user_id, name, c_type)
    return jsonify(response), status_code

# Get all categories for the logged-in user
@category_bp.route("/all", methods=["GET"])
@jwt_required()
def all_categories():
    user_id = int(get_jwt_identity())
    categories = get_categories(user_id)
    return jsonify(categories)