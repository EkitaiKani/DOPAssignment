from flask import Blueprint, request, jsonify
from controllers.user_controller import get_users, add_user

user_bp = Blueprint('user_routes', __name__)

@user_bp.route("/", methods=["GET"])
def fetch_users():
    users = get_users()
    return jsonify(users)

@user_bp.route("/", methods=["POST"])
def create_user():
    data = request.json
    add_user(data)
    return jsonify({"message": "User added successfully!"}), 201
