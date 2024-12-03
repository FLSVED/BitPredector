Module: sentiment_service
Version: 2.2.0
Date de la dernière mise à jour: 03/12/2024

Description:
Ce module fournit une analyse de sentiment pour les marchés de la cryptomonnaie en utilisant plusieurs sources de données,
y compris Twitter, Reddit, et des articles d'actualités. Il utilise des techniques avancées de NLP et met en œuvre
des mécanismes de mise en cache pour optimiser les performances.

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
import tweepy
import praw
from transformers import pipeline
from cachetools import TTLCache, cached

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Cache configuration
cache = TTLCache(maxsize=100, ttl=300)

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

    @cached(cache)
    async def fetch_data(self, keyword):
        if not self.enabled:
            logger.info(f"Source {self.name} désactivée.")
            return []
        try:
            logger.info(f"Fetching tweets for {keyword}")
            fetched_tweets = self.api.search(q=keyword, count=100, lang='en', tweet_mode='extended')
            return [tweet.full_text for tweet in fetched_tweets]
        except tweepy.TweepError as e:
            logger.error(f"Error fetching tweets: {e}. Check API keys and network connectivity.")
            return []

class RedditSource(DataSource):
    """Source de données pour Reddit."""
    def __init__(self, reddit_client, name="Reddit", enabled=False):
        super().__init__(name, enabled)
        self.reddit_client = reddit_client

    @cached(cache)
    async def fetch_data(self, keyword):
        if not self.enabled:
            logger.info(f"Source {self.name} désactivée.")
            return []
        try:
            logger.info(f"Fetching Reddit comments for {keyword}")
            subreddit = self.reddit_client.subreddit('cryptocurrency')
            return [comment.body for comment in subreddit.comments(limit=100) if keyword.lower() in comment.body.lower()]
        except Exception as e:
            logger.error(f"Error fetching Reddit comments: {e}. Ensure Reddit API credentials are valid.")
            return []

class NewsSource(DataSource):
    """Source de données pour les articles d'actualités."""
    def __init__(self, api_key, name="News", enabled=False):
        super().__init__(name, enabled)
        self.api_key = api_key

    @cached(cache)
    async def fetch_data(self, keyword):
        if not self.enabled:
            logger.info(f"Source {self.name} désactivée.")
            return []
        url = f"https://newsapi.org/v2/everything?q={keyword}&apiKey={self.api_key}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        return [f"{article['title']} {article['description']}" for article in data['articles']]
                    else:
                        logger.error(f"Error fetching news articles: {response.status}. Verify API key and query parameters.")
                        return []
        except Exception as e:
            logger.error(f"Error fetching news articles: {e}. Check network connectivity and API availability.")
            return []

class SentimentAnalyzer:
    """Classe pour analyser le sentiment des textes collectés."""
    def __init__(self, sources):
        self.sources = sources
        self.sentiment_pipeline = pipeline("sentiment-analysis")

    async def analyze(self, keyword):
        results = []
        for source in self.sources:
            if source.enabled:
                data = await source.fetch_data(keyword)
                sentiments = [self.analyze_sentiment(text) for text in data]
                results.extend(sentiments)
        return self.calculate_confidence(results)

    def analyze_sentiment(self, text):
        try:
            analysis = self.sentiment_pipeline(text)
            return 1 if analysis[0]['label'] == 'POSITIVE' else -1
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}.")
            return 0

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
