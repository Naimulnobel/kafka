

KAFKA_CONFIGS = {
    'bootstrap_servers': ['localhost:9092'],
    'group_id': 'django_consumer_group1',
    'auto_offset_reset': 'earliest',
    'enable_auto_commit': True,
    'max_poll_interval_ms': 300000,
    'session_timeout_ms': 30000
}

KAFKA_TOPICS = ['iot-devices']