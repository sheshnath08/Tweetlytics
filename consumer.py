from kafka import KafkaConsumer

# To consume messages
consumer = KafkaConsumer('test',bootstrap_servers=['ec2-52-23-192-153.compute-1.amazonaws.com'],api_version=(0,10,1))

for msg in consumer:
    print(msg)