<<<<<<< HEAD
# tests/test_forum_service.py

# BitPredector Version 1.0.0

# Développé par LP

# Date de la dernière mise à jour : 18/11/2024

# Description: Tests unitaires pour le service de forum

import pytest
from app import create_app
from app.extensions import db
from app.models import ForumPost

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

def test_create_forum_post(app):
    new_post = ForumPost(title="Test Title", content="This is a test post.", user_id=1)
    db.session.add(new_post)
    db.session.commit()
    assert new_post.id is not None
=======
# tests/test_forum_service.py

# BitPredector Version 1.0.0

# Développé par LP

# Date de la dernière mise à jour : 18/11/2024

# Description: Tests unitaires pour le service de forum

import pytest
from app import create_app
from app.extensions import db
from app.models import ForumPost

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

def test_create_forum_post(app):
    new_post = ForumPost(title="Test Title", content="This is a test post.", user_id=1)
    db.session.add(new_post)
    db.session.commit()
    assert new_post.id is not None
>>>>>>> 777521d93e05d124c0ab38693e80b0fbc9f5a67c
