from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.transaction_service import (
    add_transaction,
    get_transactions,
    delete_transaction,
    filter_transactions
)

from app.services.category_service import (
    add_category,
    get_categories
)

transaction_bp = Blueprint("transaction", __name__)

# ============================
# Add Transaction (supports recurring)
# ============================
@transaction_bp.route("/add", methods=["POST"])
@jwt_required()
def add_transaction_route():
    user_id = int(get_jwt_identity())
    data = request.get_json()

    amount = data.get("amount")
    description = data.get("description", "")
    category_id = data.get("category_id")
    date = data.get("date")
    recurring_type = data.get("recurring_type")  # optional

    if not amount or not category_id:
        return jsonify({"error": "Amount and category are required"}), 400

    response, status_code = add_transaction(
        user_id,
        category_id,
        amount,
        description,
        date,
        recurring_type
    )

    return jsonify(response), status_code


# ============================
# Get All Transactions
# ============================
@transaction_bp.route("/all", methods=["GET"])
@jwt_required()
def all_transactions():
    user_id = int(get_jwt_identity())
    transactions = get_transactions(user_id)
    return jsonify(transactions)


# ============================
# Delete Transaction
# ============================
@transaction_bp.route("/delete/<int:transaction_id>", methods=["DELETE"])
@jwt_required()
def delete_transaction_route(transaction_id):
    user_id = int(get_jwt_identity())
    response, status_code = delete_transaction(transaction_id, user_id)
    return jsonify(response), status_code


# ============================
# Filter Transactions
# ============================
@transaction_bp.route("/filter", methods=["GET"])
@jwt_required()
def filter_route():
    user_id = int(get_jwt_identity())

    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    category_id = request.args.get("category_id", type=int)
    min_amount = request.args.get("min_amount", type=float)
    max_amount = request.args.get("max_amount", type=float)

    transactions = filter_transactions(
        user_id,
        start_date,
        end_date,
        category_id,
        min_amount,
        max_amount
    )

    return jsonify(transactions)


# ============================
# Add Category
# ============================
@transaction_bp.route("/category/add", methods=["POST"])
@jwt_required()
def add_category_route():
    user_id = int(get_jwt_identity())
    data = request.get_json()

    name = data.get("name")
    c_type = data.get("type")

    if not name or not c_type:
        return jsonify({"error": "Name and type are required"}), 400

    response, status_code = add_category(user_id, name, c_type)
    return jsonify(response), status_code


# ============================
# Get Categories
# ============================
@transaction_bp.route("/categories", methods=["GET"])
@jwt_required()
def categories():
    user_id = int(get_jwt_identity())
    categories = get_categories(user_id)
    return jsonify(categories)