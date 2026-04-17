from rest_framework import serializers
from .models import HRQuestion, GDTopic


class HRQuestionSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = HRQuestion
        fields = '__all__'


class GDTopicSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = GDTopic
        fields = '__all__'
