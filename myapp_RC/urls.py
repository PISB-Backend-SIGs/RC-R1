from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.home, name = 'Login'),
    path('home/', views.home, name = 'Login'),
    path('signup/', views.signup, name = 'SignUp'),
    path('signin/', views.signin, name = 'SignIn'),
    path('signout/', views.signout, name = 'SignOut'),
    path('instruction/',views.instruction, name = 'Instruction'),
    path('question/', views.QuestionView, name = 'QuestionView'),
    path('question/', views.check_page, name = 'TabSwitch'),
    path('question/', views.lifelineone, name = 'lifeline1'),
    path('result/', views.leaderboard, name = 'Result'),
]