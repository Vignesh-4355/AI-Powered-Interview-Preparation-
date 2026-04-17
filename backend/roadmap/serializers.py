from rest_framework import serializers
from .models import RoadmapItem


class RoadmapItemSerializer(serializers.ModelSerializer):
    """Serializer for Roadmap Item"""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = RoadmapItem
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
