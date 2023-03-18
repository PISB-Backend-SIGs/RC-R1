from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_page
from Question.models import *
from myapp_RC.models import Profile
from datetime import datetime
import datetime
import random
from itertools import groupby

# @login_required(login_url = 'signin')
def QuestionView(request):
    # print("In Questionview")
    context = { }
    ruser = request.user
    profile = Profile.objects.get(user = ruser)
    # print("QNUM",profile.quesno)    
    context['currquestNum'] = profile.quesno
    qList = eval(profile.questionIndexList)
    
    # print("currquestion here: ",qList)
    currQues = Question.objects.get(question_no=qList[0])
    
    context["currquest"] = currQues.question
    # print("currQues.question",currQues.question)
    # context["isFirstTry"] = profile.isFirstTry
    context["profile"] = profile
    context["res10"] = str(10)
    # context["marks"] = profile.marks
    context["easyQuestion"] = False
    

    # dt_str = str(profile.startTime)
    # n1 = datetime.datetime.fromisoformat(dt_str)
    # n1 = n1.replace(tzinfo=None)

    # n2 = datetime.datetime.now()
    # n3 = n2 - n1
    
    # print("SYS TIME",n1)
    # print("SERVER TIME:",n2)
    # print(n3.seconds)

    context["min1"] = (datetime.timedelta(seconds=3600) -(datetime.datetime.now() - datetime.datetime.fromisoformat(str(profile.startTime)).replace(tzinfo=None))).seconds // 60
    context["second1"] = (datetime.timedelta(seconds=3600) -(datetime.datetime.now() - datetime.datetime.fromisoformat(str(profile.startTime)).replace(tzinfo=None))).seconds % 60
    
    # context["min1"] = profile.remainingTime.seconds // 60
    # context["second1"] = profile.remainingTime.seconds % 60
    # profile.remainingTime -= (datetime.datetime.now() - datetime.datetime.fromisoformat(str(profile.startTime)).replace(tzinfo=None))
    
    # print("context",context)

    if profile.lifeline1_count == 3 and profile.simpleQuestionUsed == False:
        profile.lifeline1_status = True
    
    if profile.isFirstTry == False :
        context["resp1"] = User_Response.objects.get(user = ruser, user_profile = profile, quetionID = qList[0], isSimpleQuestion = False).response1
    
    if profile.quesno == 11 :
        profile.remainingTime -= (datetime.datetime.now() - datetime.datetime.fromisoformat(str(profile.startTime)).replace(tzinfo=None))
        profile.save()
        return redirect('Result')
        
    if request.method == "POST":
        # print("In Post")
        
        qList = eval(profile.questionIndexList)
        if profile.isFirstTry:
            givenAns = request.POST["res1"]

            # print("first attempt")
            tempSol = User_Response(user_profile = profile, quetionID = qList[0], response1 = givenAns, user = profile.user, isSimpleQuestion = False)
            tempSol.save()
            # print("DIS--------------------", qList[0])

            if str(givenAns) == str(currQues.answer):
                # print("first correct")
                profile.marks += 4
                profile.quesno += 1
                profile.isFirstTry = True
                profile.questionIndexList = str(qList[1:])
                if profile.lifeline1_count < 3 :
                    profile.lifeline1_count += 1
            
            else:
                # CHANGE BACK
                profile.isFirstTry = False   
            

        elif profile.isFirstTry == False:

            givenAns = request.POST["res2"]
            tempSol = User_Response.objects.get(user = profile.user, user_profile = profile, quetionID = qList[0], isSimpleQuestion = False)
            tempSol.response2 = givenAns
            tempSol.save()
            
            if str(givenAns) == str(currQues.answer):
                
                # print("YOUR ANSWER:", givenAns)
                # print("CORRECT: ", currQues.answer)
                profile.marks += 2

            else:
                profile.marks -= 2

            
            profile.quesno += 1
            profile.isFirstTry = True
            qList = eval(profile.questionIndexList)
            profile.questionIndexList = str(qList[1:])
            
        profile.save()
        # print("Profile Saved")
        request.method = "GET"
        return QuestionView(request)
    
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
    context["profile"] = profile

    context["users"] = list(Profile.objects.all().order_by('marks',"remainingTime").reverse())
    context["rank"] = context["users"].index(profile) + 1
    return render(request, 'Question/result.html', context)

def lifelineone(request):
    print("In Lifeline one")
    context = { }
    ruser = request.user
    profile = Profile.objects.get(user = ruser)

    profile.lifeline1_status = False
    profile.simpleQuestionUsed = True
    qList = eval(profile.questionIndexList)

    context['currquestNum'] = profile.quesno

    currQueslist = EasyQuestion.objects.all()

    currQuest = currQueslist[random.randrange(len(currQueslist))]

    context["currquest"] = currQuest.easyquestion
    context["profile"] = profile
    # context["isFirstTry"] = profile.isFirstTry
    context["res10"] = str(10)
    # context["marks"] = profile.marks

    context["min1"] = (datetime.timedelta(seconds=3600) -(datetime.datetime.now() - datetime.datetime.fromisoformat(str(profile.startTime)).replace(tzinfo=None))).seconds // 60
    context["second1"] = (datetime.timedelta(seconds=3600) -(datetime.datetime.now() - datetime.datetime.fromisoformat(str(profile.startTime)).replace(tzinfo=None))).seconds % 60
    
       
    if profile.quesno == 11 :
        profile.remainingTime -= (datetime.datetime.now() - datetime.datetime.fromisoformat(str(profile.startTime)).replace(tzinfo=None))
        profile.save()
        return redirect('Result')

    if not profile.simpleQuestionUsed: 
        print("In firt if statement")
        profile.simpleQuestionUsed = True
        
        if request.method == "GET":
            print("In lifeline GET")
            givenAns = request.GET["res1"]

            tempSol = User_Response(user_profile = profile, quetionID = currQuest.easyquestion_no, response1 = givenAns, user = profile.user, isSimpleQuestion = True)
            tempSol.save()

            if str(givenAns) == str(currQuest.easyanswer):
                profile.marks += 4
            else:
                profile.marks -= 4
            
            
            profile.quesno += 1
            profile.questionIndexList = str(qList[1:])
            profile.isFirstTry = True
                
            profile.save()
            request.method = "POST"
            return QuestionView(request)
    
    return render(request, 'Question/question.html', context)
