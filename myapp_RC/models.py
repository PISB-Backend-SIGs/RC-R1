from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    user_rank = models.IntegerField(default=1, null=True)

    curr_question=models.IntegerField(default=1)
    questionIndexList = models.TextField(default="[-1]")

    quesno = models.IntegerField(default=1)
    mob_no = models.CharField(max_length=12)

    marks = models.IntegerField(default=0)

    isFirstTry = models.BooleanField(default = True)
    isTimeOut = models.BooleanField(default = False)

    startTime = models.DateTimeField(null = True)
    tempTime = models.DateTimeField(null = True)


    # totalTime = 

    simpleQuestionUsed = models.BooleanField(default=False)
    timeLLUsed = models.BooleanField(default=False)
    remainingTime = models.IntegerField(default = 1800)

    # lifeline one
    lifeline1_count = models.IntegerField(default=0)
    lifeline1_status = models.BooleanField(default=False)  #used to check whether or not to display the Simpe Question button

    lifeline2_status = models.BooleanField(default = False)
    lifeline2_checked = models.BooleanField(default = False)

    def __str__(self):
        return self.user.username
    

class Question(models.Model):
    question_no = models.IntegerField()    
    question=models.CharField(max_length=1000)
    answer=models.IntegerField(default=-1)
    
    def __str__(self):
        return self.question

class User_Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    user_profile= models.ForeignKey(Profile, on_delete = models.CASCADE,null=True)
    quetionID = models.IntegerField(default=-1)
    response1 = models.CharField(null = True,max_length=1000)
    response2 = models.CharField(null = True,max_length=1000)

    isSimpleQuestion = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class EasyQuestion(models.Model):
    easyquestion_no = models.IntegerField()    
    easyquestion = models.CharField(max_length=1000)
    easyanswer = models.IntegerField(default=-1)
    question_id = models.IntegerField(default = 0)
    
    def __str__(self):
        return self.easyquestion