from kafka import KafkaProducer

class Producer:
    producer = KafkaProducer(bootstrap_servers='52.87.152.11:9092', api_version=(0, 10))
    def send_tweet(self, topic, msg):
        self.producer.send(topic,value=msg.encode())