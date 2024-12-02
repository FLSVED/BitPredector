# app/utils/security.py

# BitPredector Version 2.1.0

# Développé par LP

# Date de la dernière mise à jour : 18/11/2024

# Description: Utilitaires de sécurité pour le hachage des mots de passe et la vérification 2FA

import bcrypt
import pyotp

class SecurityUtils:

    @staticmethod
    def hash_password(password):
        """Hache un mot de passe."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    @staticmethod
    def verify_password(hashed, password):
        """Vérifie un mot de passe haché."""
        return bcrypt.checkpw(password.encode('utf-8'), hashed)

    @staticmethod
    def generate_2fa_secret():
        """Génère un secret de 2FA."""
        return pyotp.random_base32()

    @staticmethod
    def verify_2fa_code(secret, code):
        """Vérifie un code 2FA."""
        totp = pyotp.TOTP(secret)
        return totp.verify(code)
