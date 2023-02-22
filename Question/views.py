from django.shortcuts import render
from django.contrib.auth.models import User
from .models import *
from myapp_RC.models import Profile
import random

def QuestionView(request):
    context = { }
    ruser = request.user
    profile = Profile.objects.get(user=ruser)
    print(profile)
    if request.method == "POST":
        question1 = Question.objects.get(question_no=profile.curr_question)
        context["question"]=question1.question
    else:
        question1 = list(Question.objects.all())
        context['question']=question1[0].question
    return render(request, "Question/question.html",context)


def test(request):
    print(list(Question.objects.get(question_no = 1)))
    return render(request, "Question/question.html")