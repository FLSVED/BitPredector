Python 3.12.6 (tags/v3.12.6:a4a2d2b, Sep  6 2024, 20:11:23) [MSC v.1940 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> # app/extensions.py
... 
... # BitPredector Version 2.2.0
... 
... # Développé par LP
... 
... # Date de la dernière mise à jour : 18/11/2024
... 
... # Description: Gestion des extensions pour l'application Flask
... 
... from flask_sqlalchemy import SQLAlchemy
... from flask_bcrypt import Bcrypt
... from flask_mail import Mail
... from flask_wtf import CSRFProtect
... from flask_caching import Cache
... 
... db = SQLAlchemy()
... bcrypt = Bcrypt()
... mail = Mail()
... csrf = CSRFProtect()
