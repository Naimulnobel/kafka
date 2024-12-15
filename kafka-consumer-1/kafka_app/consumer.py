# kafka_app/consumer.py

from kafka import KafkaConsumer,TopicPartition, OffsetAndMetadata
import json
import logging
from typing import Dict, List, Any, Optional
from .models import Device

logger = logging.getLogger(__name__)

class KafkaConsumerService:
    def __init__(self, configs: Dict[str, Any], topics: List[str], key_filter: Optional[str] = None):
        self.configs = configs
        self.topics = topics
        self.key_filter = key_filter
        self.consumer = None
        self.running = True

    def connect(self) -> None:
        """Initialize Kafka consumer connection"""
        try:
            self.consumer = KafkaConsumer(
                *self.topics,
                **self.configs,
                key_deserializer=lambda x: x.decode('utf-8') if x else None,
                value_deserializer=lambda x: json.loads(x.decode('utf-8'))
            )
            logger.info(f"Subscribed to topics: {self.topics}")
        except Exception as e:
            logger.error(f"Failed to connect to Kafka: {str(e)}")
            raise

    def consume(self) -> None:
        """Main consumption loop"""
        try:
            for message in self.consumer:
                if not self.running:
                    break
                
                if self.key_filter is None or message.key == self.key_filter:
                    try:
                        self._process_message(message)
                    except Exception as e:
                        logger.error(f"Error processing message: {str(e)}")
                        continue
                
        except Exception as e:
            logger.error(f"Consumer error: {str(e)}")
        finally:
            self.stop()

    def _process_message(self, message) -> None:
        """Process individual Kafka messages"""
        try:
            logger.info(f"Processing message from topic {message.topic}, partition {message.partition}, key {message.key}")
            self._handle_message(message.value)
        except Exception as e:
            logger.error(f"Failed to process message: {str(e)}")

    def _handle_message(self, data: Dict[str, Any]) -> None:
        """Handle the processed message"""
        # Implement your business logic here
        logger.info(f"Received data: {data}")
        # For example, you can save the data to a database
        # data1 = {
        #     "id": data["id"],
        #     "sn": data["sn"],
        #     "description": data["description"],
        #     "status": data["status"]
        # }
        # device = Device.objects.create(**data1)
        # logger.info(f"Device {device} created")

    def stop(self) -> None:
        """Stop the consumer"""
        self.running = False
        if self.consumer:
            self.consumer.close()
            logger.info("Consumer closed")
    def get_offsets(self) -> Dict[TopicPartition, OffsetAndMetadata]:
        """Fetch the current consumer group offsets"""
        offsets = {}
        for topic in self.topics:
            partitions = self.consumer.partitions_for_topic(topic)
            for partition in partitions:
                tp = TopicPartition(topic, partition)
                offset = self.consumer.committed(tp)
                offsets[tp] = offset
        return offsets