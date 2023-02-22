from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,)
    curr_question=models.IntegerField(default=0)
    mob_no = models.CharField(max_length=12)
    
    def __str__(self):
        return self.user.first_name