from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, Markup
from flask_login import current_user

polls = Blueprint("polls", __name__, template_folder="templates/polls")
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

        poll_title = request.form.get("poll-title")
        if poll_title == "":
            flash("Poll title cannot be empty", "danger")
            return redirect(url_for("polls.create_poll"))

        answers = []
        answerIndex = 1
        
        while True:
            if new_answer_text := request.form.get(f'poll-answer-{answerIndex}'):
                new_answer = Answer(text = new_answer_text, order = answerIndex)
                answers.append(new_answer)
                answerIndex += 1
            else:
                break
        
        print(request.form.get('unlisted'))
        unlisted = True if request.form.get('unlisted') else False

        new_poll = Poll(user_id = int(current_user.get_id()), name = poll_title, answers = answers, is_unlisted = unlisted)

        db = current_app.config["db"]
        db.session.add(new_poll)
        db.session.commit()

        flash(Markup(f"You've successfully created your new poll! You can see it <a href='/poll/{new_poll.id}'>here</a>"), "success")
        return redirect(url_for("main.home"))


@polls.route("/poll/<poll_id>/results", methods=["GET"])
def poll_results(poll_id):
    db = current_app.config["db"]
    poll = db.session.get(Poll, poll_id)
    poll_data = poll_answers_to_tuple(poll)

    return render_template('poll_results.html', poll = poll, poll_answers = poll_data)
    

@polls.route("/poll/<poll_id>/", methods=["GET", "POST"])
def poll_vote(poll_id):
    db = current_app.config["db"]
    poll = db.session.get(Poll, poll_id)

    if current_user.is_anonymous:
        flash("You have to be logged in to vote in a poll", "warning")
        return redirect(url_for("polls.poll_results", poll_id = poll_id))

    voted_polls = current_user.voted_polls

    if poll in voted_polls:
        flash("You have already voted in this poll. Here are the results", "warning")
        return redirect(url_for("polls.poll_results", poll_id = poll_id))

    # Show poll
    if request.method == "GET":     
        redirect(url_for("polls.poll_vote", poll_id = poll_id))
        return render_template('poll.html', poll = poll, user_is_creator = True if poll in current_user.polls else False)

    
    # Vote
    if request.method == "POST":
        voted_answer_index = int(request.form.get('poll-answer'))
        voted_answer = poll.answers[voted_answer_index - 1]

        current_user.voted_answers.append(voted_answer)
        db.session.commit()

        flash("You've successfully voted in this poll! Here are the results:", 'success')
        return redirect(url_for("polls.poll_results", poll_id = poll_id))
    



def poll_answers_to_tuple(poll):
    return tuple([(answer.text, answer.number_of_votes, answer.answer_percent) for answer in poll.answers])

    


        








