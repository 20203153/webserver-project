"""
URL configuration for pybo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path

from pybo import views

urlpatterns = [
    # question_list
    path('', views.QuestionListAPI.as_view(), name='index'),

    # questions
    path('<int:question_id>/', views.QuestionDetailAPI.as_view(), name='question'),
    path('question/', views.QuestionCreateAPI.as_view(), name='question_create'),
    path('question/<int:question_id>/', views.QuestionCreateAPI.as_view(), name='question_modify'),

    # answers
    path('<int:question_id>/<int:answer_id>/', views.AnswerDetailAPI.as_view(), name='answer'),
    path('answer/<int:question_id>/', views.AnswerCreateAPI.as_view(), name='answer_create'),
    path('answer/<int:question_id>/<int:answer_id>/', views.AnswerCreateAPI.as_view(), name='answer_modify'),

    # topics
    path('topics/', views.TopicListAPI.as_view(), name='topics'),
    path('topics/<int:topic_id>/', views.TopicAPI.as_view(), name='topic'),

    # vote
    path('vote/question/<int:question_id>/', views.QuestionVoteAPI.as_view(), name='question_vote'),
    path('vote/answer/<int:answer_id>/', views.AnswerVoteAPI.as_view(), name='question_vote'),
]
