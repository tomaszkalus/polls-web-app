""" This module contains the routes for the authentication blueprint. """

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from .models import User
from .validation import validate_password

from .config import TEST_USERNAME, TEST_PASSWORD

auth = Blueprint("auth", __name__, template_folder="templates/auth")
app = current_app


@auth.route("/login/")
def login():
    """Renders the login page"""
    return render_template("login.html")


@auth.route("/login/", methods=["POST"])
def login_post():
    """Login handler"""
    username = request.form.get("username")
    password = request.form.get("password")

    remember = True if request.form.get("remember") else False

    if request.form.get("guest"):
        username = TEST_USERNAME
        password = TEST_PASSWORD
    
    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        flash("Please check your login details and try again.", "danger")
        return redirect(url_for("auth.login"))

    login_user(user, remember=remember)
    flash("You are successfully logged in.", "success")
    return redirect(url_for("main.profile"))

@auth.route('/login_guest', methods=["POST"])
def login_guest():
    """ Login handler for guest user. """

    username = TEST_USERNAME
    password = TEST_PASSWORD

    remember = True if request.form.get("remember") else False

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        flash("The guest account is not working. Please try again later or create an account.", "danger")
        return redirect(url_for("auth.login"))

    login_user(user, remember=remember)
    flash("You are successfully logged in as a guest.", "success")
    return redirect(url_for("main.index"))


@auth.route("/register/")
def register():
    """Renders the register page"""
    return render_template("register.html")


@auth.route("/register/", methods=["POST"])
def register_post():
    """Register handler"""
    username, password = request.form.get("username"), request.form.get("password")
    confirm_password = request.form.get("confirm_password")

    password_validation = validate_password(password, confirm_password)

    if not password_validation.is_valid:
        flash(password_validation.message, "danger")
        return render_template("register.html", username=username)

    user = User.query.filter_by(username=username).first()

    if user:
        flash(
            "A user with this username already exists, please choose a different one.",
            "danger",
        )
        return redirect(url_for("auth.register"))

    new_user = User(
        username=username,
        password=generate_password_hash(password, method="sha256"),
    )

    db = app.config["db"]
    db.session.add(new_user)
    db.session.commit()

    flash("You were successfully registered in", "success")
    return redirect(url_for("auth.login"))


@auth.route("/logout/")
@login_required
def logout():
    """Logout handler"""
    logout_user()
    flash("You were successfully logged out", "success")
    return redirect(url_for("main.home"))


@auth.route("/delete_account/", methods=["GET", "POST"])
@login_required
def delete_account():
    """Route responsible for deleting the user's account"""
    if request.method == "GET":
        return render_template("delete_account.html")

    if request.method == "POST":
        password = request.form.get("password")

        user = User.query.filter_by(id=current_user.id).first()

        if not check_password_hash(user.password, password):
            flash("The password you've provided is incorrect.", "danger")
            return redirect(url_for("auth.delete_account"))

        db = app.config["db"]
        db.session.delete(user)
        db.session.commit()

        flash("Your account was successfully deleted", "success")
        return redirect(url_for("main.home"))


@auth.route("/change_password/", methods=["GET", "POST"])
@login_required
def change_password():
    """Route responsible for changing the user's password"""
    if request.method == "GET":
        return render_template("change_password.html")

    if request.method == "POST":
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_new_password")

        user = User.query.filter_by(id=current_user.id).first()

        if not check_password_hash(user.password, old_password):
            flash("The password you've provided is incorrect.", "danger")
            return redirect(url_for("auth.change_password"))

        password_validation = validate_password(new_password, confirm_password)
        if not password_validation.is_valid:
            flash(password_validation.message, "danger")
            return redirect(url_for("auth.change_password"))

        user.password = generate_password_hash(new_password, method="sha256")
        db = app.config["db"]
        db.session.commit()

        flash("Your password was successfully changed", "success")
        return redirect(location=url_for("main.profile"))
