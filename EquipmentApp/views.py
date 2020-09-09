from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from UserApp.models import User
from .models import Equipment, SaleRequest
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

def equip_delete(request):
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
        equip.delete()
        return JsonResponse({"message": "ok"})
    return JsonResponse({"error": "wrong request method"})

def equip_add(request):
    if request.method == 'POST':
        if judge_cookie(request) == False:
            return JsonResponse({"error": "please login"})
        try:
            equip_name = request.POST.get('equip_name')
            address = request.POST.get('address')
        except:
            return JsonResponse({"error": "invalid parameters"})
        user = User.objects.get(rand_str=request.COOKIES['session_id'])
        equip = Equipment()
        equip.equip_name = equip_name
        equip.lessor_name = user.username
        equip.address = address
        equip.contact = user.contact
        equip.status = 'pending'
        equip.save()
        return JsonResponse({"message": "ok"})
    return JsonResponse({"error": "wrong request method"})

def equip_request_query(request):
    if request.method == 'GET':
        if judge_cookie(request) == False:
            return JsonResponse({"error": "please login"})
        filter = {}
        lessor = User.objects.get(rand_str=request.COOKIES['session_id'])
        try:
            filter['lessor_name'] = request.GET.get('lessor_name')
        except:
            filter['lessor_name'] = None
        try:
            filter['lessor_id'] = request.GET.get('lessor_id')
        except:
            filter['lessor_id'] = None
        try:
            filter['equip_name'] = request.GET.get('equip_name')
        except:
            filter['equip_name'] = None
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
        results = SaleRequest.objects.filter(**nFilter)
        total = len(results)
        equip_req = []
        for item in results:
            equip_req.append({
                "equip_id": item.id,
                "equip_name": item.equip_name,
                "end_time": item.end_time
            })
        return JsonResponse({"total": total, "equip_req": equip_req})
    return JsonResponse({"error": "wrong request method"})

def equip_request_decide(request):
    if request.method == 'POST':
        if judge_cookie(request) == False:
            return JsonResponse({"error": "please login"})
        try:
            sale_req_id = request.POST.get('sale_req_id')
        except:
            return JsonResponse({"error": "no such a sale request"})
        try:
            decision = request.POST.get('decision')
        except:
            return JsonResponse({"error": "invalid decision"})
        try:
            sale_req = SaleRequest.objects.get(id=sale_req_id)
        except:
            return JsonResponse({"error": "no such a sale request"})
        sale_req.status = 'apply'
        equip = Equipment.objects.get(id = sale_req.equip_id)
        equip.status = 'onsale'
        equip.end_time = sale_req.end_time
        equip.save()
        sale_req.save()
        return JsonResponse({"message": "ok"})
    return JsonResponse({"error": "wrong request method"})

def equip_request_add(request):
    if request.method == 'POST':
        if judge_cookie(request) == False:
            return JsonResponse({"error": "please login"})
        try:
            equip_id = request.POST.get('equip_id')
            end_time = request.POST.get('end_time')
        except:
            return JsonResponse({"error": "invalid parameters"})
        try:
            equip = Equipment.objects.get(id=equip_id)
        except:
            return JsonResponse({"error": "no such a equipment"})
        user = User.objects.get(rand_str=request.COOKIES['session_id'])
        if user.username !=equip.lessor_name:
            return JsonResponse({"error": "this is not your equipment"})
        sale_req = SaleRequest()
        sale_req.equip_id = equip_id
        sale_req.end = end_time
        sale_req.equip_name = equip.equip_name
        sale_req.lessor_name = equip.lessor_name
        sale_req.status = 'pending'
        sale_req.save()
        return JsonResponse({"message": "ok"})
    return JsonResponse({"error": "wrong request method"})