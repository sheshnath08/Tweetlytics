import json
import threading
import requests
from kafka import KafkaConsumer
from keys import KAFKA_URL, APP_URL

class Consumer(threading.Thread):
    '''This is kafka consumer to show tweets and count'''
    count = 0

    trend = {}

    def extract_hash_tags(self, s):
        s = s.lower()
        return set(part[1:] for part in s.split() if part.startswith('#'))

    def update_trend(self, hashtag):
        keys = self.trend.keys()
        for item in hashtag:
            if (len(item) < 3):
                continue
            if item in keys:
                self.trend[item] = self.trend[item] + 1
            else:
                self.trend[item] = 1

    def getTopNhashags(self, n):
        if (len(self.trend) >= n):
            top = sorted(self.trend.items(), key=lambda x: x[1], reverse=True)[:n]
        else:
            top = sorted(self.trend.items(), key=lambda x: x[1], reverse=True)
        new_data = []
        if (len(top) > 0):
            for item in top:
                new_data.append({'key': item[0], 'value': item[1]})
        return new_data

    def stop(self):
        self._stop_event.set()


    def run(self):
        consumer = KafkaConsumer(bootstrap_servers=[KAFKA_URL], api_version=(0,10),
                                 auto_offset_reset='earliest', enable_auto_commit=False, consumer_timeout_ms=60000)
        consumer.subscribe(['newtweet'])
        while(True):
            for message in consumer:
                self.count = self.count+1
                requests.post(APP_URL+'tweet-count', data=str(self.count))#message.value)
                requests.post(APP_URL+'notify', message.value)

                tweet = str(message.value, encoding='utf-8')
                hastag = self.extract_hash_tags(tweet)
                self.update_trend(hastag)
                top_10 = self.getTopNhashags(10)
                requests.post(APP_URL + 'trending-hashtag', json=json.dumps(top_10))

    def stop(self):
        self._stop_event.set()


class SentimentConsumer(threading.Thread):

    def run(self):
        consumer = KafkaConsumer(bootstrap_servers=[KAFKA_URL], api_version=(0,10),
                                 auto_offset_reset='earliest', enable_auto_commit=False, consumer_timeout_ms=60000)
        consumer.subscribe(['newtweet'])
        while(True):
            for message in consumer:
                self.count = self.count+1
                requests.post(APP_URL+'tweet-count', data=str(self.count))#message.value)
                requests.post(APP_URL+'notify', message.value)

    def stop(self):
        self._stop_event.set()