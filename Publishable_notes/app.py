from flask import Flask, redirect, url_for
from flask_login import LoginManager
from flask_migrate import Migrate
from models import db, User
from routes.auth import auth_bp
from routes.notes import notes_bp
from routes.posts import posts_bp
from routes.tags import tags_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Initialize DB and migrations
    db.init_app(app)
    Migrate(app, db)

    # Initialize login manager
    login_manager = LoginManager(app)
    login_manager.login_view = "auth.login" # if we try to access /notes without login it will redirect to auth/login

    @login_manager.user_loader  # to load a user from the DB
    def load_user(user_id):
        return User.query.get(int(user_id))# finds the user in primary key

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(notes_bp, url_prefix='/notes')
    app.register_blueprint(posts_bp, url_prefix='/posts')
    app.register_blueprint(tags_bp, url_prefix='/tags')

    # Default home route
    @app.route("/")
    def home():
        return redirect(url_for("posts.list_posts")) #when user visits / redirects to /posts

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all() # create tables if they dont exist

        # Seed admin user if not exists
        if not User.query.filter_by(email="admin@example.com").first():
            admin_user = User(
                username="kalpesh",            # set default username
                email="admin@example.com",
                is_admin=True
            )
            # Set password using your User model method
            admin_user.set_password("admin")
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created: admin@example.com / admin")

    app.run(debug=True)
