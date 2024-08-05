import threading
import time
from kafka import KafkaProducer, KafkaConsumer

# write a program using kafka client to publish messages at an interval and consume those messages from kafka
# Kafka broker address
bootstrap_servers = 'localhost:9092'

# Topic name
topic = 'my_topic'

# Create Kafka producer
producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

# Create Kafka consumer
consumer = KafkaConsumer(topic, bootstrap_servers=bootstrap_servers)

# Publish messages at an interval
def publish_messages():
  while True:
    message = input("Enter a message to publish (or 'q' to quit): ")
    if message == 'q':
      break
    producer.send(topic, message.encode())
    print("Message published successfully")
    time.sleep(1)

# Consume messages
def consume_messages():
  for message in consumer:
    print(f"Received message: {message.value.decode()}")

# Start publishing messages in a separate thread
publish_thread = threading.Thread(target=publish_messages)
publish_thread.start()

# Consume messages
consume_messages()