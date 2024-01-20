""" This module contains all the routes related to polls. """

from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    current_app,
    Markup,
)
from flask_login import current_user

polls = Blueprint("polls", __name__, template_folder="templates/polls")
from .models import Answer
from .models import Poll


@polls.route("/new_poll", methods=["GET", "POST"])
def create_poll():
    """Route for creating a new poll. It only lets logged to create a poll."""
    if request.method == "GET":
        if current_user.is_anonymous:
            flash("You have to be logged in to create a poll", "warning")
            return redirect(url_for("auth.login"))

        return render_template("create_poll.html")

    if request.method == "POST":
        poll_title = request.form.get("poll-title")
        if poll_title == "":
            flash("Poll title cannot be empty", "danger")
            return redirect(url_for("polls.create_poll"))

        answers = []
        answerIndex = 1

        while True:
            if new_answer_text := request.form.get(f"poll-answer-{answerIndex}"):
                new_answer = Answer(text=new_answer_text, order=answerIndex)
                answers.append(new_answer)
                answerIndex += 1
            else:
                break

        unlisted = True if request.form.get("unlisted") else False

        new_poll = Poll(
            user_id=int(current_user.get_id()),
            name=poll_title,
            answers=answers,
            is_unlisted=unlisted,
        )

        db = current_app.config["db"]
        db.session.add(new_poll)
        db.session.commit()

        flash(
            "You've successfully created your new poll!",
            "success",
        )
        return redirect(url_for("polls.poll_results", poll_id=new_poll.id))


@polls.route("/poll/<poll_id>/results", methods=["GET"])
def poll_results(poll_id):
    """Route for displaying the results of a poll."""
    db = current_app.config["db"]
    poll = db.session.get(Poll, poll_id)
    if not poll:
        flash("This poll does not exist", "warning")
        return redirect(url_for("main.home"))

    poll_data = poll.graph_data
    return render_template("poll_results.html", poll=poll, poll_answers=poll_data)


@polls.route("/poll/<poll_id>/", methods=["GET", "POST"])
def poll_vote(poll_id):
    """Route for voting in a poll."""
    db = current_app.config["db"]
    poll = db.session.get(Poll, poll_id)

    if current_user.is_anonymous:
        return redirect(url_for("polls.poll_results", poll_id=poll_id))

    if poll in current_user.voted_polls:
        return redirect(url_for("polls.poll_results", poll_id=poll_id))

    if request.method == "GET":
        redirect(url_for("polls.poll_vote", poll_id=poll_id))
        return render_template(
            "poll.html",
            poll=poll,
            user_is_creator=True if poll in current_user.polls else False,
        )

    if request.method == "POST":
        voted_answer_index = int(request.form.get("poll-answer"))
        voted_answer = poll.answers[voted_answer_index - 1]

        current_user.voted_answers.append(voted_answer)
        db.session.commit()

        flash(
            "You've successfully voted in this poll! Here are the results:", "success"
        )
        return redirect(url_for("polls.poll_results", poll_id=poll_id))


@polls.route("/your_polls/", methods=["GET"])
def user_created_polls():
    """Route for displaying all the polls that the user has created."""
    if current_user.is_anonymous:
        flash("You have to be logged in to view your polls", "warning")
        return redirect(url_for("auth.login"))

    if not current_user.polls:
        flash("You haven't created any polls yet", "warning")
        return redirect(url_for("auth.profile"))

    return render_template("all_user_created_polls.html", polls=current_user.polls)


@polls.route("/delete_poll/<poll_id>", methods=["POST"])
def delete_poll(poll_id):
    """Route for deleting a poll."""
    if current_user.is_anonymous:
        flash("You have to be logged in to delete a poll", "warning")
        return redirect(url_for("auth.login"))

    poll_id = int(poll_id)

    db = current_app.config["db"]
    poll = db.session.get(Poll, poll_id)

    if poll not in current_user.polls:
        flash("You can't delete a poll that you haven't created", "danger")
        return redirect(url_for("main.profile"))

    db.session.delete(poll)
    db.session.commit()

    print(f"Deleted poll with id {poll_id}")

    flash("You've successfully deleted the poll", "success")
    return redirect(url_for("main.profile"))


@polls.route("/poll/<poll_id>/edit", methods=["POST"])
def edit_poll(poll_id):
    """Route for editing a poll."""
    if current_user.is_anonymous:
        flash("You have to be logged in to edit a poll", "warning")
        return redirect(url_for("auth.login"))

    db = current_app.config["db"]
    poll = db.session.get(Poll, poll_id)

    if poll not in current_user.polls:
        flash("You can't edit a poll that you haven't created", "danger")
        return redirect(url_for("main.profile"))

    unlisted = True if request.form.get("poll-visibility") == "unlisted" else False
    poll.is_unlisted = unlisted
    db.session.commit()

    flash(
        "You've successfully edited your poll!",
        "success",
    )
    return redirect(url_for("polls.poll_results", poll_id=poll.id))
