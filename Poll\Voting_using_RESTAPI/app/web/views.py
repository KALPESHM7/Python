from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
from flask_login import login_required, current_user
from app.models import Poll, Option, Vote, db

web_bp = Blueprint("web", __name__)

@web_bp.route("/")
def index():
    """Show all polls on home page"""
    polls = Poll.query.order_by(Poll.created_at.desc()).all()
    return render_template("index.html", polls=polls)

@web_bp.route("/polls/create", methods=["GET", "POST"])
@login_required
def create_poll():
    """Allow logged-in user to create a new poll"""
    if request.method == "POST":
        title = request.form["title"]
        options = request.form.getlist("options")

        if not title or len([o for o in options if o.strip()]) < 2:
            flash("Please provide a question and at least two valid options.", "danger")
            return redirect(url_for("web.create_poll"))

        poll = Poll(title=title, owner_id=current_user.id)
        db.session.add(poll)
        db.session.flush()  # flush to get poll.id

        for option in options:
            if option.strip():
                db.session.add(Option(text=option.strip(), poll_id=poll.id))

        db.session.commit()
        flash("Poll created successfully!", "success")
        return redirect(url_for("web.index"))

    return render_template("create_poll.html")

@web_bp.route("/polls/<int:poll_id>", methods=["GET", "POST"])
def poll_public(poll_id):
    """Public page for voting on a poll and viewing results"""
    poll = Poll.query.get_or_404(poll_id)

    # Prevent double voting using cookies
    has_voted = request.cookies.get(f"poll_{poll.id}_voted")

    if request.method == "POST":
        if has_voted:
            flash("You have already voted on this poll.", "warning")
            return redirect(url_for("web.poll_public", poll_id=poll.id))

        option_id = request.form.get("option_id")
        option = Option.query.filter_by(id=option_id, poll_id=poll.id).first()
        if option:
            option.votes += 1
            db.session.add(Vote(option_id=option.id))
            db.session.commit()

            flash("Thanks for voting!", "success")
            resp = make_response(redirect(url_for("web.poll_public", poll_id=poll.id)))
            resp.set_cookie(f"poll_{poll.id}_voted", "1", max_age=60*60*24*365)  # 1 year
            return resp
        else:
            flash("Invalid option selected.", "danger")
            return redirect(url_for("web.poll_public", poll_id=poll.id))

    return render_template("poll_public.html", poll=poll, has_voted=bool(has_voted))

@web_bp.route("/polls/<int:poll_id>/delete", methods=["POST"])
@login_required
def delete_poll(poll_id):
    """Allow poll owner to delete their poll"""
    poll = Poll.query.get_or_404(poll_id)

    if poll.owner_id != current_user.id:
        flash("You are not allowed to delete this poll.", "danger")
        return redirect(url_for("web.poll_public", poll_id=poll.id))

    # Delete all options & votes
    for option in poll.options:
        Vote.query.filter_by(option_id=option.id).delete()
        db.session.delete(option)

    db.session.delete(poll)
    db.session.commit()

    flash("Poll deleted successfully.", "success")
    return redirect(url_for("web.index"))
