# kafka_app/management/commands/run_kafka_consumer.py

from django.core.management.base import BaseCommand
from kafka_app.consumer import KafkaConsumerService
from kafka_app.configs import KAFKA_CONFIGS, KAFKA_TOPICS

class Command(BaseCommand):
    help = 'Start the Kafka consumer service'

    def add_arguments(self, parser):
        parser.add_argument('--key', type=str, help='Key to filter messages', required=False)

    def handle(self, *args, **options):
        key_filter = options.get('key')

        if key_filter:
            self.stdout.write(self.style.SUCCESS(f'Starting Kafka consumer for key: {key_filter}...'))
        else:
            self.stdout.write(self.style.SUCCESS('Starting Kafka consumer without key filtering...'))
        
        consumer = KafkaConsumerService(KAFKA_CONFIGS, KAFKA_TOPICS, key_filter)
        try:
            consumer.connect()
            consumer.consume()
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('Stopping consumer...'))
            consumer.stop()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
            consumer.stop()