from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class QuestionListAPI(generics.ListAPIView):
    
		queryset = Question.objects.all()
    
		serializer_class = QuestionSerializer
    
		permission_classes = [IsAuthenticated]  
		
		@action(detail=False, methods=['GET'])
    
		def custom_action(self, request):
        
				user = request.user  
        
				questions = Question.objects.filter(Q(id_set__id__gt=3), user=user)
        
				serializer = self.get_serializer(questions, many=True)
        
				return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionDetailAPI(generics.RetrieveUpdateDestroyAPIView):
	queryset = Question.objects.all()
	serializer_class = QuestionSerializer

class AnswerListAPI(generics.ListAPIView,generics.CreateAPIView, generics.DestroyAPIView):
	queryset = Answer.objects.all()
	serializer_class = AnswerSerializer

