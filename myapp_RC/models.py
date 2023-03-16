from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,)

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
    totalTime = models.IntegerField(default=-1)

    lifeline_1 = models.BooleanField(default=False)

    remainingTime = models.IntegerField(default= -1)

    def __str__(self):
        return self.user.username