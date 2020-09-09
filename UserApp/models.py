from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=200)
    mail = models.EmailField()
    student_id = models.CharField()
    authority = models.CharField()
    active = models.BooleanField(default=False)
    rand_str = models.CharField(max_length=233)
    contact = models.CharField(default=None)
    lab_info = models.CharField(default=None)