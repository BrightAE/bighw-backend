from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from UserApp.models import User
from EquipmentApp.models import Equipment
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

def rent_query(request):
    if request.method == 'GET':
        if judge_cookie(request) == False:
            return JsonResponse({"error": "please login"})
        filter = {}
        session_id = request.COOKIES['session_id']
        user = User.objects.get(rand_str=session_id)
        try:
            filter['equip_id'] = request.GET.get('equip_id')
            filter['equip_id'] = int(filter['equip_id'])
        except:
            filter['equip_id'] = None
        try:
            filter['equip_name'] = request.GET.get('equip_name')
        except:
            filter['equip_name'] = None
        try:
            filter['lessor_id'] = request.GET.get('lessor_id')
            filter['lessor_id'] = int(filter['lessor_id'])
        except:
            filter['lessor_id'] = None
        try:
            filter['lessor_name'] = request.GET.get('lessor_name')
        except:
            filter['lessor_name'] = None
        try:
            filter['user_id'] = request.GET.get('user_id')
            filter['user_id'] = int(filter['user_id'])
        except:
            filter['user_id'] = None
        try:
            filter['username'] = request.GET.get('username')
        except:
            filter['user_id'] = None
        nFilter = {}
        for filter_item in filter:
            if filter[filter_item]:
                nFilter[filter_item] = filter[filter_item]
        page = request.GET.get('page')
        if page == None or page.isdigit() == False:
            page = 1
        else:
            page = int(page)
        page_size = request.GET.get('page_size')
        if page_size == None or page_size.isdigit() == False:
            page_size = 20
        else:
            page_size = int(page_size)
        nFilter['id__gte'] = (page - 1) * page_size
        nFilter['id__lt'] = page * page_size
        results = Equipment.objects.filter(**nFilter)
        total = len(results)
        rent_info = []
        for item in results:
            rent_info.append({
                'equip_id': item.equip_id,
                'equip_name': item.equip_name,
                'lessor_name': item.lessor_name,
                'username': item.username,
                'rent_time': item.rent_time,
                'return_time': item.return_time,
                'end_time': item.end_time,
                'status': item.status
            })
        return JsonResponse({"total": total, "rent_info": rent_info})
    return JsonResponse({"error": "wrong request method"})

def rent_request_query(request):
    if request.method == 'GET':
        pass
    return JsonResponse({"error": "wrong request method"})

def rent_request_decide(request):
    if request.method == 'POST':
        pass
    return JsonResponse({"error": "wrong request method"})

def rent_request_delete(request):
    if request.method == 'POST':
        pass
    return JsonResponse({"error": "wrong request method"})

def rent_request_add(request):
    if request.method == 'POST':
        pass
    return JsonResponse({"error": "wrong request method"})

def rent_confirm(request):
    if request.method == 'POST':
        pass
    return JsonResponse({"error": "wrong request method"})
