# app/services/news_service.py

# BitPredector Version 2.2.0

# Développé par LP

# Date de la dernière mise à jour : 18/11/2024

# Description: Service pour gérer les opérations liées aux articles de presse

import requests
from ..models import NewsArticle
from ..extensions import db
from ..config import Config

class NewsService:

    def fetch_news(self):
        """Récupère les nouvelles liées aux cryptomonnaies à partir de l'API News."""
        params = {
            'q': 'cryptocurrency',
            'apiKey': Config.NEWS_API_KEY,
            'language': 'en',
            'sortBy': 'publishedAt'
        }
        response = requests.get("https://newsapi.org/v2/everything", params=params)
        if response.status_code == 200:
            news_data = response.json().get('articles', [])
            for article in news_data:
                self.save_article(article)

    def save_article(self, article):
        """Enregistre un article dans la base de données."""
        news_article = NewsArticle(
            title=article['title'],
            content=article['description'] or article['content'],
            url=article['url']
        )
        db.session.add(news_article)
        db.session.commit()

    def get_latest_articles(self):
        """Récupère les 10 derniers articles de la base de données."""
        return NewsArticle.query.order_by(NewsArticle.id.desc()).limit(10).all()
