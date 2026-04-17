from rest_framework import viewsets, permissions
from .models import HRQuestion, GDTopic
from .serializers import HRQuestionSerializer, GDTopicSerializer


class HRQuestionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing HR questions.
    
    Actions:
    - list: GET /api/hr-questions/ - List all HR questions
    - retrieve: GET /api/hr-questions/{id}/ - Get HR question details
    """
    queryset = HRQuestion.objects.all()
    serializer_class = HRQuestionSerializer
    permission_classes = [permissions.AllowAny]


class GDTopicViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing GD topics.
    
    Actions:
    - list: GET /api/gd-topics/ - List all GD topics
    - retrieve: GET /api/gd-topics/{id}/ - Get GD topic details
    """
    queryset = GDTopic.objects.all()
    serializer_class = GDTopicSerializer
    permission_classes = [permissions.AllowAny]
