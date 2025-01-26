from flask import Blueprint, request
from controllers.student_controller import list_students, search_student_by_id, search_student_by_name, create_student, modify_student, delete_student

student_bp = Blueprint('student_bp', __name__)

@student_bp.route("/", methods=["GET"])
def list_all_students():
    return list_students()

@student_bp.route("/<student_id>", methods=["GET"])
def get_student_by_id(student_id):
    return search_student_by_id(student_id)

@student_bp.route("/search", methods=["GET"])
def get_student_by_name():
    identifier = request.args.get('identifier')
    if len(identifier) == 9 and any(char.isdigit() for char in identifier):
        return search_student_by_id(identifier)
    else:
        return search_student_by_name(identifier)

@student_bp.route("/add_student", methods=["POST"])
def add_student():
    return create_student()

@student_bp.route("/<student_id>", methods=["PUT"])
def update_student(student_id):
    return modify_student(student_id)

@student_bp.route("/<student_id>", methods=["DELETE"])
def remove_student(student_id):
    return delete_student(student_id)