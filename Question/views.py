from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_page
from .models import *
from myapp_RC.models import Profile
import random

@cache_page(60*5)
def QuestionView(request):
    context = { }
    ruser = request.user
    profile = Profile.objects.get(user = ruser)

    context['currquest'] = profile.quesno
    
    
   
    if profile.quesno < 10:
    
        if request.method == "POST":
            profile.quesno += 1
            profile.save()
            question1 = Question.objects.get(question_no=eval(profile.questionIndexList)[profile.quesno])
            context["question"]=question1.question
            res1 = request.POST['res1']
            # ===================================================
            res2 = request.POST['res2']
            # print(type(res2), type(res1))

            responsesUser = User_Response.objects.filter(user_profile = profile)
            responsesUser = responsesUser[len(responsesUser)-1]

            print("Correct: ",Question.objects.get(question_no=eval(profile.questionIndexList)[profile.quesno - 1]).answer, "You: ", res1)

            if responsesUser.response1 != None:
                
                if str(res1) == str(Question.objects.get(question_no=eval(profile.questionIndexList)[profile.quesno - 1]).answer):

                    profile.marks += 4
                
                else:
                    profile.marks -= 2  
                
                    # Redenr taka koni tari pls sos



            elif responsesUser.response2 == None:

                if str(res2) == str(Question.objects.get(question_no=eval(profile.questionIndexList)[profile.quesno - 1]).answer):
                    profile.marks += 2
                
                else:
                    profile.marks -= 2
                
                # Ethe pan render page kara koni tari pls Ansh SOS bro pls HELP
            # ===================================================
            profile.save()

            context["marks"] = profile.marks

            respo = User_Response(user=ruser,user_profile=profile,response1 = int(res1),response2 = int(res2), quetionID = eval(profile.questionIndexList)[profile.quesno - 1])
            respo.save()
            
            
        elif request.method == "GET":
            question1 = Question.objects.get(question_no=eval(profile.questionIndexList)[profile.quesno])
            context["question"]=question1.question

        else :
            return render(request, "Question/error.html",context)

        return render(request, "Question/question.html",context)
    else:
        return render(request, "Question/result.html", context)