from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from db import db
from models.redeemableItem_model import RedeemableItem
from models.student_model import Student  # Assuming you have a Student model

student_bp = Blueprint("student", __name__)

@student_bp.route("/student", methods=["GET"])
def student_dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    user = Student.query.filter_by(username=session["user"]).first()
    items = RedeemableItem.query.all()

    return render_template("student.html", username=user.username, points=user.points, items=items)

@student_bp.route("/redeem", methods=["POST"])
def redeem():
    if "user" not in session:
        return jsonify({"success": False, "error": "User not logged in"}), 403

    item_id = request.form.get("item_id")
    if not item_id:
        return jsonify({"success": False, "error": "No item selected"}), 400

    user = Student.query.filter_by(username=session["user"]).first()
    item = RedeemableItem.query.get(item_id)

    if item and user.points >= item.value and item.quantity > 0:
        user.points -= item.value
        item.quantity -= 1
        db.session.commit()
        session["points"] = user.points  # Update session points
        return jsonify({"success": True, "new_points": user.points})

    return jsonify({"success": False, "error": "Not enough points or item out of stock"}), 400
