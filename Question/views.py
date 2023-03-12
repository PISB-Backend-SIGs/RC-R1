from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_page
from Question.models import *
from myapp_RC.models import Profile
from datetime import datetime
import datetime
from itertools import groupby

# @login_required(login_url = 'signin')
def QuestionView(request):
    print("In Questionview")
    context = { }
    ruser = request.user
    profile = Profile.objects.get(user = ruser)
    print("QNUM",profile.quesno)    
    context['currquestNum'] = profile.quesno
    qList = eval(profile.questionIndexList)
    
    print("currquestion here: ",qList)
    currQues = Question.objects.get(question_no=qList[0])
    
    context["currquest"] = currQues.question
    print("currQues.question",currQues.question)
    context["isFirstTry"] = profile.isFirstTry
    context["res10"] = str(10)
    context["marks"] = profile.marks
    

    dt_str = str(profile.startTime)
    n1 = datetime.datetime.fromisoformat(dt_str)
    n1 = n1.replace(tzinfo=None)

    n2 = datetime.datetime.now()
    n3 = n2 - n1
    
    print("SYS TIME",n1)
    print("SERVER TIME:",n2)
    print(n3.seconds)

    context["min1"] = (datetime.timedelta(seconds=3600) -(datetime.datetime.now() - datetime.datetime.fromisoformat(str(profile.startTime)).replace(tzinfo=None))).seconds // 60
    context["second1"] = (datetime.timedelta(seconds=3600) -(datetime.datetime.now() - datetime.datetime.fromisoformat(str(profile.startTime)).replace(tzinfo=None))).seconds % 60
    
    print("context",context)
    
    if profile.isFirstTry == False :
        context["resp1"] = User_Response.objects.get(user = ruser, user_profile = profile, quetionID = qList[0]).response1
    
    if profile.quesno == 11 :
        profile.remainingTime = (datetime.timedelta(seconds=3600) -(datetime.datetime.now() - datetime.datetime.fromisoformat(str(profile.startTime)).replace(tzinfo=None))).seconds
        profile.save()
        return redirect('Result')
        
    if request.method == "POST":
        print("In Post")
        
        qList = eval(profile.questionIndexList)
        if profile.isFirstTry:
            givenAns = request.POST["res1"]

            print("first attempt")
            tempSol = User_Response(user_profile = profile, quetionID = qList[0], response1 = givenAns, user = profile.user)
            tempSol.save()
            # print("DIS--------------------", qList[0])

            if str(givenAns) == str(currQues.answer):
                print("first correct")
                profile.marks += 4
                profile.quesno += 1
                profile.isFirstTry = True
                profile.questionIndexList = str(qList[1:])
            
            else:
                # CHANGE BACK
                profile.isFirstTry = False   
            

        elif profile.isFirstTry == False:

            givenAns = request.POST["res2"]
            tempSol = User_Response.objects.get(user = profile.user, user_profile = profile, quetionID = qList[0])
            tempSol.response2 = givenAns
            tempSol.save()
            
            if str(givenAns) == str(currQues.answer):
                
                print("YOUR ANSWER:", givenAns)
                print("CORRECT: ", currQues.answer)
                profile.marks += 2

            else:
                profile.marks -= 2

            
            profile.quesno += 1
            profile.isFirstTry = True
            qList = eval(profile.questionIndexList)
            profile.questionIndexList = str(qList[1:])
            
        profile.save()
        print("Profile Saved")
        request.method = "GET"
        return QuestionView(request)
    
    else:
        print(context)
    return render(request, 'Question/question.html', context)


def computeContext(user):
    profile = Profile.objects.get(user = user)
    qList = eval(profile.questionIndexList)
    que = Question.objects.get(question_no = qList[0])
    context = {"currquest" : que}
    context["currquestNum"] = profile.quesno
    context["isFirstTry"] = profile.isFirstTry

    return profile, que, context

def leaderboard(request) :
    context = {}
    ruser = request.user

    profile = Profile.objects.get(user = ruser)
    context["marks"] = profile.marks

    context["users"] = list(Profile.objects.all().order_by('marks',"remainingTime").reverse())
    context["rank"] = context["users"].index(profile) + 1
    return render(request, 'Question/result.html', context)