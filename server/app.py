from flask import Flask, send_from_directory, request, redirect, make_response, jsonify, session, render_template
from routes.student_routes import student_bp
from routes.authentication_routes import authentication_bp
from config import DevelopmentConfig, ProductionConfig
from db import init_db, db
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__, static_folder="../client/static", template_folder="../client/templates")
app.secret_key = os.urandom(24)
app.config.from_object(ProductionConfig)
init_db(app)

users = {}

app.register_blueprint(student_bp, url_prefix='/devopsassignment1/students')
app.register_blueprint(authentication_bp, url_prefix='/devopsassignment1/authentication')

@app.route("/")
def serve_index():
    if 'userID' in session:
        return render_template("index.html")
    return redirect("/login")

@app.route("/login")
def serve_login():
    return render_template("login.html")

@app.route("/recover-password")
def serve_recover_password():
    return render_template("recover-password.html")

@app.route("/admin")
def serve_admin():
    if 'userID' in session:
        return render_template("admin.html")
    return redirect("/login")

@app.route("/editStudent")
def serve_editStudent():
    if 'userID' in session:
        return render_template("editStudent.html")
    return redirect("/login")

@app.route("/createStudent")
def server_createStudent():
    if 'userID' in session:
        return render_template("createStudent.html")
    return redirect("/login")

@app.route("/student")
def serve_student():
    if 'userID' in session:
        return render_template("student.html")
    return redirect("/login")

@app.route("/logout")
def logout():
    session.pop("userID", None)
    return redirect("/login")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=(DevelopmentConfig != ProductionConfig))
