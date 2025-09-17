import datetime
from flask import Flask, jsonify, request, render_template
from .config import Config
from .extensions import db, migrate, login_manager, jwt
from .web.views import web_bp
from .auth.routes import auth_bp
from .api.polls import api_bp

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(Config)

    # inject current year in templates
    @app.context_processor
    def inject_now():
        return {'year': datetime.datetime.utcnow().year}

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    jwt.init_app(app)
    app.config["JWT_SECRET_KEY"] = "super-secret-key"

    # register blueprints
    app.register_blueprint(web_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(api_bp, url_prefix='/api')

    # error handlers
    @app.errorhandler(404)
    def not_found(e):
        if request.path.startswith('/api') or (request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html):
            return jsonify(status='error', error={'code':404, 'message':'Not Found'}), 404
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        if request.path.startswith('/api') or (request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html):
            return jsonify(status='error', error={'code':500, 'message':'Internal Server Error'}), 500
        return render_template('500.html'), 500

    return app
