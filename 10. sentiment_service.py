
Module: sentiment_service

Version: 2.0.0
Date de la dernière mise à jour: 03/12/2024

Description:
Ce module fournit une analyse de sentiment pour les marchés de la cryptomonnaie en utilisant plusieurs sources de données, y compris Twitter, Reddit et des articles d'actualités. Les utilisateurs peuvent activer ou désactiver les sources selon leurs préférences.

Classes:
- DataSource: Classe de base pour toutes les sources de données.
- TwitterSource: Source de données pour Twitter.
- RedditSource: Source de données pour Reddit.
- NewsSource: Source de données pour les articles d'actualités.
- SentimentAnalyzer: Classe pour analyser le sentiment des textes collectés à partir des sources activées.

Fonctions:
- main: Fonction principale pour exécuter l'analyseur de sentiment.

Utilisation:
1. Configurez les clés API requises dans les variables d'environnement.
2. Activez les sources de données souhaitées.
3. Exécutez la fonction `main` pour obtenir le ratio de confiance pour un mot-clé donné.

Exemple:
    asyncio.run(main())
"""

import os
import logging
import asyncio
import aiohttp
from textblob import TextBlob
import tweepy
import praw

# Configure logging
logging.basicConfig(level=logging.INFO)

class DataSource:
    """Classe de base pour toutes les sources de données."""
    def __init__(self, name, enabled=False):
        self.name = name
        self.enabled = enabled
    
    async def fetch_data(self, keyword):
        """Cette méthode doit être implémentée par chaque source spécifique."""
        raise NotImplementedError("fetch_data doit être implémentée par les sous-classes")

class TwitterSource(DataSource):
    """Source de données pour Twitter."""
    def __init__(self, api, name="Twitter", enabled=False):
        super().__init__(name, enabled)
        self.api = api

    async def fetch_data(self, keyword):
        try:
            logging.info(f"Fetching tweets for {keyword}")
            fetched_tweets = self.api.search(q=keyword, count=100, lang='en', tweet_mode='extended')
            return [tweet.full_text for tweet in fetched_tweets]
        except tweepy.TweepError as e:
            logging.error(f"Error fetching tweets: {e}")
            return []

class RedditSource(DataSource):
    """Source de données pour Reddit."""
    def __init__(self, reddit_client, name="Reddit", enabled=False):
        super().__init__(name, enabled)
        self.reddit_client = reddit_client

    async def fetch_data(self, keyword):
        try:
            logging.info(f"Fetching Reddit comments for {keyword}")
            subreddit = self.reddit_client.subreddit('cryptocurrency')
            return [comment.body for comment in subreddit.comments(limit=100) if keyword.lower() in comment.body.lower()]
        except Exception as e:
            logging.error(f"Error fetching Reddit comments: {e}")
            return []

class NewsSource(DataSource):
    """Source de données pour les articles d'actualités."""
    def __init__(self, api_key, name="News", enabled=False):
        super().__init__(name, enabled)
        self.api_key = api_key

    async def fetch_data(self, keyword):
        url = f"https://newsapi.org/v2/everything?q={keyword}&apiKey={self.api_key}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        return [article['title'] + " " + article['description'] for article in data['articles']]
                    else:
                        logging.error(f"Error fetching news articles: {response.status}")
                        return []
        except Exception as e:
            logging.error(f"Error fetching news articles: {e}")
            return []

class SentimentAnalyzer:
    """Classe pour analyser le sentiment des textes collectés."""
    def __init__(self, sources):
        self.sources = sources

    async def analyze(self, keyword):
        results = []
        for source in self.sources:
            if source.enabled:
                data = await source.fetch_data(keyword)
                sentiments = [self.analyze_sentiment(text) for text in data]
                results.extend(sentiments)
        return self.calculate_confidence(results)

    @staticmethod
    def analyze_sentiment(text):
        analysis = TextBlob(text)
        return analysis.sentiment.polarity

    @staticmethod
    def calculate_confidence(sentiments):
        if not sentiments:
            return 0
        positive = len([s for s in sentiments if s > 0])
        negative = len([s for s in sentiments if s < 0])
        return (positive - negative) / len(sentiments)

async def main():
    """Fonction principale pour exécuter l'analyseur de sentiment."""
    # Initialize API clients
    twitter_api_key = os.getenv("TWITTER_API_KEY")
    twitter_api_secret_key = os.getenv("TWITTER_API_SECRET_KEY")
    twitter_access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    twitter_access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    twitter_auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_secret_key)
    twitter_auth.set_access_token(twitter_access_token, twitter_access_token_secret)
    twitter_api = tweepy.API(twitter_auth)

    reddit_client_id = os.getenv("REDDIT_CLIENT_ID")
    reddit_client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    reddit_user_agent = os.getenv("REDDIT_USER_AGENT")
    reddit = praw.Reddit(client_id=reddit_client_id, client_secret=reddit_client_secret, user_agent=reddit_user_agent)

    news_api_key = os.getenv("NEWS_API_KEY")

    # Initialize sources with user preference (in a real-world scenario, these could be set via a UI)
    sources = [
        TwitterSource(twitter_api, enabled=True),
        RedditSource(reddit, enabled=True),
        NewsSource(news_api_key, enabled=True),
    ]

    analyzer = SentimentAnalyzer(sources)
    confidence = await analyzer.analyze("Bitcoin")
    print(f"Confidence ratio for Bitcoin: {confidence:.2f}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Tests Unitaires

Voici les tests unitaires associés pour s'assurer que chaque composant fonctionne correctement :

```python
import unittest
from unittest.mock import AsyncMock, patch
from sentiment_service import TwitterSource, RedditSource, NewsSource, SentimentAnalyzer

class TestSentimentService(unittest.TestCase):

    @patch('sentiment_service.tweepy.API')
    def test_twitter_source(self, MockTwitterAPI):
        # Mocking Twitter API
        mock_api = MockTwitterAPI.return_value
        mock_api.search.return_value = [AsyncMock(full_text="Positive tweet about Bitcoin")]

        twitter_source = TwitterSource(mock_api, enabled=True)
        data = asyncio.run(twitter_source.fetch_data("Bitcoin"))
        self.assertEqual(len(data), 1)
        self.assertIn("Positive tweet about Bitcoin", data)

    @patch('sentiment_service.praw.Reddit')
    def test_reddit_source(self, MockReddit):
        # Mocking Reddit API
        mock_reddit = MockReddit.return_value
        mock_comments = [AsyncMock(body="Positive Reddit comment about Bitcoin")]
        mock_subreddit = AsyncMock()
        mock_subreddit.comments.return_value = mock_comments
        mock_reddit.subreddit.return_value = mock_subreddit

        reddit_source = RedditSource(mock_reddit, enabled=True)
        data = asyncio.run(reddit_source.fetch_data("Bitcoin"))
        self.assertEqual(len(data), 1)
        self.assertIn("Positive Reddit comment about Bitcoin", data)

    @patch('sentiment_service.aiohttp.ClientSession')
    def test_news_source(self, MockClientSession):
        # Mocking News API
        mock_session = MockClientSession.return_value
        mock_get = mock_session.get.return_value.__aenter__.return_value
        mock_get.status = 200
        mock_get.json.return_value = {
            'articles': [{'title': 'Positive news about Bitcoin', 'description': 'Bitcoin is rising'}]
        }

        news_source = NewsSource("fake_api_key", enabled=True)
        data = asyncio.run(news_source.fetch_data("Bitcoin"))
        self.assertEqual(len(data), 1)
        self.assertIn("Positive news about Bitcoin Bitcoin is rising", data)

    def test_sentiment_analyzer(self):
        sources = [
            TwitterSource(None, enabled=False),
            RedditSource(None, enabled=False),
            NewsSource(None, enabled=False)
        ]
