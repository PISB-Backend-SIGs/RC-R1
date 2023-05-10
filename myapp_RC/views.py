from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from myapp_RC.models import *
from django.contrib.auth.models import User # using a django in built library to store or register the user in our database
from django.contrib import messages  # to display messagess after the the user has registered successfully
from django.shortcuts import redirect, render #to use the 'redirect' function in line 28
from django.contrib.auth import login,authenticate, logout  #refer line 39, 42
from django.contrib.auth.decorators import login_required
import re
import numpy as np
import random
import datetime
import requests
import time
import json
from django.http import JsonResponse

def home(request):
    return render(request, "myapp_RC/signin.html")

def signup(request):
    
    if request.method == "POST":
        nusername = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        nemail = request.POST['email']
        pass2 = request.POST['pass2']
        pass1 = request.POST['pass1']
        mobno = request.POST['mobno']
        category = request.POST['categories']
        
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
            if category == '1':
                newuserprofile=Profile(user = myuser, mob_no = mobno, category = True)

            elif category == '0':
                newuserprofile=Profile(user = myuser, mob_no = mobno, category = False)
            # newuserprofile=Profile(user = myuser, mob_no = mobno)
            newuserprofile.save()

            messages.success(request, "Your account has been successfully created!")
            return redirect('/signin')   # to redirect the user to the signin page once the successful registration messages is displayed
        return redirect('/signup')
    return render(request, "myapp_RC/signup.html")

def signin(request):
    context ={}
    try :
        if request.method == 'POST':
            username = request.POST['username']
            pass1 = request.POST['pass1']
            team_value = request.POST.get('flexRadioDefault') # 1 for team, 2 for individual
            user = authenticate(username = username, password = pass1)

            if user is not None:
                login(request, user)
                fname = user.first_name

                # =====================
                profile = Profile.objects.get(user = user)

                if profile.category == True:   # True for Junior
                    allQues = Question.objects.filter(is_junior = True)
                else:   #False for Senior
                    allQues = Question.objects.filter(is_junior = False)
                
                # allQues = Question.objects.all()
                # queIndex = np.arange(1, len(allQues)).tolist()
                queIndex = [q.id for q in allQues]
                random.shuffle(queIndex)

                queIndex = queIndex[:11]

                profile.questionIndexList = str(queIndex)
                # if profile.newlogin == False :
                #     profile.newlogin = True
                # else :
                #     messages.error(request, "Already Logged in via other device")
                #     return render(request, 'myapp_RC/signin.html', context)
                profile.save()
                # =====================
                return redirect('Instruction')

            else:
                messages.error(request, "Bad Credentials")
                return render(request, "myapp_RC/signin.html")
            
    except :
        return redirect ('SignIn')

    return render( request, "myapp_RC/signin.html")

def signout(request):
    try :
        ruser = request.user
        profile = Profile.objects.get(user = ruser)
        profile.remainingTime = profile.remainingTime -(datetime.datetime.now() - datetime.datetime.fromisoformat(str(profile.startTime)).replace(tzinfo=None)).seconds 
        profile.logoutTime = datetime.datetime.now()
        logout(request)
        messages.success(request, "Logged out successfully!")
        return redirect('/home')
    except :
        return redirect('/home')

@login_required(login_url = 'SignIn')
def instruction(request):
    try :
        if request.method == 'POST':
            ruser = request.user
            profile = Profile.objects.get(user = ruser)
            profile.startTime = datetime.datetime.now()
            profile.save()
            print("profile.startTime :",profile.startTime)
            request.method = "GET"
            return QuestionView(request)
    except :
        print("ithe allo .....")
        return redirect('Instruction')
    return render(request,"myapp_RC/instruction.html")

@login_required(login_url = 'SignIn')
def QuestionView(request):
    
    context = { }
    ruser = request.user
    profile = Profile.objects.get(user = ruser)
    # print("dwer :",request.POST["submit"] )
    
    
    # if request.POST.get('submit') == int(profile.quesno):
    
    context['currquestNum'] = profile.quesno
    qList = eval(profile.questionIndexList)

    currQues = Question.objects.get(id=qList[0])
    
    context["currquest"] = currQues.question
    context['plusmrks'] = 4
    context['minusmrks'] = 0
    context["profile"] = profile

    if profile.quesno == 1:
        profile.accuracy = (profile.correctanswers/(profile.quesno))*100
    else:
        profile.accuracy = (profile.correctanswers/(profile.quesno-1))*100
    print("Accuracy: ", profile.accuracy, "%")

    context["second1"] = (datetime.timedelta(seconds = profile.remainingTime) -(datetime.datetime.now() - datetime.datetime.fromisoformat(str(profile.startTime)).replace(tzinfo=None))).seconds 
    
    # if request.method == 'POST':
    #     x1=request.POST['submit']
        
    #     if x1==int(profile.quesno):
    #         # return render(request, 'myapp_RC/question.html',context)
    #         print("-----------------------------------------",x1,profile.quesno)
    
    if profile.accuracy > 50 and profile.quesno > 3 and profile.lifeline3_status == False and profile.lifeline3_used == False:
        profile.lifeline3_status = True
    
    if profile.lifeline1_count == 3 and profile.lifeline1_using == False:
        print("In here qid generation")
        profile.lifeline1_status = True
        currQueslist = EasyQuestion.objects.all()
        profile.lifeline1_question_id = (random.randrange(len(currQueslist)))
        print("EASY QID: ", profile.lifeline1_question_id)
        profile.save()
    
    if profile.isFirstTry == False :
        context["resp1"] = User_Response.objects.get(user = ruser, user_profile = profile, quetionID = qList[0], isSimpleQuestion = False).response1
    
    if profile.lifeline1_using == True:
        print("In here , lifeline1_using true")
        givenAns = request.POST["res1"]
        profile.lifeline1_status = False  #to disable Simple Question button
        profile.simpleQuestionUsed = True 
        context["easyQuestion"] = False
        profile.lifeline1_using = False
        profile.plusmrks = 4
        profile.minusmrks = 0
        currQuest = EasyQuestion.objects.get(easyquestion_no = profile.lifeline1_question_id)


        tempSol = User_Response(user_profile = profile, quetionID = currQuest.easyquestion_no, response1 = givenAns, user = profile.user, isSimpleQuestion = True)
        tempSol.save()
        print("Easy Given ans", givenAns)
        print("Easy Question", currQuest.easyquestion)
        print("Easy Answer", currQuest.easyanswer)

        if str(givenAns) == str(currQuest.easyanswer):
            profile.marks += 4
        else:
            profile.marks -= 4
        
        # profile.save()
        profile.quesno += 1

        profile.questionIndexList = str(qList[1:])


        print(" now qlist = ", profile.questionIndexList)
        print("(In l1 in post)profile.simpleQuestionUsed = ", profile.simpleQuestionUsed)
        print("(In l1 in post)profile.lifeline1_status", profile.lifeline1_status)
            
        profile.isFirstTry = True
        print("In lifeline post profile.isFirstTry = ", profile.isFirstTry)
        print("question number before saving ",profile.quesno)
        print("Marks before save", profile.marks)
        profile.save()
        print("Marks after save", profile.marks)
        print("Question number after saving ",profile.quesno)
        request.method = "GET"
        # context['profile'] =  profile
        return QuestionView(request)

    if profile.quesno == 11 or profile.remainingTime == 0:
        profile.logoutTime = datetime.datetime.now()
        profile.save()
        return redirect('Result')
    print("====")

    context['plusmrks'] = profile.plusmrks
    context['minusmrks'] = profile.minusmrks
    
    if request.method == "POST" :
        # print("Checked Status: ",profile.lifeline2_status)
        print("Question: ",profile.quesno)
        print("In Post")
        print("profile.lifeline2_status:",profile.lifeline2_status)
        
        qList = eval(profile.questionIndexList)
        if profile.isFirstTry:
            profile.plusmrks = 4
            profile.minusmrks = 0
            givenAns = request.POST["res1"]

            tempSol = User_Response(user_profile = profile, quetionID = qList[0], response1 = givenAns, user = profile.user, isSimpleQuestion = False)
            tempSol.save()



            if str(givenAns) == str(currQues.answer):


                if profile.lifeline2_status and profile.lifeline2_checked == False:
                    profile.lifeline2_checked = True
                    profile.lifeline2_status = False
                    print("Timer Up")
                    profile.remainingTime += 300
                profile.correctanswers += 1
                
                profile.marks += 4
                profile.quesno += 1
                profile.isFirstTry = True
                profile.questionIndexList = str(qList[1:])
                print("first now qlist = ", profile.questionIndexList)
                if profile.lifeline1_count < 3 :
                    profile.lifeline1_count += 1
            
            else:
                if profile.lifeline2_status and profile.lifeline2_checked == False:                    
                    print("Timer Down")
                    profile.remainingTime -= 120 

                profile.plusmrks = 2
                profile.minusmrks = -2   
                profile.isFirstTry = False   
            

        elif profile.isFirstTry == False:

            givenAns = request.POST["res2"]
            tempSol = User_Response.objects.get(user = profile.user, user_profile = profile, quetionID = qList[0], isSimpleQuestion = False)
            tempSol.response2 = givenAns
            tempSol.save()
            profile.plusmrks = 4
            profile.minusmrks = 0
            
            if str(givenAns) == str(currQues.answer):
                if profile.lifeline2_status and profile.lifeline2_checked == False:
                    profile.lifeline2_checked = True
                    profile.lifeline2_status = False
                    print("Timer Up")
                    profile.remainingTime += 300
                profile.marks += 2
                profile.correctanswers += 1

            else:
                if profile.lifeline2_status and profile.lifeline2_checked == False:
                    profile.lifeline2_checked = True
                    profile.lifeline2_status = False
                    print("Timer Down")
                    profile.remainingTime -= 180
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
        # return redirect(QuestionView)
    
    # Calculate rank

    ruser = request.user
    profile = Profile.objects.get(user = ruser)
    context["users"] = list(Profile.objects.filter(category = profile.category).order_by('marks',"remainingTime").reverse())
    context["rank"] = context["users"].index(profile) + 1
    profile.user_rank = context["rank"]
    profile.save()

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
    context["usersjunior"] = list(Profile.objects.filter(category = True).order_by('marks',"remainingTime").reverse())
    context["userssenior"] = list(Profile.objects.filter(category = False).order_by('marks',"remainingTime").reverse())
    context["users"] = list(Profile.objects.filter(category = True).order_by('marks',"remainingTime").reverse())
    return render(request, 'myapp_RC/leaderboard.html', context)

@login_required(login_url = 'SignIn')
def result(request):
    try :
        context = {}
        ruser = request.user
        profile = Profile.objects.get(user = ruser)
        context["profile"] = profile
        context["users"] = list(Profile.objects.all().order_by('marks',"remainingTime").reverse())
        context["rank"] = context["users"].index(profile) + 1
        profile.logoutTime = datetime.datetime.now()
        context["q_correct"] = round(((profile.correctanswers)/(profile.quesno-1))*100,2)
        context["timetaken"] = round(((1800 - profile.remainingTime)/1800) * 100,2)
        context["totalques"] = profile.quesno - 1
    except :
        return redirect('SignIn')

    return render(request, 'myapp_RC/result.html', context)


@login_required(login_url = 'SignIn')
def lifelineone(request):
    print("===")
    print("In Lifeline one")
    context = { }
    ruser = request.user
    profile = Profile.objects.get(user = ruser)
    profile.lifeline1_using = True
    profile.lifeline1_count = 0
    profile.lifeline1_status = False
    print("(In l1 before post)profile.simpleQuestionUsed = ", profile.simpleQuestionUsed)
    print("(In l1 before post)profile.lifeline1_status", profile.lifeline1_status)
    
    context["plusmrks"] = 4
    context['minusmrks'] = -4
    context['plusmrks'] = profile.plusmrks
    context['minusmrks'] = profile.minusmrks
    qList = eval(profile.questionIndexList)

    context["easyQuestion"] = True
    context["isSimpleQuestion"] = profile.simpleQuestionUsed

    context['currquestNum'] = profile.quesno

    # currQueslist = EasyQuestion.objects.all()

    # currQuest = EasyQuestion.objects.get(easyquestion_no = (random.randrange(len(currQueslist))))
    print("Iska value to ye hai ->", profile.lifeline1_question_id)
    currQuest = EasyQuestion.objects.get(easyquestion_no = profile.lifeline1_question_id)
    # currQuest = currQueslist[easyquestion_no=(random.randrange(len(currQueslist)).easyques)]
    # currQuest = EasyQuestion.objects.get(easyquestion_no=qList[0])

    context["currquest"] = currQuest.easyquestion
    context["profile"] = profile

    context["second1"] = (datetime.timedelta(seconds = profile.remainingTime) -(datetime.datetime.now() - datetime.datetime.fromisoformat(str(profile.startTime)).replace(tzinfo=None))).seconds 
    profile.startTime = datetime.datetime.now()
    profile.remainingTime = context["second1"]
       
    if profile.quesno == 11 or profile.remainingTime == 0 :
        profile.logoutTime = datetime.datetime.now()
        profile.save()
        return redirect('Result')
    
    print("(In l1 after post)profile.simpleQuestionUsed = ", profile.simpleQuestionUsed)
    print("(In l1 after post)profile.lifeline1_status", profile.lifeline1_status)
    print("===")
    profile.isFirstTry = True
    profile.save()
    return render(request, 'myapp_RC/question.html', context)


def lifeLine3(request):
    ruser = request.user
    profile = Profile.objects.get(user = ruser)
    profile.lifeline3_status = False
    profile.lifeline3_used = True
    profile.save()
    print("---")
    try :
        print("in L3")
        print("======================")
        profile.lifeline3_used = True
        profile.save()
        if request.method == "GET":
            userQuery = request.GET["question"]
            allKeys = chatGPTLifeLine.objects.all()
            allKeys2 = chatGPTLifeLine.objects.filter(isDepleted = False)

            if len(allKeys2) == 0:
                return JsonResponse({'question': {userQuery},'answer': "Somethingwentwrong"})
            
            isproblem = True

            #==== remove loop after testing=====
            for k in allKeys:
                print(k.key, k.numUsed, k.isDepleted)
            #===================================
            currentTime = time.time()

            for key in allKeys2:
                print(f"Key last used {currentTime - key.lastUsed} seconds ago")
                print(f"{currentTime} - {key.lastUsed} = {currentTime - key.lastUsed}")
                
                if True:
                    if key.numUsed < 3:
                        isproblem = False
                        key.numUsed += 1
                        key.lastUsed = time.time()
                        key.save()
                        break
                    else:
                        print("Key is depleted")
                        key.isDepleted = True
                        key.save()
                else:
                    print(f"is in use: {key}")

            if isproblem:
                return JsonResponse({'question': {userQuery},'answer': "Somethingwentwrong"})
            
            answerResp = GPT_Link(userQuery, key= key)

            return JsonResponse({'question': userQuery,'answer': answerResp})
    except :
        return JsonResponse({'question': {userQuery},'answer': "Somethingwentwrong"})


def GPT_Link(message, key):
    URL = "https://api.openai.com/v1/chat/completions"

    print(f"using key: {key}")

    payload = {
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": message}],
    "temperature" : 1.0,
    "top_p":1.0,
    "n" : 1,
    "stream": False,
    "presence_penalty":0,
    "frequency_penalty":0,
    }

    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {key}"
    }

    response = requests.post(URL, headers=headers, json=payload, stream=False)
    print("Here==========",response.content)

    # if "choices" not in json.loads(response.content):
    #     return "Somethingwentwrong"
    
    return (json.loads(response.content)["choices"][0]['message']['content'])

def test(request):

    return render(request, "myapp_RC/ajaxcode1.html")

def call(request):
    allKeys = chatGPTLifeLine.objects.all()
    for key in allKeys:
        key.numUsed = 0
        key.isDepleted = False
        key.save()

@login_required(login_url = 'SignIn')
def lifeline2(request):
    print("Inside l2 function")

    ruser = request.user
    profile = Profile.objects.get(user = ruser)
    profile.lifeline2_status = True
    profile.lifeline2_superstatus = False
    profile.save()

    return JsonResponse({'success':'True'})
       
  
def webadmin(request) :
    
    if request.method == 'POST':
        superusername = request.POST['superusername']
        superpwd = request.POST['pass1']

        username = request.POST['username']
        password = request.POST['pass']

        superuser = authenticate(username = superusername, password = superpwd)
        user = authenticate(username = username, password = password)

        if superuser.is_superuser and user is not None:
            profile = Profile.objects.get(user = user)
            profile.remainingTime += int(request.POST['tabs'])

            profile.save()

            messages.success(request, "Updated")
            return render(request, "myapp_RC/signin.html")

        else:
            messages.error(request, "Bad Credentials")
            return render(request, "myapp_RC/signin.html")
        
    return render (request, "myapp_RC/webadmin.html")

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def savetimer(request) :
    if request.method == 'POST':
        context = {}
        ruser = request.user
        profile = Profile.objects.get(user = ruser)
        context["second1"] = (datetime.timedelta(seconds = profile.remainingTime) -(datetime.datetime.now() - datetime.datetime.fromisoformat(str(profile.startTime)).replace(tzinfo=None))).seconds 
        profile.startTime = datetime.datetime.now()
        profile.remainingTime = context["second1"]
        if profile.remainingTime <= 0 or profile.remainingTime >= 2500:
            logout(request)
            return render(request, 'myapp_RC/signin.html', context)
        profile.save()
        return JsonResponse({'success':'True'})