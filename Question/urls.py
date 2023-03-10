from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('question/', views.QuestionView, name = 'QuestionView1'),
    path('result/', views.result, name = 'Result'),
]

