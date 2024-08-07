# desktop_app/flask_server.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from threading import Thread

app = Flask(__name__)
CORS(app)

tweets_data = []

@app.route('/post_tweets', methods=['POST'])
def add_tweet():
    tweet_data = request.json.get('tweets', [])
    if isinstance(tweet_data, list):
        tweets_data.extend(tweet_data)
    return jsonify({"status": "success", "message": "Tweets added successfully"}), 200

@app.route('/get_tweets', methods=['GET'])
def get_tweets():
    return jsonify({'tweets': tweets_data})

def run_server():
    app.run(port=5000)

def start_server():
    server_thread = Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
