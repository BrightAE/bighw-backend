from django.db import models

# Create your models here.


class Equipment(models.Model):
    equip_name = models.CharField(max_length=50)
    lessor_name = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    end_time = models.DateField()
    contact = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    score = models.CharField(max_length=100)
    score_count = models.CharField(max_length=100)


class SaleRequest(models.Model):
    equip_id = models.IntegerField()
    equip_name = models.CharField(max_length=50)
    end_time = models.DateField()
    lessor_name = models.CharField(max_length=20)
    status = models.CharField(max_length=10)