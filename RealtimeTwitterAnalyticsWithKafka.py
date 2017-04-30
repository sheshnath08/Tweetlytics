import json

from flask import Flask
from flask import render_template
from flask import request

import keys
import tweepy
from TweetStream import TweetStream
from flask_socketio import SocketIO

app = Flask(__name__)

ACCESS_TOKEN = keys.TWITTER_ACCESS_TOKEN
ACCESS_SECRET = keys.TWITTER_ACCESS_SECRET
CONSUMER_KEY = keys.TWITTER_CONSUMER_KEY
CONSUMER_SECRET = keys.TWITTER_CONSUMER_SECRET

oauth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
oauth.set_access_token(ACCESS_TOKEN,ACCESS_SECRET)
# tweepy api auth, used to get tweets from twitter
api = tweepy.API(oauth)

application = Flask(__name__)
socketio = SocketIO(application)

@application.route('/', methods=['GET'])
def hello_world():
    tweet_listner = TweetStream()
    tweet_stream = tweepy.Stream(auth=api.auth, listener=tweet_listner)
    tweet_stream.filter(languages=["en"],
                        track=['i','u','in','is','was','where','you','me','have','with',\
                               'buy','bought','product','india'],
                        async=True)

    return render_template('index.html')


@application.route('/notify',methods=['POST'])
def notify():
    data = str(request.get_data(), encoding='utf-8')
    socketio.emit('newTweet',data)

    return 'home'


if __name__ == '__main__':
    socketio.run(application)
