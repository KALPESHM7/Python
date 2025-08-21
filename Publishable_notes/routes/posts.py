from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Post, Note, Comment, Tag

posts_bp = Blueprint("posts", __name__, url_prefix="/posts")

@posts_bp.route("/")
def list_posts():
    posts = Post.query.order_by(Post.published_at.desc()).all()
    return render_template("posts/list.html", posts=posts)

@posts_bp.route("/<slug>")
def detail_post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    return render_template("posts/detail.html", post=post, edit_mode=False)

# Edit the underlying Note (title/body) from the post page
@posts_bp.route("/<slug>/edit", methods=["GET", "POST"])
@login_required
def edit_post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    note = post.note
    # Only the author (owner of note) or admin can edit
    if not (current_user.is_admin or note.user_id == current_user.id):
        flash("You cannot edit this post.", "danger")
        return redirect(url_for("posts.detail_post", slug=slug))

    if request.method == "POST":
        note.title = (request.form.get("title") or "").strip() or "Untitled"
        note.body = (request.form.get("body") or "").strip()
        db.session.commit()
        flash("Post updated (and note synced).", "success")
        return redirect(url_for("posts.detail_post", slug=slug))

    return render_template("posts/detail.html", post=post, edit_mode=True)

@posts_bp.route("/<slug>/unpublish", methods=["POST"])
@login_required
def unpublish(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    note = post.note
    if not (current_user.is_admin or note.user_id == current_user.id):
        flash("You cannot unpublish this post.", "danger")
        return redirect(url_for("posts.detail_post", slug=slug))
    db.session.delete(post)
    db.session.commit()
    flash("Unpublished. Note kept privately.", "info")
    return redirect(url_for("notes.list_notes"))

@posts_bp.route("/<slug>/feature", methods=["POST"])
@login_required
def toggle_feature(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    note = post.note
    if not (current_user.is_admin or note.user_id == current_user.id):
        flash("You cannot feature this post.", "danger")
        return redirect(url_for("posts.detail_post", slug=slug))
    post.is_featured = not post.is_featured
    db.session.commit()
    flash("Toggled featured.", "success")
    return redirect(url_for("posts.detail_post", slug=slug))

# Comments (anyone can add; only admin can delete)
@posts_bp.route("/<slug>/comment", methods=["POST"])
def add_comment(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    author = (request.form.get("author_name") or "").strip() or "Anonymous"
    text = (request.form.get("text") or "").strip()
    if not text:
        flash("Comment cannot be empty.", "warning")
        return redirect(url_for("posts.detail_post", slug=slug))
    c = Comment(post_id=post.id, author_name=author, text=text)
    db.session.add(c)
    db.session.commit()
    flash("Comment added!", "success")
    return redirect(url_for("posts.detail_post", slug=slug))

@posts_bp.route("/<slug>/delete-comment/<int:cid>", methods=["POST"])
@login_required
def delete_comment(slug, cid):
    post = Post.query.filter_by(slug=slug).first_or_404()
    comment = Comment.query.get_or_404(cid)
    if not current_user.is_admin:
        flash("Only admin can delete comments.", "danger")
        return redirect(url_for("posts.detail_post", slug=slug))
    if comment.post_id != post.id:
        flash("Invalid comment.", "danger")
        return redirect(url_for("posts.detail_post", slug=slug))
    db.session.delete(comment)
    db.session.commit()
    flash("Comment deleted.", "info")
    return redirect(url_for("posts.detail_post", slug=slug))
