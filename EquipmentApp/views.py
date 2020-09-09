from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from UserApp.models import User
from .models import Equipment
import json

def judge_cookie(request):
    return True
    try:
        saved_user = User.objects.filter(rand_str=request.COOKIES['session_id'])
        if not saved_user.exists():
            return False
    except:
        return False

def judge_manager(request):
    return True
    try:
        saved_user = User.objects.get(rand_str=request.COOKIES['session_id'])
        if not saved_user.authority == 'admin':
            return False
    except:
        return False

def query(request):
    if request.method == 'POST':
        if judge_cookie(request) == False:
            return HttpResponse(json.dumps({"error": "please login"}))
        filter = {}
        lessor = User.objects.get(rand_str=request.COOKIES['session_id'])
        try:
            filter['status'] = request.GET.get('status')
        except:
            filter['status'] = None
        try:
            filter['lessor_name'] = request.GET.get('lessor_name')
        except:
            filter['lessor_name'] = None
        try:
            filter['lessor_id'] = request.GET.get('lessor_id')
            filter['lessor_id'] = int(filter['lessor_id'])
        except:
            filter['lessor_id'] = None
        try:
            filter['name_search'] = request.GET.get('name_search')
        except:
            filter['name_search'] = None
        if judge_manager(request) == False:
            filter['lessor_name'] = lessor.username
        for filter_item in filter:
            if filter[filter_item] == None:
                del filter[filter_item]
        results = Equipment.objects.filter(**filter)
        page = request.GET.get('page')
        page_size = request.GET.get('page_size')
        total = len(results)
        results = results[(page-1)*page_size:page*page_size]
        equip = []
        for item in results:
            equip.append({
                'equip_id': item.id,
                'equip_name': item.name,
                'lessor_name': item.lessor_name,
                'address': item.address,
                'end_time': item.end_time,
                'contact': item.contact,
                'status': item.status,
                'username': item.username
            })
        return JsonResponse({'total': total, 'equip': equip})


    return HttpResponse(json.dumps({"error": "wrong request method"}))