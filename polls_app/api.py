import csv
import io
from .models import Poll
from flask import Blueprint, current_app, Response, render_template_string
from flask_login import current_user
from .utils import decode_url_identifier, poll_name_to_filename

api = Blueprint("api", __name__)

@api.route("/api/<string:hashed_poll_id>/results", methods=["GET"])
def poll_results(hashed_poll_id: str):
    """Returns the poll results in a format that can be used by the chart.js library"""
    poll_id = decode_url_identifier(hashed_poll_id)
    db = current_app.config["db"]

    poll = db.session.get(Poll, poll_id)
    return [
        (answer.text, answer.number_of_votes, answer.answer_percent)
        for answer in poll.answers
    ]


@api.route("/api/<string:hashed_poll_id>/csv", methods=["GET"])
def poll_csv(hashed_poll_id: str):
    """Returns a CSV file with the poll results"""
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


@api.route("/api/<string:hashed_poll_id>/edit", methods=["GET"])
def get_poll_edit_modal(hashed_poll_id: str):
    """Returns the poll edit modal"""
    poll_id = decode_url_identifier(hashed_poll_id)
    db = current_app.config["db"]
    poll = db.session.get(Poll, poll_id)

    edit_modal = render_template_string(
        "{% import 'macros/edit_poll_modal.html' as edit_macro %}"
        "{{ edit_macro.render_edit_modal(poll) }}",
        poll=poll,
    )

    return edit_modal


@api.route("/api/<string:hashed_poll_id>/delete", methods=["GET"])
def get_poll_delete_modal(hashed_poll_id: str):
    """Returns the poll delete modal"""

    if current_user.is_anonymous:
        return "You need to be logged in to delete a poll", 403

    poll_id = decode_url_identifier(hashed_poll_id)
    db = current_app.config["db"]
    poll = db.session.get(Poll, poll_id)

    delete_modal = render_template_string(
        "{% import 'macros/delete_poll_modal.html' as delete_macro %}"
        "{{ delete_macro.render_delete_modal(poll) }}",
        poll=poll,
    )

    return delete_modal
