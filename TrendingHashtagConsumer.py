import json
import threading
import requests
from kafka import KafkaConsumer
from keys import KAFKA_URL, APP_URL


class TrendingHashtagConsumer(threading.Thread):
    '''This class is responsible to consume message from kafka to find trending hashtags'''



    def run(self):
        consumer = KafkaConsumer(bootstrap_servers=[KAFKA_URL], api_version=(0, 10),
                                 auto_offset_reset='earliest', enable_auto_commit=False, consumer_timeout_ms=60000)
        consumer.subscribe(['newtweet'])

        while(True):
            for message in consumer:
                tweet = str(message.value, encoding='utf-8')
                hastag = self.extract_hash_tags(tweet)
                self.update_trend(hastag)
                top_10 = self.getTopNhashags(10)
                requests.post(APP_URL+'trending-hashtag', json = json.dumps(top_10))

