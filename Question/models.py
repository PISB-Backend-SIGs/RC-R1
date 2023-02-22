from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    question_no = models.IntegerField()    
    question=models.CharField(max_length=1000)
    answer=models.IntegerField()
    
    def __str__(self):
        return self.question

class User_Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    question_id = models.ForeignKey(Question, on_delete = models.CASCADE,default=None)
    response = models.IntegerField()

    def __str__(self):
        return self.user.username+f'({self.response})'


