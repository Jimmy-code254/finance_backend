from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.dashboard_service import get_dashboard

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/summary", methods=["GET"])
@jwt_required()
def dashboard_summary():
    user_id = int(get_jwt_identity())
    dashboard_data = get_dashboard(user_id)
    return jsonify(dashboard_data)