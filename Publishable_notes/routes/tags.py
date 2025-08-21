from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_login import login_required, current_user
from models import db, Tag, Post

tags_bp = Blueprint("tags", __name__, url_prefix="/tags")

@tags_bp.route("/add/<slug>", methods=["POST"])
@login_required
def add_tag(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    # Only owner/admin can tag
    if not (current_user.is_admin or post.note.user_id == current_user.id):
        flash("You cannot tag this post.", "danger")
        return redirect(url_for("posts.detail_post", slug=slug))

    tag_name = (request.form.get("tag") or "").strip().lower()
    if not tag_name:
        flash("Tag cannot be empty.", "warning")
        return redirect(url_for("posts.detail_post", slug=slug))

    tag = Tag.query.filter_by(name=tag_name).first()
    if not tag:
        tag = Tag(name=tag_name)
        db.session.add(tag)
    if tag not in post.tags:
        post.tags.append(tag)
        db.session.commit()
        flash("Tag added.", "success")
    else:
        flash("Tag already present.", "info")
    return redirect(url_for("posts.detail_post", slug=slug))

@tags_bp.route("/remove/<slug>/<int:tag_id>", methods=["POST"])
@login_required
def remove_tag(slug, tag_id):
    post = Post.query.filter_by(slug=slug).first_or_404()
    if not (current_user.is_admin or post.note.user_id == current_user.id):
        flash("You cannot remove tags from this post.", "danger")
        return redirect(url_for("posts.detail_post", slug=slug))

    tag = Tag.query.get_or_404(tag_id)
    if tag in post.tags:
        post.tags.remove(tag)
        db.session.commit()
        flash("Tag removed.", "info")
    return redirect(url_for("posts.detail_post", slug=slug))

@tags_bp.route("/<name>")
def posts_by_tag(name):
    tag = Tag.query.filter_by(name=name.lower()).first_or_404()
    posts = tag.posts
    return render_template("posts/list.html", posts=posts, tag_filter=tag.name)
