from werkzeug.security import generate_password_hash, check_password_hash
from models.student_model import db, Student
from models.admin_model import Admin

def get_user_data(username):
    user = Student.query.filter_by(username=username).first()
    if user:
        return user.to_dict(), 'student'

    user = Admin.query.filter_by(username=username).first()
    if user:
        return user.to_dict(), 'admin'

    return None, None

def login_user(username, password):
    user_data, role = get_user_data(username)
    if user_data is None:
        return {"error": "Invalid username"}

    stored_password = user_data['password']
    if not check_password_hash(stored_password, password):
        return {"error": "Invalid password"}

    return {"userID": user_data[role+"id"], "role": role}

def recoverPassword(username, new_password):
    user_data = get_user_data(username)

    if user_data is None:
        return {"error": "Invalid username"}

    role = user_data['role']
    userID = user_data['id']

    if role == 'student':
        user = Student.query.filter_by(studentid=userID).first()
    elif role == 'admin':
        user = Admin.query.filter_by(adminid=userID).first()

    if user is None:
        return {"error": "User not found"}

    # Update the user's password
    user.password = generate_password_hash(new_password)
    db.session.commit()

    return {"success": True}
