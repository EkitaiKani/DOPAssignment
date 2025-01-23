from flask import Blueprint, jsonify, request
from controllers.authentication_controller import login_user

authentication_bp = Blueprint('authentication_bp', __name__)

@authentication_bp.route("/login", methods=["POST"])
def login():
    loginData = login_user(request.json["username"], request.json["password"])
    return jsonify(loginData)

