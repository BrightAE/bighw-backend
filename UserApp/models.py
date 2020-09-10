from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=200)
    email = models.EmailField()
    student_id = models.CharField(max_length=20)
    authority = models.CharField(max_length=20)
    active = models.BooleanField(default=False)
    rand_str = models.CharField(max_length=233)
    contact = models.CharField(max_length=200, default=None)
    lab_info = models.CharField(max_length=200, default=None)


class AuthorityRequest(models.Model):
    user_id = models.IntegerField()
    username = models.CharField(max_length=20)
    lab_info = models.CharField(max_length=200)
    detail = models.CharField(max_length=200)
    status = models.CharField(max_length=20, default='pending')
