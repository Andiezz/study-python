from ast import Dict
from typing import Optional
from api.configuration.kafka_config import KafkaConfig
from api.exception.service_exception import ServiceException
from confluent_kafka import Producer, Consumer, KafkaError, KafkaException

"""
Author : Neda Peyrone
Create Date : 30-08-2023
File : kafka_connector.py
"""


class KafkaConnector:
    def __init__(self, config: Optional[KafkaConfig]):
        self.config = config

    def error_callback(self, err: KafkaError):
        raise ServiceException(err.str())

    def __get_producer(self, conf: Optional[Dict] = None) -> Producer:
        default_conf = {
            "bootstrap.servers": self.config.bootstrap_servers,
            "retries": 0,
            "error_cb": self.error_callback,
        }
        if conf:
            default_conf.update(conf)

        return Producer(default_conf)

    def produce(self, topic, message, conf: Optional[Dict] = None):
        producer = self.__get_producer(conf)
        producer.produce(topic, message)
        producer.flush()

    def __get_consumer(self, group_id, topics, conf: Optional[Dict] = None) -> Consumer:
        default_conf = {
            "bootstrap.servers": self.config.bootstrap_servers,
            "group.id": group_id,
            "auto.offset.reset": self.config.auto_offset_reset,
            "enable.auto.commit": True,
        }

        if conf:
            default_conf.update(conf)

        try:
            consumer = Consumer(default_conf)
            consumer.subscribe(topics)
            return consumer
        except KafkaException as err:
            raise ServiceException(
                f'Error while consuming message: "{err.args[0].str()}."'
            )

    def consume(
        self, group_id: str, topic: str, timeout=10.0, conf: Optional[Dict] = None
    ):
        consumer = self.__get_consumer(group_id, [topic], conf)
        msg = consumer.poll(timeout)  # Pull a message takes as much as 10 seconds
        consumer.close()  # Close the consumer

        if msg is None:
            raise ServiceException(
                "Error consuming a message that does not have a message part."
            )
        elif not msg.error():
            return msg.value().decode("utf-8")
        elif msg.error().code() == KafkaError._PARTITION_EOF:
            raise ServiceException(
                f"End of partition reached {msg.topic()}/{msg.partition()}."
            )
        else:
            raise ServiceException(
                f"Error while consuming message: {(msg.error().str())}."
            )
