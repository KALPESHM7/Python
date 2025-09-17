from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Poll, Option, Vote, db

api_bp = Blueprint("api", __name__)

@api_bp.route("/polls", methods=["GET"])
def list_polls():
    polls = Poll.query.all()
    return jsonify([{"id": p.id, "title": p.title} for p in polls])

@api_bp.route("/polls", methods=["POST"])
@jwt_required()
def create_poll():
    data = request.json
    title = data.get("title")
    options = data.get("options", [])
    if not title or len(options) < 2:
        return jsonify({"error": "Need title and at least 2 options"}), 400

    poll = Poll(title=title, owner_id=get_jwt_identity())
    db.session.add(poll)
    db.session.commit()

    for option in options:
        db.session.add(Option(text=option, poll_id=poll.id))
    db.session.commit()

    return jsonify({"message": "Poll created", "poll_id": poll.id}), 201
