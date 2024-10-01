# app.py
from flask import Flask, jsonify, request, render_template
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

NEWS_API_KEY = os.getenv('NEWS_API_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/news', methods=['GET'])
def get_news():
    category = request.args.get('category', 'general')
    search = request.args.get('search', '')

    url = f'https://newsapi.org/v2/top-headlines?category={category}&apiKey={NEWS_API_KEY}'
    response = requests.get('https://newsapi.org/v2/everything', params={'q': 'political', 'apiKey': NEWS_API_KEY})
    print(response.json())

    articles = response.json().get('articles', [])

    if search:
        articles = [article for article in articles if search.lower() in article['title'].lower()]

    return jsonify({'articles': articles})

if __name__ == '__main__':
    app.run(debug=True)
