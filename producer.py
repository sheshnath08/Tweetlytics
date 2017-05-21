from kafka import KafkaProducer
from keys import KAFKA_URL

class Producer:
    producer = KafkaProducer(bootstrap_servers=KAFKA_URL, api_version=(0, 10))
    def send_tweet(self, topic, msg):
        self.producer.send(topic,value=msg.encode())