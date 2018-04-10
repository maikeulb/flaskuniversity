import os
from app import create_app, cli
from app.extensions import db

app = create_app(os.getenv('FLASK_APP_CONFIG') or 'config.DevelopmentConfig')
cli.register(app)
