from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, Markup
from flask_login import current_user

polls = Blueprint("polls", __name__, template_folder="templates/polls")
from .models import User
from .models import Answer
from .models import Poll


@polls.route("/new_poll", methods=["GET", "POST"])
def create_poll():
    if request.method == "GET":
        if current_user.is_anonymous:
            flash("You have to be logged in to create a poll", "warning")
            return redirect(url_for("auth.login"))

        return render_template("create_poll.html")

    if request.method == "POST":
        answers = []
        answerIndex = 1
        while True:
            if new_answer_text := request.form.get(f'poll-answer-{answerIndex}'):
                print(new_answer_text)
                new_answer = Answer(text = new_answer_text)
                answers.append(new_answer)
                answerIndex += 1
            else:
                break
        
        new_poll = Poll(user_id = int(current_user.get_id()), name = request.form.get('poll-title'), answers = answers)

        db = current_app.config["db"]
        db.session.add(new_poll)
        db.session.commit()

        flash(Markup(f"You've successfully created your new poll!. You can see it <a href='/poll/{new_poll.id}'>here</a>"), "success")
        return redirect(url_for("main.home"))

@polls.route("/poll/<poll_id>")
def get_poll():
    




