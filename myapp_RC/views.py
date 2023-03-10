from django.shortcuts import render
from django.http import HttpResponse
from myapp_RC.models import Profile
from django.contrib.auth.models import User # using a django in built library to store or register the user in our database
from django.contrib import messages  # to display messagess after the the user has registered successfully
from django.shortcuts import redirect, render #to use the 'redirect' function in line 28
from django.contrib.auth import login,authenticate, logout  #refer line 39, 42
import re
import numpy as np
import random
from Question.models import Question

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
            
            newuserprofile=Profile(user=myuser,mob_no=mobno)
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
        return render(request, "Question/question.html")
    return render(request,"myapp_RC/instruction.html")
