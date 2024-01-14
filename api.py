from flask import (Blueprint, current_app)

api = Blueprint("api", __name__)
from .models import Poll

@api.route("/api/<poll_id>/results", methods=["GET"])
def poll_results(poll_id):
    db = current_app.config["db"]
    poll = db.session.get(Poll, poll_id)
    return [(answer.text, answer.number_of_votes, answer.answer_percent) for answer in poll.answers]