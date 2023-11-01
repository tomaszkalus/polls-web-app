from flask import Blueprint, render_template, current_app
from flask_login import login_required, current_user

main = Blueprint("main", __name__)
from .models import Poll


@main.route("/")
def home():
    return render_template("index.html")


@main.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)
