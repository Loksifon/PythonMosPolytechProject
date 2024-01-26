from django.urls import path, include
from . import views


urlpatterns = [
	path('', views.MainView.as_view(), name='main'),
	path('questions/', views.QuestionViewSet.as_view({'get': 'list'}), name='questionList'),
	path('questions/get_all_questions', views.QuestionViewSet.as_view({'get': 'get_all_questions'}), name='get_all_questions'),
	path('signup/', views.SignupView.as_view(), name='signup'),
  path('login/', views.LoginView.as_view(), name='login'),
	path('logout/', views.LogoutView.as_view(), name='logout'),
	path('profile/', views.ProfileView.as_view(), name='profile'),
	path('add_comment/', views.AddCommentView.as_view(), name='add_comment'),
	path('question/create/', views.CreateQuestionView.as_view(), name='create_question'),
	path('question/<int:question_id>/', views.QuestionDetailView.as_view(), name='question_detail'),
	path('add_answer/<int:question_id>/', views.AddAnswerView.as_view(), name='add_answer'),
]

