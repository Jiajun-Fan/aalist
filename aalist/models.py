from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import User, check_password

class MyGroup(models.Model):
    name = models.CharField(unique=True, max_length=40)
    members = models.ManyToManyField(User)
