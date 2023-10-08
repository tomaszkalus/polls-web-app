from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    current_app,
    flash,
)
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from flask_login import login_user, login_required, logout_user, login_manager

auth = Blueprint("auth", __name__, template_folder="templates/auth")

app = current_app


@auth.route("/login/")
def login():
    return render_template("login.html")


@auth.route("/login/", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")

    remember = True if request.form.get("remember") else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash("Please check your login details and try again.", "danger")
        return redirect(url_for("auth.login"))

    login_user(user, remember=remember)
    flash("You are successfully logged in.", "success")
    return redirect(url_for("main.profile"))


@auth.route("/register/")
def register():
    return render_template("register.html")


@auth.route("/register/", methods=["POST"])
def register_post():
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if user:
        flash("Email address already exists")
        return redirect(url_for("auth.register"))

    new_user = User(
        email=email,
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
    logout_user()
    flash("You were successfully logged out", "success")
    return redirect(url_for("main.home"))
