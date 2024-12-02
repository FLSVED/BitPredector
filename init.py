# app/__init__.py

# BitPredector Version 2.3.1

# Développé par LP

# Date de la dernière mise à jour : 01/12/2024

# Description: Initialisation de l'application Flask pour BitPredector

import os
import logging
from logging.config import dictConfig
from flask import Flask
from .extensions import db, bcrypt, mail, csrf, cache
from .config import Config
from .routes import register_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configure logging
    configure_logging(app)
    
    # Initialisation des extensions
    initialize_extensions(app)

    # Enregistrement des routes
    register_routes(app)

    # Register Blueprints (Example)
    # from .blueprints.example import example_bp
    # app.register_blueprint(example_bp)

    # Register error handlers
    register_error_handlers(app)

    return app

def configure_logging(app):
    """Configure logging for the application."""
    log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': log_level,
            'handlers': ['wsgi']
        }
    })
    app.logger.setLevel(log_level)

def initialize_extensions(app):
    """Initialise les extensions avec l'application Flask."""
    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    cache.init_app(app)

def register_error_handlers(app):
    """Register error handlers for the application."""
    @app.errorhandler(404)
    def not_found_error(error):
        return {"error": "Not Found"}, 404

    @app.errorhandler(500)
    def internal_error(error):
        return {"error": "Internal Server Error"}, 500
