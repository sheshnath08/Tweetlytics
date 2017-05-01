# from kafka.conn import log
#
# from kafka import KafkaProducer
# from kafka.errors import KafkaError
#
# producer = KafkaProducer(bootstrap_servers='ec2-52-23-192-153.compute-1.amazonaws.com', api_version=(0,10))
#
# # Asynchronous by default
# future = producer.send('newtweet', b'test')
#
# # Block for 'synchronous' sends
# try:
#     record_metadata = future.get(timeout=10)
# except KafkaError:
#     # Decide what to do if produce request failed...
#     log.exception()
#     pass
#
# # Successful result returns assigned partition and offset
# print (record_metadata.topic)
# print (record_metadata.partition)
# print (record_metadata.offset)
#
# # # produce keyed messages to enable hashed partitioning
# # print(producer.send('newtweet', key=b'foo', value=b'bar'))
#
# # block until all async messages are sent
# producer.flush()
#
# # configure multiple retries
# producer = KafkaProducer(retries=5)

import threading, logging, time

from kafka import KafkaConsumer, KafkaProducer


class Producer(threading.Thread):
    daemon = True

    def run(self):
        producer = KafkaProducer(bootstrap_servers='http://52.23.192.153:9029', api_version=(0,10))
        print(producer.metrics())
        while True:
            print('sending msg')
            producer.send('newtweet', b"test")
            producer.send('newtweet', b"\xc2Hola, mundo!")
            time.sleep(1)


class Consumer(threading.Thread):
    daemon = True

    def run(self):
        consumer = KafkaConsumer(bootstrap_servers='http://52.23.192.153:9029', api_version=(0,10),
                                 auto_offset_reset='earliest')
        consumer.subscribe(['newtweet'])

        for message in consumer:
            print ("msg:", message)


def main():
    threads = [
        Producer(),
        Consumer()
    ]

    for t in threads:
        t.start()

    time.sleep(10)

if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO
        )
main()