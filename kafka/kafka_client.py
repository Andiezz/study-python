import time
import json
import threading
from kafka import KafkaProducer, KafkaConsumer


class KafkaClient:
    def __init__(self, server):
        self.server = server
        self.producer = KafkaProducer(
            bootstrap_servers=self.server,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        self.consumer = KafkaConsumer(
            bootstrap_servers=self.server,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        )

    def send_message(self, topic, message):
        self.producer.send(topic, message)
        self.producer.flush()

    def consume_messages(self, topic):
        self.consumer.subscribe([topic])
        for message in self.consumer:
            print(message.value)


kafka_client = KafkaClient("localhost:9092")


def publish_messages():
    while True:
        message = input("Enter a message to publish (or 'q' to quit): ")
        if message == "q":
            break
        kafka_client.send_message("my_topic", {"message": message})
        print("Message published successfully")
        time.sleep(1)


# Start publishing messages in a separate thread
publish_thread = threading.Thread(target=publish_messages)
publish_thread.start()

def process_message(message):
    print(message)


for message in kafka_client.consume_messages("my_topic"):
    process_message(message)
