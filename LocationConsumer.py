import threading
import requests
from kafka import KafkaConsumer
from keys import KAFKA_URL

class LocationConsumer(threading.Thread):
    '''[Working on it] This class is kafka-consumer to consume messages and plot it on map'''

    def run(self):
        while(True):
            consumer = KafkaConsumer(bootstrap_servers=[KAFKA_URL], api_version=(0,10),
                                     auto_offset_reset='begining', consumer_timeout_ms=600000)
            consumer.subscribe(['location'])
            print(consumer.fetch_messages())
            while(True):
                print('location consumer')
                for message in consumer:
                    print(message)
                    requests.post('http://localhost:5000/notify', message.value)

    def stop(self):
        self._stop_event.set()