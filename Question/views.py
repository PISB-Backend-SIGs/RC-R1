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

    context['currquestNum'] = profile.quesno
    
    if request.method == "POST":
        # Post Request
        # MAKE SURE THAT WHE NYOU CREATE PROFILE THE QUESTION NUMBER IS SET TO 0
        # MARKS ALSO SET TO 0
        if profile.quesno == 0:
            # First Question
            profile.quesno += 1
            context["currquestNum"] = profile.quesno
            
            sendQuestion = Question.objects.get(question_no=eval(profile.questionIndexList)[profile.quesno])
            context["currquest"]=sendQuestion.question

            context["marks"] = profile.marks

            profile.save()

            return render(request, "Question/question.html",context)
        
        elif profile.quesno < len(eval(profile.questionIndexList)) - 1:
            # Second Question to Last Question
            checkQuestionIndex = profile.quesno
            
            # Question Checking part begin 
            checkQuestion = Question.objects.get(question_no=eval(profile.questionIndexList)[checkQuestionIndex])
            correctSol = checkQuestion.answer

            if profile.isFirstTry == True:
                givenSol = request.POST['res1']
                if str(givenSol) == str(correctSol):
                    profile.marks += 4

                else:
                    profile.marks -= 2
                    profile.isFirstTry = False

                    profile.save()

                    # RENDERING THE SECOND ATTEMPT PAGE
                    
                    context["hint"] = givenSol

                    currentQuesNum = profile.quesno

                    context["currquestNum"] = currentQuesNum

                    sendQuestion = Question.objects.get(question_no=eval(profile.questionIndexList)[currentQuesNum])
                    context["currquest"]=sendQuestion.question

                    context["marks"] = profile.marks

                    return render(request, "Question/quesRes2.html",context)

            
            elif profile.isFirstTry == False:

                profile.isFirstTry = True
                profile.save()

                givenSol = request.POST['res2']

                if str(givenSol) == str(correctSol):
                    profile.marks += 4
                else:
                    profile.marks -= 2
            
            else:

                profile.isFirstTry = True
                profile.save()    

                # RENDER THE ERRORS PAGE
                pass 

            # Question Checking part complete

            # Next Question Part begin

            profile.quesno += 1
            currentQuesNum = profile.quesno

            context["currquestNum"] = currentQuesNum

            sendQuestion = Question.objects.get(question_no=eval(profile.questionIndexList)[currentQuesNum])
            context["currquest"]=sendQuestion.question

            context["marks"] = profile.marks
            # Next Question Part complete

            profile.save()

            return render(request, "Question/quesRes1.html",context)
        
        else:
            # Last question over so checking it then rendering result
            checkQuestionIndex = profile.quesno
            
            # Question Checking part begin 
            
            checkQuestion = Question.objects.get(question_no=eval(profile.questionIndexList)[checkQuestionIndex])
            correctSol = checkQuestion.answer

            if profile.isFirstTry == True:
                givenSol = request.POST['res1']

                if str(givenSol) == str(correctSol):
                    profile.marks += 4

                else:
                    profile.marks -= 2

            else:
                givenSol = request.POST['res2']

                if str(givenSol) == str(correctSol):
                    profile.marks += 4

                else:
                    profile.marks -= 2

            # Question Checking part begin 

            context["marks"] = profile.marks
            profile.save()

            return render(request, "Question/result.html",context)
        
    elif request.method == "GET":
        # Get Request
        # NEED TO FIX THIS PART

        # OPTION 1: SIMPLY MAKE THE REQUEST IN THE INSTRUCTION PAGE POST
        # OPTION 2: MAKE ANOTHER PAGE FOR THIS PART

        #==============================USE THIS==========================================
        # context["marks"] = "GET REQUEST"
        # return render(request, "Question/quesRes1.html",context)

        #==============================THIS IS FOR TESTING===============================
        context["tryStatus"] = "First Attempt"
        context["hint"] = -1
        return render(request, "Question/quesRes1.html",context)

    else:
        # Send Errors!!
        return render(request, "Question/error.html",context)