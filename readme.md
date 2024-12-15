# Django Kafka Consumer Projects

This repository contains multiple Django-based Kafka consumer applications and a main service for managing Kafka topics and messages.

## Project Structure

The project is organized into three main components:

### kafka-consumer-1

A Django application implementing a Kafka consumer with configuration support.

```
kafka-consumer-1/
├── consumer/           # Django project settings
├── kafka_app/         # Main consumer application
│   ├── consumer.py    # Kafka consumer implementation
│   ├── configs.py     # Configuration settings
│   └── management/
│       └── commands/
│           └── run_kafka_consumer.py
└── manage.py
```

### kafka-consumer-2

A secondary consumer implementation with similar structure.

```
kafka-consumer-2/
├── consumer/
├── kafka_app/
│   └── management/
│       └── commands/
│           └── run_kafka_consumer.py
└── manage.py
```

### kafka-main-service

The main service for managing Kafka topics and producing messages.

```
kafka-main-service/
├── kafka_core/
│   ├── kafka_utils.py   # Kafka management utilities
│   └── views.py         # API endpoints
├── main_service/
└── manage.py
```

## Features

- Multiple independent Kafka consumers
- Django management commands for running consumers
- REST API for managing Kafka topics and messages
- Configurable consumer groups and topics
- Support for message filtering by key
- Offset management and tracking

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd kafka-project
```

2. Set up virtual environments and install dependencies for each service:

For kafka-consumer-1:

```bash
cd kafka-consumer-1
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

Repeat the same process for kafka-consumer-2 and kafka-main-service.

## Usage

### Running the Consumers

To start the first consumer:

```bash
cd kafka-consumer-1
python manage.py run_kafka_consumer [--key <message-key>]
```

To start the second consumer:

```bash
cd kafka-consumer-2
python manage.py run_kafka_consumer [--key <message-key>]
```

### Managing Kafka Topics

The main service provides REST APIs for:

- Creating topics
- Deleting topics
- Producing messages
- Listing topics

Start the main service:

```bash
cd kafka-main-service
python manage.py runserver
```

## API Endpoints

### Topic Management

- `GET /api/topics/` - List all topics
- `POST /api/topics/` - Create a new topic
- `DELETE /api/topics/{topic_name}/` - Delete a topic

### Message Production

- `POST /api/produce/` - Produce messages to a topic

## Configuration

Each consumer can be configured through their respective

configs.py

files:

- Bootstrap servers
- Consumer group IDs
- Topic subscriptions
- Message serialization/deserialization
- Security settings

## Requirements

- Python 3.8+
- Django 3.2+
- kafka-python-ng
- Additional dependencies listed in requirements.txt

## License

This project is licensed under the Apache License 2.0.
