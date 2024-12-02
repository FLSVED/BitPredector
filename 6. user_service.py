<<<<<<< HEAD
# app/services/user_service.py

# BitPredector Version 2.3.0

# Développé par LP

# Date de la dernière mise à jour : 18/11/2024

# Description: Service pour gérer les opérations utilisateur

from flask import url_for
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from ..models import User
from ..extensions import db, bcrypt, mail
from ..config import Config

class UserService:

    def register_user(self, email, password):
        """Enregistre un nouvel utilisateur et envoie un e-mail de confirmation."""
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        token = URLSafeTimedSerializer(Config.SECRET_KEY).dumps(email, salt=Config.SECURITY_PASSWORD_SALT)
        link = url_for('api.confirm_email', token=token, _external=True)
        msg = Message('Confirm your email', sender=Config.MAIL_USERNAME, recipients=[email])
        msg.body = f'Your link is {link}'
        mail.send(msg)

        return {"message": "Please confirm your email address", "status": 201}

    def login_user(self, email, password):
        """Authentifie un utilisateur."""
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            if not user.confirmed:
                return {"message": "Please confirm your email address", "status": 400}
            return {"message": "Login successful", "status": 200}
        return {"message": "Login unsuccessful. Please check email and password", "status": 401}
=======
# app/services/user_service.py

# BitPredector Version 2.3.0

# Développé par LP

# Date de la dernière mise à jour : 18/11/2024

# Description: Service pour gérer les opérations utilisateur

from flask import url_for
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from ..models import User
from ..extensions import db, bcrypt, mail
from ..config import Config

class UserService:

    def register_user(self, email, password):
        """Enregistre un nouvel utilisateur et envoie un e-mail de confirmation."""
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        token = URLSafeTimedSerializer(Config.SECRET_KEY).dumps(email, salt=Config.SECURITY_PASSWORD_SALT)
        link = url_for('api.confirm_email', token=token, _external=True)
        msg = Message('Confirm your email', sender=Config.MAIL_USERNAME, recipients=[email])
        msg.body = f'Your link is {link}'
        mail.send(msg)

        return {"message": "Please confirm your email address", "status": 201}

    def login_user(self, email, password):
        """Authentifie un utilisateur."""
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            if not user.confirmed:
                return {"message": "Please confirm your email address", "status": 400}
            return {"message": "Login successful", "status": 200}
        return {"message": "Login unsuccessful. Please check email and password", "status": 401}
>>>>>>> 777521d93e05d124c0ab38693e80b0fbc9f5a67c
