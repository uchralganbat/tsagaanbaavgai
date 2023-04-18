import os
import requests
import tweepy
from flask import Flask, jsonify
from dotenv import load_dotenv
import sys
load_dotenv()

app = Flask(__name__)

BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

print(ACCESS_TOKEN_SECRET, ACCESS_TOKEN, BEARER_TOKEN)

@app.route('/search/<query>')
def search_tweets(query):
    url = f'https://api.twitter.com/2/tweets/search/recent?query={query}&max_results=10'
    headers = {'Authorization': f'Bearer {BEARER_TOKEN}'}
    response = requests.get(url, headers=headers)
    print(response.json())
    if response.status_code != 200:
        return jsonify({'error': f'Request failed: {response.text}'}), response.status_code
    return response.json()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

