from django.db import models

# Create your models here.
class RentRequest(models.Model):
    username = models.CharField(max_length=20)
    lessor_name = models.CharField(max_length=20)
    equip_name = models.CharField(max_length=50)
    equip_id = models.IntegerField()
    status = models.CharField()
    detail = models.CharField()
    contact = models.CharField()
    return_time = models.TimeField()

class RentInfomation(models.Model):
    equip_id = models.IntegerField()
    equip_name = models.CharField(max_length=50)
    lessor_name = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    rent_time = models.TimeField()
    return_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField()