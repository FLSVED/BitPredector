# app/services/sentiment_service.py

# BitPredector Version 1.0.0

# Développé par LP

# Date de la dernière mise à jour : 18/11/2024

# Description: Service pour l'analyse sentimentale des cryptomonnaies

import tweepy
import requests
from textblob import TextBlob
import logging
import praw  # Pour accéder à Reddit

class SentimentService:

    def __init__(self, twitter_api_key, twitter_api_secret_key, twitter_access_token, twitter_access_token_secret, reddit_client_id, reddit_client_secret, reddit_user_agent, news_api_key):
        # Configuration de l'API Twitter
        self.twitter_auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_secret_key)
        self.twitter_auth.set_access_token(twitter_access_token, twitter_access_token_secret)
        self.twitter_api = tweepy.API(self.twitter_auth)

        # Configuration de l'API Reddit
        self.reddit = praw.Reddit(client_id=reddit_client_id, client_secret=reddit_client_secret, user_agent=reddit_user_agent)

        # Clé API pour NewsAPI
        self.news_api_key = news_api_key

        logging.basicConfig(level=logging.INFO)

    def get_tweets(self, keyword, count=100):
        """Récupère les tweets contenant le mot-clé spécifié."""
        tweets = []
        try:
            fetched_tweets = self.twitter_api.search(q=keyword, count=count, lang='en', tweet_mode='extended')
            for tweet in fetched_tweets:
                tweets.append(tweet.full_text)
            logging.info(f"{len(tweets)} tweets récupérés pour le mot-clé: {keyword}")
            return tweets
        except tweepy.TweepError as e:
            logging.error(f"Erreur lors de la récupération des tweets : {e}")
            return []

    def get_reddit_comments(self, keyword, count=100):
        """Récupère les commentaires de Reddit contenant le mot-clé spécifié."""
        comments = []
        try:
            subreddit = self.reddit.subreddit('cryptocurrency')
            for comment in subreddit.comments(limit=count):
                if keyword.lower() in comment.body.lower():
                    comments.append(comment.body)
            logging.info(f"{len(comments)} commentaires récupérés de Reddit pour le mot-clé: {keyword}")
            return comments
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des commentaires Reddit : {e}")
            return []

    def get_news_articles(self, keyword):
        """Récupère des articles d'actualités contenant le mot-clé spécifié."""
        articles = []
        url = f"https://newsapi.org/v2/everything?q={keyword}&apiKey={self.news_api_key}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                for article in data['articles']:
                    articles.append(article['title'] + " " + article['description'])
                logging.info(f"{len(articles)} articles récupérés pour le mot-clé: {keyword}")
            return articles
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des articles d'actualités : {e}")
            return []

    def analyze_sentiment(self, texts):
        """Analyse le sentiment des textes récupérés."""
        sentiment_results = []
        for text in texts:
            analysis = TextBlob(text)
            sentiment_results.append({
                'text': text,
                'polarity': analysis.sentiment.polarity,
                'subjectivity': analysis.sentiment.subjectivity
            })
        return sentiment_results

    def analyze_crypto_sentiment(self, crypto_name, tweet_count=100, reddit_count=100):
        """Récupère et analyse le sentiment des tweets et commentaires concernant une cryptomonnaie."""
        logging.info(f"Analyse du sentiment pour {crypto_name}...")
        tweets = self.get_tweets(crypto_name, tweet_count)
        reddit_comments = self.get_reddit_comments(crypto_name, reddit_count)
        all_texts = tweets + reddit_comments
        if not all_texts:
            logging.warning("Aucun texte récupéré. Analyse impossible.")
            return []
        sentiment_results = self.analyze_sentiment(all_texts)
        return sentiment_results
