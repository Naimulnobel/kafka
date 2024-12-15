from django.urls import path
from .views import TopicManagementView, MainProducerView

urlpatterns = [
    path('topics/', TopicManagementView.as_view(), name='topics'),
    path('topics/<str:topic_name>/', TopicManagementView.as_view(), name='topic-detail'),
    path('produce/', MainProducerView.as_view(), name='produce'),
]