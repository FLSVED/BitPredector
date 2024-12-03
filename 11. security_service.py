BitPredector Version 2.1.0
Développé par LP
Date de la dernière mise à jour : 03/12/2024

Description:
Service pour la sécurité des actifs et la détection d'anomalies dans les transactions des utilisateurs.
Utilise des techniques statistiques avancées pour une détection robuste.
"""

import logging
import pandas as pd
from ..models import User
from ..extensions import db

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SecurityService:
    def __init__(self, threshold_multiplier=3, iqr_multiplier=1.5):
        self.threshold_multiplier = threshold_multiplier
        self.iqr_multiplier = iqr_multiplier

    def detect_anomalies(self, user_id):
        """
        Détecte les anomalies dans les transactions de l'utilisateur.

        Args:
            user_id (int): L'identifiant de l'utilisateur.

        Returns:
            list: Liste des montants de transactions considérées comme des anomalies.
        """
        try:
            if not isinstance(user_id, int) or user_id <= 0:
                logger.error("Invalid user_id provided.")
                return []

            transactions = self.get_user_transactions(user_id)
            if transactions.empty:
                logger.info(f"Aucune transaction trouvée pour l'utilisateur ID {user_id}.")
                return []

            anomalies = self._find_anomalies(transactions['amount'])
            logger.info(f"Anomalies détectées pour l'utilisateur ID {user_id}: {anomalies}")

            return anomalies.tolist()

        except Exception as e:
            logger.error(f"Erreur lors de la détection des anomalies pour l'utilisateur ID {user_id}: {e}")
            return []

    def get_user_transactions(self, user_id):
        """
        Récupère les transactions d'un utilisateur.

        Args:
            user_id (int): L'identifiant de l'utilisateur.

        Returns:
            pd.DataFrame: Un DataFrame contenant les montants des transactions de l'utilisateur.
        """
        try:
            user = User.query.get(user_id)
            if not user:
                logger.warning(f"Utilisateur ID {user_id} non trouvé.")
                return pd.DataFrame()

            transactions = pd.DataFrame(user.transactions, columns=['amount'])
            return transactions

        except Exception as e:
            logger.error(f"Erreur lors de la récupération des transactions pour l'utilisateur ID {user_id}: {e}")
            return pd.DataFrame()

    def _find_anomalies(self, amounts):
        """
        Identifie les anomalies dans une série de montants.

        Args:
            amounts (pd.Series): Série de montants à analyser.

        Returns:
            pd.Series: Montants considérés comme anomalies.
        """
        # Méthode utilisant l'écart-type
        mean = amounts.mean()
        std_dev = amounts.std()
        threshold_std = mean + self.threshold_multiplier * std_dev

        # Méthode utilisant l'IQR
        Q1 = amounts.quantile(0.25)
        Q3 = amounts.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - self.iqr_multiplier * IQR
        upper_bound = Q3 + self.iqr_multiplier * IQR

        # Combinaison des deux méthodes
        anomalies = amounts[(amounts > threshold_std) | (amounts < lower_bound) | (amounts > upper_bound)]
        return anomalies
```
