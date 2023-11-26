from .models import *
from rest_framework import serializers
from django.db.models import Q 

class AnswerSerializer(serializers.ModelSerializer):
    def validate_content(self, value):

        if len(value) < 10:
            raise serializers.ValidationError("Длина content должна быть не менее 10 символов.")
        return value
    
    class Meta:
        model = Answer
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Question
		fields = '__all__'
