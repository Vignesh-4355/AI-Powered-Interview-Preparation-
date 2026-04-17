from rest_framework import serializers
from .models import ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    """Serializer for Chat Message"""

    class Meta:
        model = ChatMessage
        fields = ['id', 'user', 'message', 'response', 'category', 'timestamp', 'session_id']
        read_only_fields = ['id', 'timestamp', 'response', 'category']


class ChatRequestSerializer(serializers.Serializer):
    """Serializer for chat request"""
    message = serializers.CharField(max_length=1000)
    session_id = serializers.CharField(max_length=100, required=False)
