"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from RegisterApp import views
from django.conf.urls import url
import EquipmentApp.views
import RentApp.views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^helloworld$', views.hello_world),
    url(r'^api/logon$', views.logon),
    url(r'^api/active/(.+)$', views.active),
    url(r'^api/login$', views.login),
    url(r'^api/logout$', views.logout),
    url(r'^api/equip/query$', EquipmentApp.views.equip_query),
    url(r'^api/equip/set$', EquipmentApp.views.equip_set),
    url(r'^api/equip/delete$', EquipmentApp.views.equip_delete),
    url(r'^api/equip/request/query', EquipmentApp.views.equip_request_query),
    url(r'^api/equip/request/decide', EquipmentApp.views.equip_request_decide),
    url(r'^api/equip/add', EquipmentApp.views.equip_add),
    url(r'^api/equip/request/add', EquipmentApp.views.equip_request_add),
    url(r'^api/rent/query$', RentApp.views.rent_query),
    url(r'^api/rent/request/query$', RentApp.views.rent_request_query),
    url(r'^api/request/decide$', RentApp.views.rent_request_decide),
    url(r'^api/request/delete$', RentApp.views.rent_request_delete),
    url(r'^api/request/add$', RentApp.views.rent_request_add),
    url(r'^api/rent/confirm$', RentApp.views.rent_confirm),
]
