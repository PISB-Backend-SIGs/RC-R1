from django.shortcuts import render
from django.contrib.auth.models import User
from .models import *
from myapp_RC.models import Profile
import random

def QuestionView(request):
    context = { }
    ruser = request.user
    profile = Profile.objects.get(user = ruser)

    context['currquest'] = profile.quesno
    
    
   
    if profile.quesno < 11:
    
        if request.method == "POST":
            profile.quesno += 1
            profile.save()
            question1 = Question.objects.get(question_no=eval(profile.questionIndexList)[profile.quesno])
            context["question"]=question1.question
            res1 = request.POST['res1']

            respo = User_Response(user=ruser,response1 = int(res1))
            respo.save()
            
            
        elif request.method == "GET":
            question1 = Question.objects.get(question_no=eval(profile.questionIndexList)[0])
            context["question"]=question1.question

        else :
            return render(request, "Question/error.html",context)

        return render(request, "Question/question.html",context)
    else:
        return render(request, "Question/result.html", context)