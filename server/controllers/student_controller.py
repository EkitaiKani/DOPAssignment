from flask import jsonify, request
from werkzeug.security import generate_password_hash
from models.student_model import db, Student

def list_students():
    students = Student.query.all()
    return jsonify([student.to_dict() for student in students])

def search_student_by_id(student_id):
    student = Student.query.filter_by(studentid=student_id).first()
    if student is None:
        return {"error": "Student not found"}
    return jsonify([student.to_dict()])

def search_student_by_name(student_name):
    students = Student.query.filter(Student.username.like(f'%{student_name}%')).all()
    return jsonify([student.to_dict() for student in students])

def create_student():
    data = request.json
    studentid = data.get('studentid')
    password = generate_password_hash(data.get('password'))
    username = data.get('username')
    diplomaofstudy = data.get('diplomaofstudy')
    yearofentry = data.get('yearofentry')
    emailaddress = data.get('emailaddress')
    points = data.get('points', 0)

    new_student = Student(
        studentid=studentid,
        password=password,
        username=username,
        diplomaofstudy=diplomaofstudy,
        yearofentry=yearofentry,
        emailaddress=emailaddress,
        points=points
    )

    db.session.add(new_student) 
    db.session.commit()
    return {"success": True}

def handle_password(password):
    if password.startswith('scrypt'):
        return password
    return generate_password_hash(password)

def modify_student(student_id):
    data = request.json
    student = Student.query.filter_by(studentid=student_id).first() 

    if student is None:
        return {"error": "Student not found"}

    student.password = handle_password(data.get('password'))
    student.username = data.get('username')
    student.diplomaofstudy = data.get('diplomaofstudy')
    student.yearofentry = data.get('yearofentry')
    student.emailaddress = data.get('emailaddress')
    student.points = data.get('points')

    db.session.commit()
    return {"success": True}

def delete_student(student_id):
    student = Student.query.filter_by(studentid=student_id).first()

    if student is None:
        return {"error": "Student not found"}, 404

    db.session.delete(student)
    db.session.commit()
    return {"success": True}
