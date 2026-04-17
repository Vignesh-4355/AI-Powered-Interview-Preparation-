from rest_framework import serializers
from .models import Company, CompanyInterviewPattern, CompanyQuestion


class CompanyInterviewPatternSerializer(serializers.ModelSerializer):
    """Serializer for Company Interview Pattern"""
    round_name_display = serializers.CharField(source='get_round_name_display', read_only=True)

    class Meta:
        model = CompanyInterviewPattern
        fields = ['id', 'round_name', 'round_name_display', 'description', 'duration', 'order']
        read_only_fields = ['id']


class CompanyQuestionSerializer(serializers.ModelSerializer):
    """Serializer for Company Questions"""
    question_type_display = serializers.CharField(source='get_question_type_display', read_only=True)
    difficulty_display = serializers.CharField(source='get_difficulty_display', read_only=True)

    class Meta:
        model = CompanyQuestion
        fields = [
            'id', 'question', 'question_type', 'question_type_display',
            'answer', 'youtube_link', 'difficulty', 'difficulty_display',
            'tags', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class CompanySerializer(serializers.ModelSerializer):
    """Serializer for Company with related data"""
    interview_patterns = CompanyInterviewPatternSerializer(many=True, read_only=True)
    questions = CompanyQuestionSerializer(many=True, read_only=True)
    questions_count = serializers.SerializerMethodField()
    difficulty_display = serializers.CharField(source='get_difficulty_level_display', read_only=True)
    hiring_frequency_display = serializers.CharField(source='get_hiring_frequency_display', read_only=True)

    class Meta:
        model = Company
        fields = [
            'id', 'name', 'description', 'logo', 'website', 'industry',
            'difficulty_level', 'difficulty_display', 'hiring_frequency',
            'hiring_frequency_display', 'total_questions',
            'interview_patterns', 'questions', 'questions_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_questions_count(self, obj):
        return obj.questions.count()


class CompanyListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for company list"""
    difficulty_display = serializers.CharField(source='get_difficulty_level_display', read_only=True)
    hiring_frequency_display = serializers.CharField(source='get_hiring_frequency_display', read_only=True)
    
    class Meta:
        model = Company
        fields = [
            'id', 'name', 'description', 'logo', 'industry',
            'difficulty_level', 'difficulty_display',
            'hiring_frequency', 'hiring_frequency_display',
            'total_questions'
        ]
        read_only_fields = ['id']
