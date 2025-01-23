from db import get_db

def get_all_students():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT studentID, name, points FROM students")
    rows = cursor.fetchall()

    students = [
        {
            "studentID": row[0],
            "name": row[1],
            "points": row[2]
        }
        for row in rows
    ]
    
    return students

def login_student(username, password):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students WHERE username = %s", (username,))
    user_row = cursor.fetchone()

    if user_row is None:
        return {"error": "Invalid username"}  

    cursor.execute("SELECT * FROM students WHERE username = %s AND password = %s", (username, password))
    password_row = cursor.fetchone()

    if password_row is None:
        return {"error": "Invalid password"}

    student = {
        "studentid": password_row[0],
    }

    return 
