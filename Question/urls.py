from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('question/', views.QuestionView, name = 'QuestionView1'),
    path('result/', views.leaderboard, name = 'Result'),
    path('lifeline1/', views.lifelineone, name = 'lifeline1'),
]

