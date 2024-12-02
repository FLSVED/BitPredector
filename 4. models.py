# app/models.py

# BitPredector Version 2.3.0

# Développé par LP

# Date de la dernière mise à jour : 18/11/2024

# Description: Définition des modèles de données pour SQLAlchemy

from .extensions import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    confirmed = db.Column(db.Boolean, default=False)

class NewsArticle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)
    url = db.Column(db.String, nullable=False)

class MarketPrediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crypto_name = db.Column(db.String, nullable=False)
    prediction = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    arima_params = db.Column(db.String, nullable=True)

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    crypto_name = db.Column(db.String, nullable=False)
    target_price = db.Column(db.Float, nullable=False)

class ForumPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    crypto_name = db.Column(db.String, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    purchase_price = db.Column(db.Float, nullable=False)
