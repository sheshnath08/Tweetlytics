import json
import threading
import requests
from kafka import KafkaConsumer
from keys import KAFKA_URL
class TrendingHashtagConsumer(threading.Thread):

    trend = {}

    def run(self):
        consumer = KafkaConsumer(bootstrap_servers=[KAFKA_URL], api_version=(0,10),
                                 auto_offset_reset='earliest', enable_auto_commit=False, consumer_timeout_ms=60000)
        consumer.subscribe(['newtweet'])
        while(True):
            for message in consumer:
                tweet = str(message.value, encoding='utf-8')
                hastag = self.extract_hash_tags(tweet)
                self.update_trend(hastag)
                top_10 = self.getTopNhashags(10)
                requests.post('http://localhost:5000/trending-hashtag', json = json.dumps(top_10))

    def extract_hash_tags(self, s):
        s = s.lower()
        return set(part[1:] for part in s.split() if part.startswith('#'))

    def update_trend(self, hashtag):
        keys = self.trend.keys()
        for item in hashtag:
            if(len(item)<3):
                continue
            if item in keys:
                self.trend[item] = self.trend[item]+1
            else:
                self.trend[item] = 1

    def getTopNhashags(self,n):
        if(len(self.trend)>=n):
            top = sorted(self.trend.items(), key=lambda x:x[1], reverse=True)[:n]
        else:
            top = sorted(self.trend.items(), key=lambda x: x[1], reverse=True)

        return top

    def stop(self):
        self._stop_event.set()