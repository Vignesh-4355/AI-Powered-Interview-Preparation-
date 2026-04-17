from rest_framework import serializers
from .models import UserProgress


class UserProgressSerializer(serializers.ModelSerializer):
    """Serializer for User Progress"""
    coding_accuracy = serializers.ReadOnlyField()
    aptitude_accuracy = serializers.ReadOnlyField()

    class Meta:
        model = UserProgress
        fields = '__all__'


class DetailedAnalyticsSerializer(serializers.Serializer):
    """Serializer for detailed analytics response"""
    progress = UserProgressSerializer()
    coding_stats = serializers.DictField()
    aptitude_stats = serializers.DictField()
    mock_interview_stats = serializers.DictField()
    company_prep_stats = serializers.DictField()
    roadmap_stats = serializers.DictField()
    recent_activity = serializers.ListField()
