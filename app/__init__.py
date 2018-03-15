import config
import os
from flask import (
    Flask,
    render_template,
    request,
    current_app)
from app.api import api as api_bp
from app.errors import errors as error_bp
from app.extensions import (
    bcrypt,
    db,
    login,
    migrate,
)


def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)
    register_blueprints(app)
    register_extensions(app)
    return app


def register_extensions(app):
    bcrypt.init_app(app)
    db.init_app(app)
    login.init_app(app)
    migrate.init_app(app, db)
    return None


def register_blueprints(app):
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(error_bp, url_prefix='/errors')
    return None
