<<<<<<< HEAD
Python 3.12.6 (tags/v3.12.6:a4a2d2b, Sep  6 2024, 20:11:23) [MSC v.1940 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> # app/config.py
... 
... # BitPredector Version 2.2.0
... 
... # Développé par LP
... 
... # Date de la dernière mise à jour : 18/11/2024
... 
... # Description: Configuration de l'application, chargement des variables d'environnement
... 
... import os
... from dotenv import load_dotenv
... 
... load_dotenv()
... 
... class Config:
...     SECRET_KEY = os.getenv('SECRET_KEY')
...     SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
...     MAIL_SERVER = os.getenv('MAIL_SERVER')
...     MAIL_PORT = os.getenv('MAIL_PORT')
...     MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() in ['true', '1', 't']
...     MAIL_USERNAME = os.getenv('MAIL_USERNAME')
...     MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
...     CORS_HEADERS = 'Content-Type'
=======
Python 3.12.6 (tags/v3.12.6:a4a2d2b, Sep  6 2024, 20:11:23) [MSC v.1940 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> # app/config.py
... 
... # BitPredector Version 2.2.0
... 
... # Développé par LP
... 
... # Date de la dernière mise à jour : 18/11/2024
... 
... # Description: Configuration de l'application, chargement des variables d'environnement
... 
... import os
... from dotenv import load_dotenv
... 
... load_dotenv()
... 
... class Config:
...     SECRET_KEY = os.getenv('SECRET_KEY')
...     SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
...     MAIL_SERVER = os.getenv('MAIL_SERVER')
...     MAIL_PORT = os.getenv('MAIL_PORT')
...     MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() in ['true', '1', 't']
...     MAIL_USERNAME = os.getenv('MAIL_USERNAME')
...     MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
...     CORS_HEADERS = 'Content-Type'
>>>>>>> 777521d93e05d124c0ab38693e80b0fbc9f5a67c
