from .models import *
from rest_framework import serializers

class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = '__all__'

    def validate_content(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Длина контента должна быть не менее 10 символов.")
        return value

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question	
        fields = ['id', 'title', 'content', 'created_at']