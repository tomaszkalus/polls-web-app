from flask import Blueprint, current_app, Response

api = Blueprint("api", __name__)
from .models import Poll
from .utils import decode_url_identifier, poll_name_to_filename
import csv
import io


@api.route("/api/<string:hashed_poll_id>/results", methods=["GET"])
def poll_results(hashed_poll_id: str):
    poll_id = decode_url_identifier(hashed_poll_id)
    db = current_app.config["db"]

    poll = db.session.get(Poll, poll_id)
    return [
        (answer.text, answer.number_of_votes, answer.answer_percent)
        for answer in poll.answers
    ]


@api.route("/api/<string:hashed_poll_id>/csv", methods=["GET"])
def poll_csv(hashed_poll_id: str):
    poll_id = decode_url_identifier(hashed_poll_id)
    db = current_app.config["db"]
    poll = db.session.get(Poll, poll_id)

    if not poll:
        return "Poll not found", 404

    poll_questions = [answer.text for answer in poll.answers]
    poll_votes = [answer.number_of_votes for answer in poll.answers]

    stream = io.StringIO()
    writer = csv.writer(stream, delimiter=";")

    writer.writerow(poll_questions)
    writer.writerow(poll_votes)

    csv_content = stream.getvalue()
    stream.close()

    file_name = poll_name_to_filename(poll.name)

    return Response(
        csv_content,
        mimetype="text/csv",
        headers={"Content-disposition": f"attachment; filename={file_name}.csv"},
    )
