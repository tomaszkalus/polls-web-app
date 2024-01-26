from flask import Blueprint, current_app, render_template, redirect, url_for
from flask_login import current_user, login_required

main = Blueprint("main", __name__)
from sqlalchemy import select

from .models import Poll


@main.route("/")
def home():
    
    return polls_page(1)

@main.route('/page/<int:page>', defaults={'page': 1})
@main.route("/page/<int:page>")
def polls_page(page: int = 1):
    """Route for displaying all polls. It also handles pagination."""
    db = current_app.config["db"]

    polls = db.paginate(db.select(Poll).where(Poll.is_unlisted == False).order_by(Poll.created), max_per_page=10, page=page, error_out=False)

    if not polls or polls.pages == 0 or page > polls.pages:
        return redirect(url_for("main.home"))

    return render_template("index.html", polls=polls)


@main.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404