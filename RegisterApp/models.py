from django.db import models

# Create your models here.


class Account(models.Model):
    username = models.CharField(max_length=33, default=None)
    password = models.CharField(max_length=233, default=None)
    mail = models.CharField(max_length=50, default=None)
    student_id = models.IntegerField(default=0)
    authority = models.CharField(max_length=23, default=None)
    active = models.IntegerField(default=0)
    rand_str = models.CharField(max_length=233, default=None)


class MySession(models.Model):
    sessionID = models.CharField(max_length=233, default=None)
    username = models.CharField(max_length=33, default=None)


class MyData(models.Model):
    name = models.CharField(max_length=233, default=None)
    time = models.IntegerField(default=0)
    content = models.CharField(max_length=2333, default=None)
    user = models.CharField(max_length=233, default=None)
