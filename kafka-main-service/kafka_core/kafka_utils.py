from django.conf import settings
from kafka.admin import KafkaAdminClient, NewTopic
from kafka import KafkaProducer
import json

class KafkaUtils:
    def __init__(self):
        self.admin_client = KafkaAdminClient(
            bootstrap_servers=settings.KAFKA_CONFIG['BOOTSTRAP_SERVERS'],
            client_id=settings.KAFKA_CONFIG['CLIENT_ID']
        )
        self.producer = KafkaProducer(
            bootstrap_servers=settings.KAFKA_CONFIG['BOOTSTRAP_SERVERS'],
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )

    def create_topic(self, topic_name, num_partitions=1, replication_factor=1):
        topic = NewTopic(
            name=topic_name,
            num_partitions=num_partitions,
            replication_factor=replication_factor
        )
        return self.admin_client.create_topics([topic])

    def delete_topic(self, topic_name):
        return self.admin_client.delete_topics([topic_name])

    def list_topics(self):
        return self.admin_client.list_topics()

    def produce_message(self, topic, message, key=None, partition=None):
        future = self.producer.send(
            topic=topic,
            value=message,
            key=key.encode() if key else None,
            partition=partition
        )
        self.producer.flush()
        metadata = future.get(timeout=60)
        return {
            'topic': metadata.topic,
            'partition': metadata.partition,
            'offset': metadata.offset
        }
    def produce_message_to_all_partitions(self, topic, message, key=None):
        partitions = self.get_partitions_for_topic(topic)
        if partitions is None:
            raise ValueError(f"Topic {topic} does not exist or has no partitions")

        results = []
        for partition in partitions:
            result = self.produce_message(topic, message, key=key, partition=partition)
            results.append(result)
            print(f"Message sent to partition {result['partition']} with offset {result['offset']}")

        return {
            'topic': topic,
            'partitions': list(partitions),
            'results': results
        }