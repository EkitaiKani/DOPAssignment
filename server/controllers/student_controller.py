from db import get_db

def get_all_students():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT student_id, name, points FROM students")
    rows = cursor.fetchall()

    students = [
        {
            "student_id": row[0],
            "name": row[1],
            "points": row[2]
        }
        for row in rows
    ]
    
    return students