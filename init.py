# app/__init__.py

# BitPredector Version 2.3.1

# Développé par LP

# Date de la dernière mise à jour : 01/12/2024

# Description: Initialisation de l'application Flask pour BitPredector

from flask import Flask
from .extensions import db, bcrypt, mail, csrf, cache
from .config import Config
from .routes import register_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialisation des extensions
    initialize_extensions(app)

    # Enregistrement des routes
    register_routes(app)
    
    return app

def initialize_extensions(app):
    """Initialise les extensions avec l'application Flask."""
    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    cache.init_app(app)