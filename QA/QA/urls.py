from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import path, include
from qa_app.api import *

urlpatterns = [
	path('api/v1/question_list/', QuestionListAPI.as_view()),
	path('api/v1/question/<int:pk>/', QuestionDetailAPI.as_view()),
	path('api/v1/answer_list/', AnswerListAPI.as_view()),
    path('admin/', admin.site.urls),
    path('qa/', include('qa_app.urls')),
	path('select2/', include('django_select2.urls')),
	path("__debug__/", include("debug_toolbar.urls")),
]


urlpatterns += [
    path('', RedirectView.as_view(url='/qa/', permanent=True)),
]