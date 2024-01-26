from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters import rest_framework as filters
from rest_framework import generics
from .models import Question
from .serializers import QuestionSerializer
from django.db.models import Q 
from rest_framework.viewsets import ModelViewSet


class QuestionListAPI(ModelViewSet):
    
    queryset = Question.objects.all()
    
    serializer_class = QuestionSerializer
    
    permission_classes = [IsAuthenticated]  
    
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['id', 'title']
    ordering_fields = ['id', 'title', 'created_at']
    filterset_fields = ['id','title']


    @action(detail=True, methods=['POST'])
    def mark_as_favorite(self, request, pk):
        question = self.get_object()
        question.is_favorite = True
        question.save()

        serializer = self.get_serializer(question)
        return Response(serializer.data)
        
    @action(detail=False, methods=['GET'])
    def filter_question(self, request):
        search_query = request.GET.get('title')
        queryset = self.get_queryset()
        
        queryset = queryset.filter(
            Q(content__startswith="К") |
            Q(content__endswith="?") &
            ~Q(title__icontains="django")
        )
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class QuestionDetailAPI(ModelViewSet):
  queryset = Question.objects.all()
  serializer_class = QuestionSerializer

class AnswerListAPI(ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['id','content','author']
    ordering_fields = ['id', 'content', 'created_at']
    filterset_fields = ['content']
  

    @action(detail=True, methods=['POST'])
    def create_answer(self, request, pk):
        question = self.get_object(pk=pk)
        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(question=question)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
