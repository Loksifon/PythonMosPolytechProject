from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404

from .forms import RegistrationForm, CommentForm, QuestionForm, AnswerForm
from django.contrib.auth import authenticate, login
from .models import Question, Tag, User, Comment, Category, Answer
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views import View
from .forms import RegistrationForm, CommentForm, QuestionForm, AnswerForm
from .models import Question, Tag, User, Comment, Category, Answer
from django.views.generic import TemplateView
from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import QuestionSerializer

class SignupView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
        else:
            return render(request, 'signup.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('questionList')
        else:
            return render(request, 'login.html', {'form': form})


from django.views.generic import ListView


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('questionList')

from rest_framework.viewsets import ViewSet
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from .models import Category, Question
from .serializers import QuestionSerializer
from django.db.models import Q
class QuestionViewSet(ViewSet):
    template_name = 'question-list.html'
    paginate_by = 8

    def list(self, request):
        queryset = self.get_queryset()
        page_number = request.GET.get('page')
        paginator = Paginator(queryset, self.paginate_by)
        page_obj = paginator.get_page(page_number)
        context = {'questions': page_obj}
        return render(request, self.template_name, context)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        question = get_object_or_404(queryset, pk=pk)
        serialized_question = QuestionSerializer(question)
        return Response(serialized_question.data)

    @action(detail=False, methods=['GET'])
    def get_all_questions(self, request):
        questions = self.get_queryset()
        serialized_questions = QuestionSerializer(questions, many=True)
        return Response(serialized_questions.data)
    
    def get_queryset(self):
        search_query = self.request.GET.get('q')
        
        if search_query:
            queryset = Question.objects.filter(Q(title__icontains=search_query))
        else:
            queryset = Question.objects.all()
        
        return queryset



class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user = self.request.user
            questions = user.questions.all()
            context['user'] = user
            context['questions'] = questions
        else:
            return HttpResponse('Unauthorized', status=401)
        return context


class MainView(ListView):
    model = Comment
    template_name = 'main.html'
    paginate_by = 5
    context_object_name = 'comments'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CommentForm()
        context['form'] = form
        return context
		
		
		

    def post(self, request):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.save()
            return redirect('main')
        else:
            context = {'form': form}
            return render(request, 'main.html', context)

    def post(self, request):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.save()
            return redirect('main')
        else:
            context = {'form': form}
            return render(request, 'main.html', context)

from django.utils.decorators import method_decorator

class AddCommentView(View):
    @method_decorator(login_required)
    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.save()
            return redirect('main')
        else:
            form = CommentForm()

        return render(request, 'main.html', {'form': form})



class CreateQuestionView(LoginRequiredMixin, View):

    def get(self, request):
        form = QuestionForm()
        context = {'form': form}
        return render(request, 'create-question.html', context)

    def post(self, request):
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            form.save_m2m()
            return redirect('questionList')

        context = {'form': form}
        return render(request, 'create-question.html', context)

class QuestionDetailView(View):
    def get(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        answers = question.answer_set.all()
        form = AnswerForm()
        
        context = {
            'question': question,
            'answers': answers,
            'form': form,
        }
        
        return render(request, 'question.html', context)
    
    @action(methods=['POST'], detail=True)
    def get_question_details(self, request, question_id):
        question = self.get_object()  # Получаем конкретный вопрос по его идентификатору
        serialized_question = QuestionSerializer(question)  # Сериализуем вопрос
        return Response(serialized_question.data)  # Возвращаем сериализованные данные в формате JSON
    
    def post(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        answers = question.answer_set.all()
        form = AnswerForm(request.POST)
        
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.author = request.user
            answer.save()
            return redirect('question_detail', question_id=question_id)
        
        context = {
            'question': question,
            'answers': answers,
            'form': form,
        }
        
        return render(request, 'question.html', context)


class AddAnswerView(View):
    @login_required
    def post(self, request, question_id):
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question_id = question_id
            answer.author = request.user
            answer.save()
            return redirect('question_detail', question_id=question_id)
        else:
            form = AnswerForm()

        return render(request, 'question.html', {'form': form})