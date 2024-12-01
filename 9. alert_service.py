# app/services/alert_service.py

# BitPredector Version 2.2.0

# Développé par LP

# Date de la dernière mise à jour : 18/11/2024

# Description: Service pour gérer les alertes basées sur les prédictions de marché

from ..models import Alert
from ..extensions import db
from ..utils.security import SecurityUtils

class AlertService:

    def create_alert(self, user_id, crypto_name, target_price):
        """Crée une alerte pour un utilisateur spécifié."""
        alert = Alert(user_id=user_id, crypto_name=crypto_name, target_price=target_price)
        db.session.add(alert)
        db.session.commit()
        return {"message": "Alert created successfully", "status": 201}

    def verify_2fa_code(self, user_secret, code):
        """Vérifie le code 2FA pour l'utilisateur."""
        return SecurityUtils.verify_2fa_code(user_secret, code)

    def check_alerts(self):
        """Vérifie les alertes par rapport aux prédictions de marché."""
        # Logique pour vérifier les alertes par rapport aux prédictions de marché
        pass
