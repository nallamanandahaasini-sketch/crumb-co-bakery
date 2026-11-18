from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import User
from extensions import db
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        name, email = request.form.get("name","").strip(), request.form.get("email","").strip().lower()
        password = request.form.get("password","")
        if not name or not email or len(password) < 8:
            flash("Enter your name, a valid email and a password with at least 8 characters.", "warning")
        elif User.query.filter_by(email=email).first():
            flash("An account with that email already exists.", "warning")
        else:
            user = User(name=name, email=email, phone=request.form.get("phone"), role="customer")
            user.set_password(password); db.session.add(user); db.session.commit()
            session["user_id"] = user.id
            flash("Welcome! Your account has been created.", "success")
            return redirect(url_for("home"))
    return render_template("auth.html", mode="register")

@auth_bp.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form.get("email","").lower()).first()
        if user and user.check_password(request.form.get("password","")):
            session["user_id"] = user.id
            flash("You are now signed in.", "success")
            return redirect(url_for("admin.dashboard") if user.role != "customer" else url_for("home"))
        flash("Email or password is incorrect.", "danger")
    return render_template("auth.html", mode="login")

@auth_bp.route("/logout")
def logout():
    session.clear(); flash("You have been signed out.", "info")
    return redirect(url_for("home"))
