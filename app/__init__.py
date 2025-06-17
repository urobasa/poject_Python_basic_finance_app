from flask import Flask, redirect, url_for
from .config import Config
from .extensions import db, migrate, csrf, login_manager
from app.models.user import User


def create_app(config_name=None):
    app = Flask(__name__)
    if config_name == "testing":
        from .config import TestingConfig
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(Config)

    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)

    # Настройка Flask-Login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.context_processor
    def inject_csrf_token():
        from flask_wtf.csrf import generate_csrf
        return dict(csrf_token=generate_csrf)

    # Регистрация blueprints
    from .views.operations import operations_bp
    from .views.categories import categories_bp
    from .views.accounts import accounts_bp
    from .views.reports import reports_bp
    from .views.transfer_view import transfer_bp
    from app.views.auth import auth_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(operations_bp, url_prefix='/operations')
    app.register_blueprint(categories_bp, url_prefix='/categories')
    app.register_blueprint(accounts_bp, url_prefix='/accounts')
    app.register_blueprint(reports_bp, url_prefix='/reports')
    app.register_blueprint(transfer_bp, url_prefix='/transfer')

    @app.route('/')
    def index_redirect():
        return redirect(url_for('operations.list_operations'))

    return app
