from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,)

    curr_question=models.IntegerField(default=1)
    questionIndexList = models.TextField(default="[-1]")

    quesno = models.IntegerField(default=1)
    mob_no = models.CharField(max_length=12)

    marks = models.IntegerField(default=0)

    isFirstTry = models.BooleanField(default = True)
    isTimeOut = models.BooleanField(default = False)

    startTime = models.DateTimeField(default = datetime.now())
    tempTime = models.DateTimeField(default = datetime.now())
    totalTime = models.IntegerField(default=-1)

    def __str__(self):
        return self.user.username