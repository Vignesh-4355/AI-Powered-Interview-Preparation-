from rest_framework import serializers
from .models import InterviewQuestion, MockInterviewSession, UserAnswer


class InterviewQuestionSerializer(serializers.ModelSerializer):
    question_type_display = serializers.CharField(source='get_question_type_display', read_only=True)
    difficulty_display = serializers.CharField(source='get_difficulty_display', read_only=True)

    class Meta:
        model = InterviewQuestion
        fields = [
            'id', 'question_text', 'question_type', 'question_type_display',
            'difficulty', 'difficulty_display', 'expected_keywords',
            'model_answer', 'created_at'
        ]
        read_only_fields = ['created_at']


class UserAnswerSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(source='question.question_text', read_only=True)
    question_type = serializers.CharField(source='question.question_type', read_only=True)

    class Meta:
        model = UserAnswer
        fields = [
            'id', 'session', 'question', 'question_text', 'question_type',
            'answer_text', 'timestamp', 'keyword_score', 'feedback'
        ]
        read_only_fields = ['timestamp', 'keyword_score', 'feedback']


class MockInterviewSessionSerializer(serializers.ModelSerializer):
    interview_type_display = serializers.CharField(source='get_interview_type_display', read_only=True)
    difficulty_display = serializers.CharField(source='get_difficulty_display', read_only=True)
    answers_count = serializers.SerializerMethodField()

    class Meta:
        model = MockInterviewSession
        fields = [
            'id', 'user', 'interview_type', 'interview_type_display',
            'difficulty', 'difficulty_display', 'total_questions',
            'start_time', 'end_time', 'is_completed', 'score', 'feedback',
            'answers_count'
        ]
        read_only_fields = ['user', 'start_time', 'end_time', 'is_completed', 'score', 'feedback']

    def get_answers_count(self, obj):
        return obj.answers.count()


class SessionDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for session with answers"""
    interview_type_display = serializers.CharField(source='get_interview_type_display', read_only=True)
    difficulty_display = serializers.CharField(source='get_difficulty_display', read_only=True)
    answers = UserAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = MockInterviewSession
        fields = [
            'id', 'user', 'interview_type', 'interview_type_display',
            'difficulty', 'difficulty_display', 'total_questions',
            'start_time', 'end_time', 'is_completed', 'score', 'feedback',
            'answers'
        ]
