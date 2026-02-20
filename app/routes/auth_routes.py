from flask import Blueprint, request, jsonify
from app.services.auth_service import register_user, login_user
from app.extensions import mysql
from flask_jwt_extended import jwt_required, get_jwt_identity

auth_bp = Blueprint("auth", __name__)

# Test route
@auth_bp.route("/test", methods=["GET"])
def test():
    return jsonify({"message": "Auth blueprint loaded"})

# DB connection test route
@auth_bp.route("/db-test", methods=["GET"])
def db_test():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT 1")
        cur.close()
        return {"status": "Database connection OK"}
    except Exception as e:
        return {"status": "Database connection FAILED", "error": str(e)}, 500

# User registration
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    response, status_code = register_user(username, email, password)
    return jsonify(response), status_code

# User login
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    response, status_code = login_user(email, password)
    return jsonify(response), status_code

# Protected dashboard test
@auth_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def dashboard():
    user_id = int(get_jwt_identity())  # convert string back to int for DB queries
    return {"message": f"Hello user {user_id}, welcome to your dashboard!"}