from django.db import models

# Create your models here.


class Equipment(models.Model):
    equip_name = models.CharField(max_length=50)
    lessor_name = models.CharField(max_length=20)
    lessor_id = models.IntegerField()
    username = models.CharField(max_length=20)
    user_id = models.IntegerField()
    address = models.CharField(max_length=200)
    end_time = models.DateField()
    contact = models.CharField(max_length=200)
    status = models.CharField(max_length=200)


class SaleRequest(models.Model):
    equip_id = models.IntegerField()
    equip_name = models.CharField(max_length=50)
    end_time = models.DateField()
    lessor_name = models.CharField(max_length=20)
    lessor_id = models.IntegerField()
    status = models.CharField(max_length=10)