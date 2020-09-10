from django.contrib import admin
from .models import RentInformation, RentRequest
# Register your models here.

admin.site.register(RentInformation)
admin.site.register(RentRequest)