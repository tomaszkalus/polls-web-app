from flask import Blueprint, render_template, current_app, redirect, url_for
from flask_login import login_required, current_user

main = Blueprint("main", __name__)
from .models import Poll
from sqlalchemy import select


@main.route("/")
def home():
    # db = current_app.config["db"]
    # db.select()
    # polls = db.session.execute(select(Poll).order_by(Poll.created).limit(10)).all()
    # polls = db.session.query(Poll).order_by(Poll.created).limit(10).all()
    # for p in polls:
    #     print(type(p))

    # return redirect(url_for("main.polls_page", page=1), code=302)

    
    return polls_page(1)

@main.route("/page/<int:page>")
def polls_page(page: int):
    db = current_app.config["db"]
    polls = db.paginate(db.select(Poll).order_by(Poll.created))

    return render_template("index.html", polls=polls)


@main.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)
