from django.shortcuts import render
from django.http import HttpResponse
from myapp_RC.models import *
from django.contrib.auth.models import User # using a django in built library to store or register the user in our database
from django.contrib import messages  # to display messagess after the the user has registered successfully
from django.shortcuts import redirect, render #to use the 'redirect' function in line 28
from django.contrib.auth import login,authenticate, logout  #refer line 39, 42
import re
import numpy as np
import random
import datetime

def home(request):
    return render(request, "myapp_RC/register.html")

def signup(request):
    
    if request.method == "POST":
        nusername = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        nemail = request.POST['email']
        pass2 = request.POST['pass2']
        pass1 = request.POST['pass1']
        mobno = request.POST['mobno']
        
        if User.objects.filter(username = nusername).exists() :
            messages.error(request,"Username already  Exists")
        elif  User.objects.filter(email = nemail).exists():
            messages.error(request,"Email is already register")
        elif pass1 != pass2 :
            messages.error(request,"Confirmed Password did not match the entered Password")
        elif (len(pass1) < 8):
            messages.error(request,"Password should contain atleast 8 characters")
        elif not re.search("[a-z]", pass1):
            messages.error(request,"Password should contain atleast one Lowercase letter")
        elif not re.search("[A-Z]", pass1):
            messages.error(request,"Password should contain atleast one Uppercase letter")
        elif not re.search("[0-9]", pass1):
            messages.error(request,"Password should contain atleast one Number")
        elif not re.search("[_@!#%$]", pass1):
            messages.error(request,"Password should contain atleast one Special character")
        elif mobno.isnumeric() == False or len(mobno) != 10 :
            messages.error(request,"Enter a valid Mobile number")
        else :    
            myuser=User.objects.create_user(username=nusername, password=pass1, email=nemail)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()
            newuserprofile=Profile(user = myuser, mob_no = mobno)
            newuserprofile.save()

            messages.success(request, "Your account has been successfully created!")

        return redirect('/signin')   # to redirect the user to the signin page once the successful registration messages is displayed
    
    return render(request, "myapp_RC/signup.html")

def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username = username, password = pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name

            # =====================
            
            allQues = Question.objects.all()
            queIndex = np.arange(1, len(allQues)).tolist()
            random.shuffle(queIndex)

            queIndex = queIndex[:11]

            profile = Profile.objects.get(user = user)

            profile.startTime = datetime.datetime.now()
            
            profile.questionIndexList = str(queIndex)
            profile.save()
            # =====================
            return render(request, "myapp_RC/instruction.html")

        else:
            messages.error(request, "Bad Credentials")
            return render(request, "myapp_RC/signin.html")

    return render( request, "myapp_RC/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('/home')

def instruction(request):
    if request.method == 'POST':
        return render(request, "myapp_RC/question.html")
    return render(request,"myapp_RC/instruction.html")


# @login_required(login_url = 'signin')
def QuestionView(request):
    
    context = { }
    ruser = request.user
    profile = Profile.objects.get(user = ruser)
    
    context['currquestNum'] = profile.quesno
    qList = eval(profile.questionIndexList)

    currQues = Question.objects.get(question_no=qList[0])
    
    context["currquest"] = currQues.question
    
    context["profile"] = profile
    context["res10"] = str(10)
    
    context["easyQuestion"] = False


    context["second1"] = (datetime.timedelta(seconds = profile.remainingTime) -(datetime.datetime.now() - datetime.datetime.fromisoformat(str(profile.startTime)).replace(tzinfo=None))).seconds 
    
    if profile.lifeline1_count == 3 and profile.simpleQuestionUsed == False:
        profile.lifeline1_status = True
    
    if profile.isFirstTry == False :
        context["resp1"] = User_Response.objects.get(user = ruser, user_profile = profile, quetionID = qList[0], isSimpleQuestion = False).response1
    
    if profile.quesno == 11 :
        
        profile.save()
        return redirect('Result')
    print("====")
    if request.method == "POST":
        # print("Checked Status: ",request.POST.get("line2Checked"))
        print("Question: ",profile.quesno)
        print("In Post")
        
        qList = eval(profile.questionIndexList)
        if profile.isFirstTry:
            givenAns = request.POST["res1"]

            tempSol = User_Response(user_profile = profile, quetionID = qList[0], response1 = givenAns, user = profile.user, isSimpleQuestion = False)
            tempSol.save()

            if str(givenAns) == str(currQues.answer):

                if request.POST.get("line2Checked") and profile.lifeline2_checked == False:
                    profile.lifeline2_checked = True
                    print("Timer Up")
                    profile.remainingTime += 300
            
                profile.marks += 4
                profile.quesno += 1
                profile.isFirstTry = True
                profile.questionIndexList = str(qList[1:])
                print("first now qlist = ", profile.questionIndexList)
                if profile.lifeline1_count < 3 :
                    profile.lifeline1_count += 1
            
            else:
                # CHANGE BACK
                if request.POST.get("line2Checked") and profile.lifeline2_checked == False:
                    profile.lifeline2_checked = True
                    print("Timer Down")
                    profile.remainingTime -= 120    
                profile.isFirstTry = False   
            

        elif profile.isFirstTry == False:

            givenAns = request.POST["res2"]
            tempSol = User_Response.objects.get(user = profile.user, user_profile = profile, quetionID = qList[0], isSimpleQuestion = False)
            tempSol.response2 = givenAns
            tempSol.save()
            
            if str(givenAns) == str(currQues.answer):
                if request.POST.get("line2Checked") and profile.lifeline2_checked == False:
                    profile.lifeline2_checked = True
                    print("Timer Up")
                    profile.remainingTime += 300
                profile.marks += 2

            else:
                if request.POST.get("line2Checked") and profile.lifeline2_checked == False:
                    profile.lifeline2_checked = True
                    print("Timer Down")
                    profile.remainingTime -= 120
                profile.marks -= 2

            
            profile.quesno += 1
            profile.isFirstTry = True
            qList = eval(profile.questionIndexList)
            profile.questionIndexList = str(qList[1:])
            print("second now qlist = ", profile.questionIndexList)
            
        profile.save()
        # print("Profile Saved")
        request.method = "GET"
        return QuestionView(request)
    
    return render(request, 'myapp_RC/question.html', context)


def computeContext(user):
    # Time 
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
    profile.user_rank = context["rank"]
    profile.save()
    return render(request, 'myapp_RC/result.html', context)

def lifelineone(request):
    print("In Lifeline one")
    context = { }
    ruser = request.user
    profile = Profile.objects.get(user = ruser)

    profile.lifeline1_count = 0
    profile.simpleQuestionUsed = True
    profile.lifeline1_status = True

    qList = eval(profile.questionIndexList)

    context["easyQuestion"] = True

    context['currquestNum'] = profile.quesno

    currQueslist = EasyQuestion.objects.all()

    currQuest = currQueslist[random.randrange(len(currQueslist))]

    context["currquest"] = currQuest.easyquestion
    context["profile"] = profile

    context["second1"] = (datetime.timedelta(seconds=profile.remainingTime) -(datetime.datetime.now() - datetime.datetime.fromisoformat(str(profile.startTime)).replace(tzinfo=None))).seconds
       
    if profile.quesno == 11 :
        profile.save()
        return redirect('Result')
    
    if request.method == "POST":
        print("LifeLine 1 Post REQ")
        print("In lifeline POST")
        
        givenAns = request.POST["res1"]
        profile.lifeline1_status = False
        context["easyQuestion"] = False

        # givenAns = request.POST["res1"]

        # tempSol = User_Response(user_profile = profile, quetionID = qList[0], response1 = givenAns, user = profile.user, isSimpleQuestion = False)
        # tempSol.save()

        tempSol = User_Response(user_profile = profile, quetionID = currQuest.easyquestion_no, response1 = givenAns, user = profile.user, isSimpleQuestion = True)
        tempSol.save()

        if str(givenAns) == str(currQuest.easyanswer):
            profile.marks += 4
        else:
            profile.marks -= 4
        
        
        profile.quesno += 1
        profile.questionIndexList = str(qList[1:])
        print("thursday now qlist = ", profile.questionIndexList)
            
        profile.save()
    
        request.method = "GET"
        return QuestionView(request)    
    
    return render(request, 'myapp_RC/question.html', context)