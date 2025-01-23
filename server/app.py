from flask import Flask, send_from_directory, request, redirect, make_response, jsonify, session
from routes.student_routes import student_bp
from routes.authentication_routes import authentication_bp
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__, static_folder="../client", static_url_path="/login")
app.secret_key = os.urandom(24)

users = {}

app.register_blueprint(student_bp, url_prefix='/devopsassignment1/students')
app.register_blueprint(authentication_bp, url_prefix='/devopsassignment1/authentication')

@app.route("/")
def serve_index():
    if 'userID' in session:
        return send_from_directory(app.static_folder, "index.html")
    return redirect("/login")

@app.route("/login")
def serve_login():
    return send_from_directory(app.static_folder, "components/login.html")

@app.route("/admin")
def serve_admin():
    if 'userID' in session:
        return send_from_directory(app.static_folder, "components/admin.html")
    return redirect("/login")

@app.route("/student")
def serve_student():
    if 'userID' in session:
        return send_from_directory(app.static_folder, "components/student.html")
    return redirect("/login")

@app.route("/logout")
def logout():
    session.pop("userID", None)
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)
