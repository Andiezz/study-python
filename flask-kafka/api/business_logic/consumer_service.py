from api.domain.consumer import Consumer
from api.constant.message_code import MessageCode
from api.configuration.app_config import AppConfig
from api.configuration.kafka_config import KafkaConfig
from api.connector.kafka_connector import KafkaConnector
from api.exception.service_exception import ServiceException

"""
Author : Neda Peyrone
Create Date : 30-08-2023
File : consumer_service.py
"""


class ConsumerService:
    def __init__(self):
        self.__load_params()
        self.connector = KafkaConnector(self.cfg)

    def __load_params(self):
        appConfig = AppConfig()
        self.cfg = KafkaConfig(
            appConfig.params["kafka"]["bootstrap_servers"],
            appConfig.params["kafka"]["auto_offset_reset"],
        )

    def consume(self, consumer: Consumer):
        action = "consume"
        print(f"I:--START--:--{action}--")
        try:
            msg = self.connector.consume(
                consumer.group_id, consumer.topic, conf=consumer.config
            )
            print(f"O:--SUCCESS--:--{action}--:msg/{msg}")
            return msg
        except Exception as err:
            self.__handle_error(action, err)

    def __handle_error(self, action, err):
        dir(err)
        desc = MessageCode.UNKNOWN_ERROR.value if len(err.args) == 0 else err.args[0]
        print(f"O:--FAIL--:--{action}--:errorDesc/{desc}")
        raise ServiceException(desc)
