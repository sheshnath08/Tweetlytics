import os
from threading import Thread
from flask import Flask, json
from flask import render_template
from flask import request
import keys
import tweepy

from TweetStream import TweetStream
from flask_socketio import SocketIO, disconnect
from consumer import Consumer
from TrendingHashtagConsumer import TrendingHashtagConsumer

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

thread = None

count = 0

def stream_tweets_background():
    """Get tweets from twitter"""
    tweet_listner = TweetStream()
    tweet_stream = tweepy.Stream(auth=api.auth, listener=tweet_listner, wait_on_rate_limit=True)
    tweet_stream.filter(languages=["en"],
                        track=['i', 'u', 'in', 'is', 'was', 'where', 'you', 'me', 'have', 'with', \
                               'buy', 'bought', 'product', 'india'],
                        async=True)

def start_stop_consumer(flag):
    consumer = TrendingHashtagConsumer()
    consumer1 = Consumer()
    if flag:
        consumer.start()
        consumer1.start()
    else:
        consumer.stop()
        consumer1.stop()


@application.route('/', methods=['GET'])
def hello_world():
    global thread
    if thread is None:
        thread = Thread(target=stream_tweets_background())
        thread.start()
        start_stop_consumer(True)

    return render_template('index.html')

@socketio.on('connected')
def connected():
    print(request.sid, "connected")

@application.route('/notify',methods=['POST'])
def notify():
    """This will send the new tweets to """
    try:
        data = request.get_data().decode()
        socketio.emit('newTweet',data)
    except:
        print('error')
    return 'home'


@application.route('/tweet-count',methods=['POST'])
def tweet_count():
    data = request.get_data().decode()
    socketio.emit('tweetcount',data)
    return 'home'

@application.route('/trending-hashtag',methods=['POST'])
def trend_count():
    data = request.get_data().decode()
    json_data = json.loads(data)
    socketio.emit('sentiment',json_data)
    return 'home'

@application.route('/sentiment',methods=['POST'])
def sentiment():
    data = request.get_data().decode()
    json_data = json.loads(data)
    socketio.emit('sentiment',json_data)
    return 'home'



@socketio.on('disconnected', namespace='/')
def test_disconnect():
    start_stop_consumer(False)
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(application, host='0.0.0.0', port=port)
