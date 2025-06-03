from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Регистрация роутов (blueprints)
    from .views.dashboard import dashboard_bp
    from .views.operations import operations_bp
    from .views.categories import categories_bp
    from .views.accounts import accounts_bp
    from .views.reports import reports_bp
    from .views.transfer_view import transfer_bp

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(operations_bp, url_prefix='/operations')
    app.register_blueprint(categories_bp, url_prefix='/categories')
    app.register_blueprint(accounts_bp, url_prefix='/accounts')
    app.register_blueprint(reports_bp, url_prefix='/reports')
    app.register_blueprint(transfer_bp, url_prefix='/transfer')
    return app
