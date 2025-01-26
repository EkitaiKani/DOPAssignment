from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db

def login_user(username, password):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 'student' AS role, studentID AS id, username, password FROM students WHERE username = %s
        UNION
        SELECT 'admin' AS role, adminID AS id, username, password FROM admins WHERE username = %s
    """, (username, username))

    user_row = cursor.fetchone()

    if user_row is None:
        return {"error": "Invalid username"}

    role, userID, stored_username, stored_password = user_row
    if not check_password_hash(stored_password, password):
        return {"error": "Invalid password"}

    return {"userID": userID, "role": role}

def recoverPassword(username, password):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 'student' AS role, studentID AS id, username, password FROM students WHERE username = %s
        UNION
        SELECT 'admin' AS role, adminID AS id, username, password FROM admins WHERE username = %s
    """, (username, username))

    user_row = cursor.fetchone()

    if user_row is None:
        return {"error": "Invalid username"}

    role, userID, stored_username, stored_password = user_row

    cursor.execute("""
        UPDATE {}s SET password = %s WHERE {}ID = %s
    """.format(role, role), (generate_password_hash(password), userID))

    conn.commit()
    return {"success": True}

