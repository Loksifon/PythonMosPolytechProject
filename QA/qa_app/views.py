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

# def signup(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             auth_login(request, user)
#             return redirect('login')  
#     else:
#         form = RegistrationForm()
#     return render(request, 'signup.html', {'form': form})


# def my_login(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
                
#                 return redirect('questionList')
#         else:
            
#             pass
#     else:
#         form = AuthenticationForm()
#     return render(request, 'login.html', {'form': form})

# def my_logout(request):
# 	logout(request)
# 	return redirect('questionList')


# def questionList(request, category_id=None):
#     questions = Question.objects.all()

#     if category_id:
#         category = Category.objects.get(id=category_id)
#         tags = category.tags.all()
#         questions = questions.filter(tags__in=tags)

#     categories = Category.objects.all()

#     context = {
#         'questions': questions,
#         'categories': categories,
#     }

#     return render(request, 'question-list.html', context)



# @login_required
# def profile(request):
#     user = request.user
#     questions = user.questions.all()

#     context = {
#         'user': user,
#         'questions': questions
#     }

#     return render(request, 'profile.html', context)



# def main(request):
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.author = request.user
#             comment.save()
#             return redirect('main')

#     else:
#         form = CommentForm()

#     comments = Comment.objects.all()

#     context = {
#         'form': form,
#         'comments': comments
#     }

#     return render(request, 'main.html', context)

# @login_required
# def add_comment(request):
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.author = request.user
#             comment.save()
#             return redirect('main')
#     else:
#         form = CommentForm()

#     return render(request, 'main.html', {'form': form})

# @login_required
# def create_question(request):
#     if request.method == 'POST':
#         form = QuestionForm(request.POST)
#         if form.is_valid():
#             question = form.save(commit=False)
#             question.author = request.user
#             question.save()
#             form.save_m2m()  
#             return redirect('questionList')
#     else:
#         form = QuestionForm()
    
#     context = {
#         'form': form
#     }
#     return render(request, 'create-question.html', context)


# def question_detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     answers = question.answer_set.all()
    
#     if request.method == 'POST':
#         form = AnswerForm(request.POST)
#         if form.is_valid():
#             answer = form.save(commit=False)
#             answer.question = question
#             answer.author = request.user
#             answer.save()
#             return redirect('question_detail', question_id=question_id)
#     else:
#         form = AnswerForm()

#     context = {
#         'question': question,
#         'answers': answers,
#         'form': form,
#     }
    
#     return render(request, 'question.html', context)


# @login_required
# def add_answer(request, question_id):
#     if request.method == 'POST':
#         form = AnswerForm(request.POST)
#         if form.is_valid():
#             answer = form.save(commit=False)
#             answer.question_id = question_id
#             answer.author = request.user
#             answer.save()
#             return redirect('question_detail', question_id=question_id)
#     else:
#         form = AnswerForm()

#     return render(request, 'question.html', {'form': form})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views import View
from .forms import RegistrationForm, CommentForm, QuestionForm, AnswerForm
from .models import Question, Tag, User, Comment, Category, Answer



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



class QuestionListView(ListView):
    model = Question
    template_name = 'question-list.html'
    context_object_name = 'questions'
    paginate_by = 8

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        if category_id:
            category = get_object_or_404(Category, id=category_id)
            tags = category.tags.all()
            queryset = queryset.filter(tags__in=tags)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        if category_id:
            category = get_object_or_404(Category, id=category_id)
            tags = category.tags.all()
            questions = context['questions']
            questions = questions.filter(tags__in=tags)
            paginator = Paginator(questions, self.paginate_by)
            page_number = self.request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context['questions'] = page_obj
        return context

class ProfileView(View):
    @login_required
    def get(self, request):
        user = request.user
        questions = user.questions.all()

        context = {
            'user': user,
            'questions': questions
        }

        return render(request, 'profile.html', context)



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