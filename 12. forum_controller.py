# app/controllers/forum_controller.py

# BitPredector Version 1.0.0

# Développé par LP

# Date de la dernière mise à jour : 18/11/2024

# Description: Contrôleur pour gérer les opérations de forum

from flask import Blueprint, jsonify, request
from ..models import ForumPost
from ..extensions import db

forum_api = Blueprint('forum_api', __name__)

@forum_api.route('/forum', methods=['POST'])
def create_forum_post():
    data = request.get_json()
    new_post = ForumPost(title=data['title'], content=data['content'], user_id=data['user_id'])
    db.session.add(new_post)
    db.session.commit()
    return jsonify({"message": "Post créé avec succès", "status": 201}), 201

@forum_api.route('/forum', methods=['GET'])
def get_forum_posts():
    posts = ForumPost.query.all()
    return jsonify([{"title": post.title, "content": post.content} for post in posts]), 200
