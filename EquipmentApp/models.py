from django.db import models

# Create your models here.
class Equipment(models.Model):
    equip_name = models.CharField(max_length=50)
    lessor_name = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    address = models.CharField()
    end_time = models.TimeField()
    contact = models.CharField()
    status = models.CharField()

class SaleRequest(models.Model):
    equip_id = models.IntegerField()
    equip_name = models.CharField(max_length=50)
    end_time = models.TimeField()
    lessor_name = models.CharField(max_length=20)