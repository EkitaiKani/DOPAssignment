from flask import jsonify, request
from werkzeug.security import generate_password_hash
from db import get_db

def list_students():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    return jsonify(students)

def search_student_by_id(student_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE studentID = %s", (student_id,))
    student = cursor.fetchone()
    if student is None:
        return {"error": "Student not found"}, 404
    return jsonify([student])

def search_student_by_name(student_name):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE username LIKE %s", ('%' + student_name + '%',))
    students = cursor.fetchall()
    return jsonify(students)

def create_student():
    data = request.json
    student_id = data.get('studentID')
    password = generate_password_hash(data.get('password'))
    username = data.get('username')
    diploma_of_study = data.get('diplomaOfStudy')
    year_of_entry = data.get('yearOfEntry')
    email_address = data.get('emailAddress')
    points = data.get('points', 0)

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO students (studentID, password, username, diplomaOfStudy, yearOfEntry, emailAddress, points)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (student_id, password, username, diploma_of_study, year_of_entry, email_address, points))
    conn.commit()
    return {"success": True}, 201

def modify_student(student_id):
    data = request.json
    print(data)
    password = generate_password_hash(data.get('password'))
    username = data.get('username')
    diploma_of_study = data.get('diplomaOfStudy')
    year_of_entry = data.get('yearOfEntry')
    email_address = data.get('emailAddress')
    points = data.get('points')

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE students
        SET password = %s, username = %s, diplomaOfStudy = %s, yearOfEntry = %s, emailAddress = %s, points = %s
        WHERE studentID = %s
    """, (password, username, diploma_of_study, year_of_entry, email_address, points, student_id))
    conn.commit()
    return {"success": True}

def delete_student(student_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE studentID = %s", (student_id,))
    conn.commit()
    return {"success": True}