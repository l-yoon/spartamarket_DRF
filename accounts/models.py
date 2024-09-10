from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    gender = (('M', 'Male'), ('F', 'Female'),('O', 'Other'))
    nickname = models.CharField(max_length=20)
    birth = models.DateField()
    gender = models.CharField(choices=gender, max_length=1, default = '0') 
    introduction = models.TextField(null=True, blank=True)  
 