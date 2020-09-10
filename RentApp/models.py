from django.db import models

# Create your models here.


class RentRequest(models.Model):
    username = models.CharField(max_length=20)
    lessor_name = models.CharField(max_length=20)
    equip_name = models.CharField(max_length=50)
    equip_id = models.IntegerField()
    status = models.CharField(max_length=20)
    detail = models.CharField(max_length=200)
    start_time = models.DateField()
    return_time = models.DateField()


class RentInformation(models.Model):
    equip_id = models.IntegerField()
    equip_name = models.CharField(max_length=50)
    lessor_name = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    rent_time = models.DateField()
    return_time = models.DateField()
    end_time = models.DateField()
    status = models.CharField(max_length=20)
