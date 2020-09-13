from django.db import models
from django.utils import timezone
# Create your models here.


class Message(models.Model):
    type = models.CharField(max_length=10, default='sys')
    from_id = models.IntegerField(default=0)
    to_id = models.IntegerField(default=0)
    title = models.CharField(max_length=60, default='default_title')
    content = models.CharField(max_length=200, default='default_content')
    time = models.DateTimeField(default=timezone.now)


class Evaluation(models.Model):
    user_id = models.IntegerField(default=0)
    equip_id = models.IntegerField(default=0)
    content = models.TextField(max_length=200, default='default_content')
    score = models.IntegerField(default=0)
    time = models.DateTimeField(default=timezone.now)
