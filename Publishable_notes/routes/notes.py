from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
import re

from models import db, Note, Post
# Here is where to do CRUD operations
notes_bp = Blueprint("notes", __name__, url_prefix="/notes")
#Slugs are used in URLs to identify posts/notes uniquely.

def slugify(text: str) -> str:
    text = (text or "").lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "post"

@notes_bp.route("/")
@login_required
def list_notes():
    show_archived = request.args.get("archived") == "1"
    q = Note.query.filter_by(user_id=current_user.id, is_archived=show_archived)
    notes = q.order_by(Note.updated_at.desc()).all()
    return render_template("notes/list.html", notes=notes, show_archived=show_archived)

@notes_bp.route("/new", methods=["POST"])
@login_required
def new_note():
    title = (request.form.get("title") or "").strip()
    body = (request.form.get("body") or "").strip()
    if not title and not body:
        flash("Note cannot be empty.", "warning")
        return redirect(url_for("notes.list_notes"))
    n = Note(title=title or "Untitled", body=body or "", user_id=current_user.id)
    db.session.add(n)
    db.session.commit()
    flash("Note created.", "success")
    return redirect(url_for("notes.list_notes"))

@notes_bp.route("/<int:note_id>/edit", methods=["GET", "POST"])
@login_required
def edit_note(note_id):
    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first_or_404()
    if request.method == "POST":
        note.title = (request.form.get("title") or "").strip() or "Untitled"
        note.body = (request.form.get("body") or "").strip()
        note.updated_at = datetime.utcnow()
        db.session.commit()
        flash("Note updated.", "success")
        return redirect(url_for("notes.list_notes"))
    return render_template("notes/edit.html", note=note)

@notes_bp.route("/<int:note_id>/delete", methods=["POST"])
@login_required
def delete_note(note_id):
    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first_or_404()
    # If note has a post, deleting note will cascade delete post due to FK uniqueness
    db.session.delete(note)
    db.session.commit()
    flash("Note deleted.", "info")
    return redirect(url_for("notes.list_notes"))

@notes_bp.route("/<int:note_id>/toggle-archive", methods=["POST"])
@login_required
def toggle_archive(note_id):
    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first_or_404()
    note.is_archived = not note.is_archived
    db.session.commit()
    flash("Note archived." if note.is_archived else "Note unarchived.", "info")
    return redirect(url_for("notes.list_notes", archived=int(note.is_archived)))

@notes_bp.route("/<int:note_id>/publish", methods=["POST"])
@login_required
def publish_note(note_id):
    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first_or_404()
    if note.post:
        flash("Already published.", "warning")
        return redirect(url_for("notes.list_notes"))

    base = note.title or (note.body[:50] if note.body else "post")
    slug = slugify(base)

    # Ensure unique slug
    unique = slug
    i = 2
    while Post.query.filter_by(slug=unique).first():
        unique = f"{slug}-{i}"
        i += 1

    post = Post(note_id=note.id, slug=unique)
    db.session.add(post)
    db.session.commit()
    flash("Published!", "success")
    return redirect(url_for("posts.detail_post", slug=post.slug))
