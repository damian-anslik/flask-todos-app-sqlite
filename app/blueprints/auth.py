from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from ..models import User, ConfirmationEmail
from .. import db, mail, sender

auth = Blueprint("auth", __name__, template_folder="templates")


@auth.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    return render_template("login.html")


@auth.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        flash("Please check your login details and try again.", "danger")
        return redirect(url_for("auth.login"))
    login_user(user, remember=remember)
    return redirect(url_for("main.home"))


@auth.route("/signup")
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    return render_template("signup.html")


@auth.route("/signup", methods=["POST"])
def signup_post():
    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")
    user = User.query.filter((User.name == name) | (User.email == email)).first()
    if user:
        flash("User already exists", "danger")
        return redirect(url_for("auth.signup"))
    new_user = User(
        email=email,
        name=name,
        password_hash=generate_password_hash(password, method="sha256"),
    )
    db.session.add(new_user)
    db.session.commit()
    send_confirmation_email(email=email)
    login_user(user=new_user)
    flash(
        "You have successfully registered. Please check your email to confirm your account.",
        "success"
    )
    return redirect(url_for("main.home"))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@auth.route("/confirm/<token>")
def confirm_email(token: str):
    confirmation_email = ConfirmationEmail.query.filter_by(token=token).first()
    if not confirmation_email:
        flash("Invalid confirmation token", "danger")
        return redirect(url_for("main.home"))
    if confirmation_email.expiry_date < datetime.now():
        flash("Confirmation token expired", "danger")
        return redirect(url_for("main.home"))
    user = User.query.filter_by(email=confirmation_email.email).first()
    user.is_confirmed = True
    db.session.delete(confirmation_email)
    db.session.commit()
    login_user(user)
    return redirect(url_for("main.home"))


@auth.route("/update", methods=["POST"])
@login_required
def update():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    new_password = request.form.get("new_password")
    confirm_new_password = request.form.get("confirm_new_password")

    if not name or not email or not password:
        flash("Please fill out all fields", "danger")
        return redirect(url_for("main.settings"))
    if check_password_hash(current_user.password_hash, password) is False:
        flash("Incorrect password", "danger")
        return redirect(url_for("main.settings"))
    if new_password and confirm_new_password:
        if new_password == confirm_new_password:
            current_user.password_hash = generate_password_hash(
                new_password, method="sha256"
            )
            db.session.commit()
            flash("Password updated", "success")
        else:
            flash("New passwords do not match", "danger")
    else:
        # Check if a user or email is already taken
        user = User.query.filter((User.name == name) | (User.email == email)).first()
        if user != current_user:
            flash("User already exists", "danger")
            return redirect(url_for("main.settings"))
        current_user.name = name
        current_user.email = email
        db.session.commit()
        flash("Profile updated", "success")
    return redirect(url_for("main.settings"))

    
@auth.route("/resend_confirmation", methods=["POST"])
@login_required
def resend_confirmation():
    if current_user.is_confirmed:
        return redirect(url_for("main.home"))
    send_confirmation_email(email=current_user.email)
    flash("Confirmation email sent", "success")
    return redirect(url_for("main.home"))


def send_confirmation_email(email: str):
    """Send a confirmation email to the new user"""
    confirmation_email = ConfirmationEmail(email=email)
    db.session.add(confirmation_email)
    db.session.commit()

    msg = Message(
        "Confirm your email",
        sender=sender,
        recipients=[email],
        html=render_template("confirm_email.html", token=confirmation_email.token),
    )
    mail.send(msg)
