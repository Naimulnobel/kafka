from rest_framework.views import APIView
from rest_framework.response import Response
from .kafka_utils import KafkaUtils
from django.core.serializers.json import DjangoJSONEncoder
import json
from .models import *
from django.forms.models import model_to_dict
class TopicManagementView(APIView):
    def __init__(self):
        self.kafka = KafkaUtils()

    def get(self, request):
        topics = self.kafka.list_topics()
        return Response({'topics': topics})

    def post(self, request):
        topic_name = request.data.get('topic_name')
        num_partitions = request.data.get('num_partitions', 1)      
        self.kafka.create_topic(topic_name,int(num_partitions))
        return Response({'message': f'Topic {topic_name} created'})

    def delete(self, request, topic_name):
        self.kafka.delete_topic(topic_name)
        return Response({'message': f'Topic {topic_name} deleted'})

class MainProducerView(APIView):
    def __init__(self):
        self.kafka = KafkaUtils()

    def post(self, request):
        try:
            # Validate JSON format
            if not request.content_type == 'application/json':
                return Response({
                    'error': 'Content-Type must be application/json'
                }, status=400)

            topic = request.data.get('topic')
            message = request.data.get('message')
            key = request.data.get('key', None)
            partition = request.data.get('partition', None)
            
            # Log request data for debugging
            print(f"Request data: {request.data}")
            
            # Validate required fields
            if not topic or not message:
                return Response({
                    'error': 'Both topic and message are required'
                }, status=400)

            # Validate message structure
            if not isinstance(message, dict):
                return Response({
                    'error': 'Message must be a JSON object with sn and description fields'
                }, status=400)
                
            # Validate required device fields
            if 'sn' not in message or 'description' not in message:
                return Response({
                    'error': 'Message must contain sn and description fields'
                }, status=400)
                
            # Create device
            device = Device.objects.create(
                sn=message['sn'],
                description=message['description']
            )
            
            # Convert device to serializable dict
            device_data = model_to_dict(device)
            
            # Send to Kafka
            response = self.kafka.produce_message(topic, message, key=key, partition=partition)
            
            return Response({
                'status': 'success',
                'message': response,
                'topic': topic,
                'device': device_data,
                'partition': response['partition'],
                'offsets':response['offset']
            })
            
        except json.JSONDecodeError as e:
            return Response({
                'error': 'Invalid JSON format',
                'details': str(e)
            }, status=400)
        except Exception as e:
            return Response({
                'error': str(e),
                'details': 'Failed to process message'
            }, status=400)
    
    class BroadcastMessageView(APIView):
        def __init__(self):
            self.kafka = KafkaUtils()

        def post(self, request):
            topic = request.data.get('topic')
            message = request.data.get('message')
            key = request.data.get('key', None)
            
            # Log request data for debugging
            print(f"Request data: {request.data}")
            
            # Validate required fields
            if not topic or not message:
                return Response({
                    'error': 'Both topic and message are required'
                }, status=400)

            try:
                # Send to Kafka
                response = self.kafka.produce_message_to_all_partitions(topic, message, key=key)
                
                return Response({
                    'status': 'success',
                    'message': response,
                    'topic': topic,
                    'partitions': response['partitions']
                })
                
            except Exception as e:
                return Response({
                    'error': str(e),
                    'details': 'Failed to process message'
                }, status=400)