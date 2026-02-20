from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.budget_service import add_budget, get_budget_progress

budget_bp = Blueprint("budget", __name__)


# =====================
# Add or Update Budget
# =====================
@budget_bp.route("/add", methods=["POST"])
@jwt_required()
def add_budget_route():
    user_id = int(get_jwt_identity())
    data = request.get_json()

    category_id = data.get("category_id")
    amount = data.get("amount")
    month = data.get("month")  # format: YYYY-MM-01

    if not category_id or not amount or not month:
        return jsonify({"error": "All fields are required"}), 400

    response, status_code = add_budget(user_id, category_id, amount, month)
    return jsonify(response), status_code


# =====================
# Get Budget Progress
# =====================
@budget_bp.route("/progress", methods=["GET"])
@jwt_required()
def budget_progress():
    user_id = int(get_jwt_identity())
    month = request.args.get("month")

    if not month:
        return jsonify({"error": "Month is required"}), 400

    results = get_budget_progress(user_id, month)
    return jsonify(results)