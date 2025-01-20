from flask import Blueprint, jsonify, request
from controllers.student_controller import get_all_students, login_student

student_bp = Blueprint('student_bp', __name__)

@student_bp.route("/", methods=["GET"])
def list_students():
    students = get_all_students()
    return jsonify(students)

@student_bp.route("/login", methods=["POST"])
def login():
    student = login_student(request.json["student_id"])
    return jsonify(student)


