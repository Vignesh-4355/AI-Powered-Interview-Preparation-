from rest_framework import serializers
from .models import CodingQuestion, UserProgress


class CodingQuestionSerializer(serializers.ModelSerializer):
    """Serializer for Coding Question"""
    difficulty_display = serializers.CharField(source='get_difficulty_display', read_only=True)
    topic_display = serializers.CharField(source='get_topic_display', read_only=True)
    is_solved = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()

    class Meta:
        model = CodingQuestion
        fields = [
            'id', 'title', 'description', 'difficulty', 'difficulty_display',
            'topic', 'topic_display', 'sample_input', 'sample_output',
            'explanation', 'youtube_link', 'constraints', 'test_cases',
            'created_at', 'updated_at', 'is_solved', 'is_bookmarked'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_is_solved(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            progress = UserProgress.objects.filter(
                user=request.user, 
                question=obj, 
                is_solved=True
            ).first()
            return progress is not None
        return False

    def get_is_bookmarked(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            progress = UserProgress.objects.filter(
                user=request.user, 
                question=obj, 
                is_bookmarked=True
            ).first()
            return progress is not None
        return False


class CodingQuestionListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for coding question list"""
    difficulty_display = serializers.CharField(source='get_difficulty_display', read_only=True)
    topic_display = serializers.CharField(source='get_topic_display', read_only=True)
    is_solved = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()

    class Meta:
        model = CodingQuestion
        fields = [
            'id', 'title', 'difficulty', 'difficulty_display',
            'topic', 'topic_display', 'created_at',
            'is_solved', 'is_bookmarked'
        ]
        read_only_fields = ['id', 'created_at']

    def get_is_solved(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            progress = UserProgress.objects.filter(
                user=request.user, 
                question=obj, 
                is_solved=True
            ).first()
            return progress is not None
        return False

    def get_is_bookmarked(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            progress = UserProgress.objects.filter(
                user=request.user, 
                question=obj, 
                is_bookmarked=True
            ).first()
            return progress is not None
        return False


class UserProgressSerializer(serializers.ModelSerializer):
    """Serializer for User Progress"""
    question_title = serializers.CharField(source='question.title', read_only=True)
    question_difficulty = serializers.CharField(source='question.difficulty', read_only=True)
    question_topic = serializers.CharField(source='question.topic', read_only=True)

    class Meta:
        model = UserProgress
        fields = [
            'id', 'question', 'question_title', 'question_difficulty',
            'question_topic', 'is_solved', 'is_bookmarked', 'attempts',
            'last_attempted_at', 'solved_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
