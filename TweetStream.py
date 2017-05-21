import json
import traceback
import tweepy
from producer import Producer

class TweetStream(tweepy.StreamListener):
    # Kafka producer
    producer = Producer()
    def on_data(self, raw_data):
        # TODO: Change this url to deploy url or find some hack around it
        try:
            tweets_json = json.loads(raw_data, encoding='utf-8')
            self.producer.send_tweet('newtweet', tweets_json['text'])
        except:
            traceback.print_exc()
            print('error', raw_data)

    def on_error(self, status_code):
        if status_code==420:
            # if rate limit exceeds
            return False
