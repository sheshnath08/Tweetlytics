import threading
import requests
from kafka import KafkaConsumer
from keys import KAFKA_URL, APP_URL

class Consumer(threading.Thread):
    '''This is kafka consumer to show tweets and count'''
    count = 0

    def run(self):
        consumer = KafkaConsumer(bootstrap_servers=[KAFKA_URL], api_version=(0,10),
                                 auto_offset_reset='earliest', enable_auto_commit=False, consumer_timeout_ms=60000)
        consumer.subscribe(['newtweet'])
        while(True):
            for message in consumer:
                self.count = self.count+1
                requests.post(APP_URL+'tweet-count', data=str(self.count))#message.value)
                requests.post(APP_URL+'notify', message.value)
                requests.post(APP_URL+'trending-hashtag', message)

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