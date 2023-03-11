from django.db import models
from django.contrib.auth.models import User
from myapp_RC.models import *

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

    def __str__(self):
        return self.user.username


