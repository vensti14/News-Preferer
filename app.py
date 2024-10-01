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
    country = request.args.get('country', 'us')  # Default to US if no country specified

    # Base URL for News API
    url = 'https://newsapi.org/v2/top-headlines?'

    # If search is specified, we use the 'everything' endpoint
    if search:
        url = f'https://newsapi.org/v2/everything?q={search}&apiKey={NEWS_API_KEY}'
    else:
        # Add query parameters based on filters
        url += f'category={category}&country={country}&apiKey={NEWS_API_KEY}'

    # Make the API request
    response = requests.get(url)
    articles = response.json().get('articles', [])

    # Get the first article's image for the background
    background_image = articles[0]['urlToImage'] if articles else 'https://via.placeholder.com/1920x1080'

    return jsonify({'articles': articles, 'background_image': background_image})

if __name__ == '__main__':
    app.run(debug=True)
