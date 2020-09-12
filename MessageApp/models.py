from django.db import models
from django.utils import timezone
# Create your models here.


class Message(models.Model):
    type = models.CharField(max_length=10, default='all')
    from_id = models.IntegerField(default=0)
    to_id = models.IntegerField(default=0)
    title = models.CharField(max_length=60, default='default_title')
    content = models.CharField(max_length=200, default='default_content')
    time = models.DateTimeField(default=timezone.now)
