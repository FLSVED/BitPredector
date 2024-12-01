Python 3.12.6 (tags/v3.12.6:a4a2d2b, Sep  6 2024, 20:11:23) [MSC v.1940 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> # app/__init__.py
... 
... # BitPredector Version 2.3.0
... 
... # Développé par LP
... 
... # Date de la dernière mise à jour : 18/11/2024
... 
... # Description: Initialisation de l'application Flask pour BitPredector
... 
... from flask import Flask
... from .extensions import db, bcrypt, mail, csrf, cache
... from .config import Config
... from .routes import register_routes
... 
... def create_app():
...     app = Flask(__name__)
...     app.config.from_object(Config)
... 
...     # Initialisation des extensions
...     db.init_app(app)
...     bcrypt.init_app(app)
...     mail.init_app(app)
...     csrf.init_app(app)
...     cache.init_app(app)
... 
...     # Enregistrement des routes
...     register_routes(app)
... 
