from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import User, check_password

class MyGroup(models.Model):
    name = models.CharField(unique=True, max_length=40)

class MyGroupUser(models.Model):
    credit = models.IntegerField()
    user = models.ForeignKey(User)
    group = models.ForeignKey(MyGroup)

class MyActivity(models.Model):
    cost = models.PositiveIntegerField()
    active = models.BooleanField()
    group = models.ForeignKey(MyGroup)

class MyRecord(models.Model):
    value = models.IntegerField()
    groupuser = models.ForeignKey(MyGroupUser)
    activity = models.ForeignKey(MyActivity)
