from db import get_db

def get_users():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    return [{"id": row[0], "name": row[1]} for row in users]

def add_user(data):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name) VALUES (%s)", (data["name"],))
    conn.commit()
    cursor.close()
