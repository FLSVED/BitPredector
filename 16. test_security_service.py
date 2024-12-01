# tests/test_security_service.py

# BitPredector Version 1.0.0

# Développé par LP

# Date de la dernière mise à jour : 18/11/2024

# Description: Tests unitaires pour le service de sécurité

import pytest
from app import create_app
from app.extensions import db
from app.services.security_service import SecurityService

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()

def test_detect_anomalies(app):
    security_service = SecurityService()
    anomalies = security_service.detect_anomalies(1)  # Exemple d'utilisateur
    assert isinstance(anomalies, list)
