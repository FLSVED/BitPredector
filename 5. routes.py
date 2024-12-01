# app/routes.py

# BitPredector Version 2.4.0

# Développé par LP

# Date de la dernière mise à jour : 01/12/2024

# Description: Définition des routes API pour BitPredector

from flask import Blueprint, jsonify, request, render_template
import pandas as pd
import plotly.express as px
from .services.user_service import UserService
from .services.news_service import NewsService
from .services.market_service import MarketService
from .services.alert_service import AlertService
from .services.sentiment_service import SentimentService

api = Blueprint('api', __name__)

@api.route('/user/register', methods=['POST'])
def register_user():
    data = request.get_json()
    user_service = UserService()
    response = user_service.register_user(data['email'], data['password'])
    return jsonify(response), response['status']

@api.route('/news', methods=['GET'])
def get_news():
    news_service = NewsService()
    articles = news_service.get_latest_articles()
    return jsonify([article.to_dict() for article in articles]), 200

@api.route('/market/predict', methods=['GET'])
def predict_market():
    market_service = MarketService()
    predictions = market_service.predict_market()
    return jsonify(predictions), 200

@api.route('/alerts', methods=['POST'])
def create_alert():
    data = request.get_json()
    alert_service = AlertService()
    response = alert_service.create_alert(data['user_id'], data['crypto_name'], data['target_price'])
    return jsonify(response), response['status']

@api.route('/sentiment/<string:crypto_name>', methods=['GET'])
def get_sentiment_analysis(crypto_name):
    sentiment_service = SentimentService(
        twitter_api_key='your_twitter_api_key',
        twitter_api_secret_key='your_twitter_api_secret_key',
        twitter_access_token='your_access_token',
        twitter_access_token_secret='your_access_token_secret',
        reddit_client_id='your_reddit_client_id',
        reddit_client_secret='your_reddit_client_secret',
        reddit_user_agent='your_reddit_user_agent',
        news_api_key='your_news_api_key'
    )
    sentiment_results = sentiment_service.analyze_crypto_sentiment(crypto_name)
    return jsonify(sentiment_results), 200

@api.route('/dashboard', methods=['GET'])
def dashboard():
    data = pd.read_csv('crypto_data.csv')  # Suppose que vous avez des données historiques
    fig = px.line(data, x='date', y='price', title='Prix des Cryptomonnaies')
    graph = fig.to_html(full_html=False)
    return render_template('dashboard.html', graph=graph)

@api.route('/education', methods=['GET'])
def education():
    resources = [
        {"title": "Introduction aux Cryptomonnaies", "url": "/resources/intro"},
        {"title": "Analyse Technique", "url": "/resources/technical-analysis"}
    ]
    return jsonify(resources), 200