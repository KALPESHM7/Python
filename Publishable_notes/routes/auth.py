from flask import Blueprint, render_template, request, redirect, url_for, flash # render_template-Used to render HTML templates
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from models import db, User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for("notes.list_notes"))
        flash("Invalid credentials")
    return render_template("auth/login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        confirm = request.form["confirm"]  # <-- get confirm password
        if User.query.filter_by(email=email).first():
            flash("Email already exists!")
            return redirect(url_for("auth.register"))
        if password != confirm:
            flash("Passwords do not match!")
            return redirect(url_for("auth.register"))
        new_user = User(
            email=email,
            password_hash=generate_password_hash(password),
            is_admin=False
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Account created! You can now log in.")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.", "info")
    return redirect(url_for("posts.list_posts"))
