from rest_framework import serializers
from .models import AptitudeQuestion, UserAttempt


class AptitudeQuestionSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    difficulty_display = serializers.CharField(source='get_difficulty_display', read_only=True)

    class Meta:
        model = AptitudeQuestion
        fields = '__all__'


class AptitudeQuestionListSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    difficulty_display = serializers.CharField(source='get_difficulty_display', read_only=True)

    class Meta:
        model = AptitudeQuestion
        fields = ['id', 'question', 'category', 'category_display', 'difficulty', 'difficulty_display', 'options']


class UserAttemptSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(source='question.question', read_only=True)
    question_category = serializers.CharField(source='question.category', read_only=True)

    class Meta:
        model = UserAttempt
        fields = ['id', 'question', 'question_text', 'question_category', 'selected_answer', 'is_correct', 'time_taken', 'attempted_at']
