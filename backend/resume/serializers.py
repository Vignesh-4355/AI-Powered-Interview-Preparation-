from rest_framework import serializers
from .models import Resume, ResumeAnalysis


class ResumeAnalysisSerializer(serializers.ModelSerializer):
    """Serializer for Resume Analysis"""
    class Meta:
        model = ResumeAnalysis
        fields = '__all__'


class ResumeSerializer(serializers.ModelSerializer):
    """Serializer for Resume with analysis"""
    analysis = ResumeAnalysisSerializer(read_only=True)
    file_size_mb = serializers.SerializerMethodField()

    class Meta:
        model = Resume
        fields = ['id', 'user', 'file', 'original_filename', 'uploaded_at', 
                  'file_size', 'file_size_mb', 'extracted_text', 'analysis']
        read_only_fields = ['user', 'extracted_text', 'file_size']

    def get_file_size_mb(self, obj):
        return round(obj.file_size / (1024 * 1024), 2)
