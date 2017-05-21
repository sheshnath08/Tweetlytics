import json
import traceback
import tweepy
import requests
from producer import Producer

class TweetStream(tweepy.StreamListener):
    producer = Producer()
    def on_data(self, raw_data):
        # TODO: Change this url to deploy url or find some hack around it
        try:
            tweets_json = json.loads(raw_data, encoding='utf-8')
            self.producer.send_tweet('newtweet', tweets_json["text"])
            requests.post('http://localhost:5000/notify', tweets_json["text"])
        except:
            traceback.print_exc()
            print('error')

    def on_error(self, status_code):
        if status_code==420:
            # if rate limit exceeds
            return False
