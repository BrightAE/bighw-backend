from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from UserApp.models import User
from EquipmentApp.models import Equipment
from .models import RentInformation, RentRequest
import json

def judge_cookie(request):
    try:
        saved_user = User.objects.filter(rand_str=request.COOKIES['session_id'])
        if not saved_user.exists():
            return False
        return True
    except Exception:
        return False


def judge_manager(request):
    try:
        saved_user = User.objects.get(rand_str=request.COOKIES['session_id'])
        if not saved_user.authority == 'admin':
            return False
        return True
    except Exception:
        return False


def parse_int(instr, deft):
    if instr is None or instr.isdigit() is False:
        ret = deft
    else:
        ret = int(instr)
    return ret


def get_filter(request, filter_eles):
    my_filter = {}
    for name in filter_eles:
        if name in request.GET:
            my_filter[name] = request.GET.get(name)
            if filter_eles[name] == 'int':
                my_filter[name] = int(my_filter[name])
    return my_filter


def rent_query(request):
    if request.method == 'GET':
        if judge_cookie(request) is False:
            return JsonResponse({"error": "please login"})
        session_id = request.COOKIES['session_id']
        user = User.objects.get(rand_str=session_id)
        filter_eles = {
            'equip_id': 'int',
            'equip_name': 'str',
            'lessor_id': 'int',
            'lessor_name': 'str',
            'user_id': 'int',
            'username': 'str'
        }
        try:
            my_filter = get_filter(request, filter_eles)
        except Exception:
            return JsonResponse({"error": "invalid filter parameters"})
        results = RentInformation.objects.filter(**my_filter)
        total = len(results)
        page = parse_int(request.GET.get('page'), 1)
        page_size = parse_int(request.GET.get('page_size'), 20)
        my_filter['id__gte'] = (page - 1) * page_size
        my_filter['id__lt'] = page * page_size
        results = RentInformation.objects.filter(**my_filter)
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
        if judge_cookie(request) is False:
            return JsonResponse({"error": "please login"})
        session_id = request.COOKIES['session_id']
        user = User.objects.get(rand_str=session_id)
        filter_eles = {
            'equip_id': 'int',
            'equip_name': 'str',
            'lessor_id': 'int',
            'lessor_name': 'str',
            'user_id': 'int',
            'username': 'str'
        }
        try:
            my_filter = get_filter(request, filter_eles)
        except Exception:
            return JsonResponse({"error": "invalid filter parameters"})
        results = RentRequest.objects.filter(**my_filter)
        total = len(results)
        page = parse_int(request.GET.get('page'), 1)
        page_size = parse_int(request.GET.get('page_size'), 20)
        my_filter['id__gte'] = (page - 1) * page_size
        my_filter['id__lt'] = page * page_size
        results = RentRequest.objects.filter(**my_filter)
        rent_req = []
        for item in results:
            rent_req.append({
                'equip_id': item.equip_id,
                'equip_name': item.equip_name,
                'lessor_name': item.lessor_name,
                'username': item.username,
                'start_time': item.start_time,
                'return_time': item.return_time,
                'detail': item.detail,
                'status': item.status,
            })
    return JsonResponse({"error": "wrong request method"})

def rent_request_decide(request):
    if request.method == 'POST':
        if judge_cookie(request) is False:
            return JsonResponse({"error": "please login"})
        if 'rent_req_id' in request.POST:
            rent_req_id = request.POST
        else:
            return JsonResponse({"error": "no such a rent request"})
        if 'decision' in request.POST:
            decision = request.POST.get('decision')
        else:
            return JsonResponse({"error": "invalid decision"})
        try:
            rent_req = RentRequest.objects.get(id=rent_req_id)
        except Exception:
            return JsonResponse({"error": "no such a rent request"})
        equip = Equipment.objects.get(id=rent_req.equip_id)
        if equip.status != 'onsale':
            return JsonResponse({"error": "this equipment is not available"})
        if decision == 'reject':
            rent_req.status = 'reject'
            rent_req.save()
            return JsonResponse({"message": "ok"})
        elif decision == 'apply':
            rent_req.status = 'apply'
            equip.status = 'rented'
            rent_info = RentInformation(
                equip_id=rent_req.equip_id,
                equip_name=rent_req.equip_name,
                lessor_name=rent_req.lessor_name,
                username=rent_req.username,
                rent_time=rent_req.start_time,
                return_time=None,
                end_time=equip.end_time,
                status='unreturned'
            )
            rent_req.save()
            equip.save()
            rent_info.save()
        else:
            return JsonResponse({"error": "invalid decision"})
    return JsonResponse({"error": "wrong request method"})

def rent_request_delete(request):
    if request.method == 'POST':
        pass
    return JsonResponse({"error": "wrong request method"})

def rent_request_add(request):
    if request.method == 'POST':
        if judge_cookie(request) is False:
            return JsonResponse({"error": "please login"})
        try:
            equip_id = request.POST.get('equip_id')
            detail = request.POST.get('detail')
            start_time = request.POST.get('start_time')
            return_time = request.POST.get('return_time')
        except Exception:
            return JsonResponse({"error": "invaild parameters"})
        try:
            equip = Equipment.objects.get(id=equip_id)
        except Exception:
            return JsonResponse({"error": "no such a equipment"})
        if equip.status != 'onsale':
            return JsonResponse({"error": "this equipment is not available"})
        user = User.objects.get(rand_str=request.COOKIES['session_id'])
        rent_req = RentRequest(
            username=user.username,
            lessor_name=equip.lessor_name,
            equip_name=equip.equip_name,
            equip_id=equip_id,
            status='pending',
            detail=detail,
            start_time=start_time,
            return_time=return_time
        )
        rent_req.save()
        return JsonResponse({"message": "ok"})
    return JsonResponse({"error": "wrong request method"})

def rent_confirm(request):
    if request.method == 'POST':
        if judge_cookie(request) is False:
            return JsonResponse({"error": "please login"})
        if 'rent_info_id' in request.POST:
            rent_info_id = request.POST
        else:
            return JsonResponse({"error": "invalid parameters"})
        try:
            rent_info = RentInformation.objects.get(id=rent_info_id)
            equip = Equipment.objects.get(id=rent_info.equip_id)
        except Exception:
            return JsonResponse({"error": "no such rent infomation"})
        rent_info.status = 'returned'
        equip.status = 'onsale'
        rent_info.save()
        equip.save()
    return JsonResponse({"error": "wrong request method"})
