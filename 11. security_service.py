# app/services/security_service.py

# BitPredector Version 1.0.0

# Développé par LP

# Date de la dernière mise à jour : 01/12/2024

# Description: Service pour la sécurité des actifs et détection d'anomalies

from ..models import User
from ..extensions import db
import numpy as np

class SecurityService:
    def detect_anomalies(self, user_id):
        """Détecte les anomalies dans les transactions de l'utilisateur."""
        transactions = self.get_user_transactions(user_id)
        if not transactions:
            return []

        mean = np.mean(transactions)
        std_dev = np.std(transactions)
        thresholds = mean + 3 * std_dev
        anomalies = [t for t in transactions if t > thresholds]
        return anomalies

    def get_user_transactions(self, user_id):
        """Récupère les transactions d'un utilisateur."""
        # Logique pour récupérer les transactions d'un utilisateur
        # Exemple : Requête à la base de données pour récupérer les transactions
        user = User.query.get(user_id)
        if not user:
            return []

        transactions = [t.amount for t in user.transactions]  # Supposons que chaque transaction a un montant
        return transactions