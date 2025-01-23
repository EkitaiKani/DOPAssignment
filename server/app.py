from flask import Flask, send_from_directory, request, redirect, make_response, jsonify
from routes.student_routes import student_bp
from routes.authentication_routes import authentication_bp
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__, static_folder="../client", static_url_path="/")


app.register_blueprint(student_bp, url_prefix='/devopsassignment1/students')
app.register_blueprint(authentication_bp, url_prefix='/devopsassignment1/authentication')

@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/login")
def serve_login():
    return send_from_directory(app.static_folder, "components/login.html")

if __name__ == "__main__":
    app.run(debug=True)
