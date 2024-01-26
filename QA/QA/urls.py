from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import path, include
from rest_framework import routers
from qa_app.api import *

router = routers.DefaultRouter()

router.register(r'answers_list', AnswerListAPI, basename='answers_list')
router.register(r'questions_list', QuestionListAPI, basename='question-list')

urlpatterns = [
	path('api/', include(router.urls)),
	path('api/question_list/', QuestionListAPI.as_view({'get': 'list'})),
	path('api/question_list/filter_question', QuestionListAPI.as_view({'get': 'filter_question'}), name='filter_question'),
	path('api/question/<int:pk>/', QuestionDetailAPI.as_view({'get': 'retrieve'})),
	path('api/answers_list/', AnswerListAPI.as_view({'get': 'list'})),
	path('api/answers_list/<int:pk>/create_answer/',AnswerListAPI.as_view({'post': 'create_answer'}), name='create_answer'),
    path('admin/', admin.site.urls),
    path('qa/', include('qa_app.urls')),
	path('select2/', include('django_select2.urls')),
	path("__debug__/", include("debug_toolbar.urls")),
]

urlpatterns += [
    path('', RedirectView.as_view(url='/qa/', permanent=True)),
]