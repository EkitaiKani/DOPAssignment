from flask import Flask, send_from_directory
from routes.user_routes import user_bp
from db import init_db
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__, static_folder="../client", static_url_path="/")

app.register_blueprint(user_bp, url_prefix='/devopsassignment1/users')

@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/login")
def serve_login():
    return send_from_directory(app.static_folder, "components/login.html")

init_db(app)

if __name__ == "__main__":
    app.run(debug=True)