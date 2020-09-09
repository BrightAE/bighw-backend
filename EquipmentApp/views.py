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

def equip_query(request):
    if request.method == 'GET':
        if judge_cookie(request) == False:
            return HttpResponse(json.dumps({"error": "please login"}))
        filter = {}
        session_id = request.COOKIES['session_id']
        print(session_id)
        for user in User.objects.all():
            print(user.rand_str)
        lessor = User.objects.get(rand_str=session_id)
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
        nFilter = {}
        for filter_item in filter:
            if filter[filter_item] != None:
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
        # results = results[(page-1)*page_size:page*page_size]
        equip = []
        for item in results:
            equip.append({
                'equip_id': item.id,
                'equip_name': item.equip_name,
                'lessor_name': item.lessor_name,
                'address': item.address,
                'end_time': item.end_time,
                'contact': item.contact,
                'status': item.status,
                'username': item.username
            })
        return JsonResponse({'total': total, 'equip': equip})
    return JsonResponse({"error": "wrong request method"})

def equip_set(request):
    if request.method == 'POST':
        if judge_cookie(request) == False:
            return JsonResponse({"error": "please login"})
        try:
            equip_id = request.POST.get('equip_id')
        except:
            return JsonResponse({"error": "no such a equipment"})
        try:
            equip = Equipment.objects.get(equip_id=equip_id)
            user = User.objects.get(rand_str=request.COOKIES['session_id'])
            if user.username != equip.lessor_name:
                raise RuntimeError
        except:
            return JsonResponse({"error": "this is not your equipment"})
        try:
            set_info = request.POST.get('set_info')
        except:
            return JsonResponse({"error": "no avaliable change"})
        for item in set_info:
            equip[item] = set_info[item]
        equip.save()
        return JsonResponse({"message": "ok"})
    return JsonResponse({"error": "wrong request method"})