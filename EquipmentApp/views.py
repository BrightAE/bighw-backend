from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from UserApp.models import User
from .models import Equipment, SaleRequest


def judge_cookie(request):
    try:
        # saved_user = User.objects.filter(rand_str=request.COOKIES['session_id'])
        saved_user = User.objects.filter(rand_str=request.headers.get('jwt'))
        if not saved_user.exists():
            return False
        return True
    except Exception:
        return False


def judge_manager(request):
    try:
        # saved_user = User.objects.get(rand_str=request.COOKIES['session_id'])
        saved_user = User.objects.get(rand_str=request.headers.get('jwt'))
        if not saved_user.authority == 'admin':
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


def equip_query(request):
    if request.method == 'GET':
        if judge_cookie(request) is False:
            return JsonResponse({"error": "please login"})
        # session_id = request.COOKIES['session_id']
        session_id = request.headers.get('jwt')
        lessor = User.objects.get(rand_str=session_id)
        filter_eles = {
            'status': 'str',
            'lessor_name': 'str',
            'lessor_id': 'int',
            'name_search': 'str',
            'username': 'str',
            'user_id': 'int',
        }
        try:
            my_filter = get_filter(request, filter_eles)
        except Exception:
            return JsonResponse({"error": "invalid filter parameters"})
        results = Equipment.objects.filter(**my_filter)
        total = len(results)
        page = parse_int(request.GET.get('page'), 1)
        page_size = parse_int(request.GET.get('page_size'), 20)
        my_filter['id__gte'] = (page - 1) * page_size
        my_filter['id__lt'] = page * page_size + 1
        results = Equipment.objects.filter(**my_filter)
        equip = []
        for item in results:
            equip.append({
                'equip_id': item.id,
                'equip_name': item.equip_name,
                'lessor_name': item.lessor_name,
                'lessor_id': item.lessor_id,
                'address': item.address,
                'end_time': item.end_time,
                'contact': item.contact,
                'status': item.status,
                'username': item.username,
                'user_id': item.user_id,
            })
        return JsonResponse({'total': total, 'equip': equip})
    return JsonResponse({"error": "wrong request method"})


def equip_set(request):
    if request.method == 'POST':
        if judge_cookie(request) is False:
            return JsonResponse({"error": "please login"})
        try:
            equip_id = request.POST.get('equip_id')
        except Exception:
            return JsonResponse({"error": "no such a equipment"})
        try:
            equip = Equipment.objects.get(id=equip_id)
            # user = User.objects.get(rand_str=request.COOKIES['session_id'])
            user = User.objects.get(rand_str=request.headers.get('jwt'))
            if user.id != equip.lessor_id and user.authority != 'admin':
                raise RuntimeError
        except Exception:
            return JsonResponse({"error": "this is not your equipment"})
        try:
            set_info = {}
            info_name = {
                'equip_name': 'str',
                'address': 'str',
                'end_time': 'str',
                'status': 'str'
            }
            for item in info_name:
                if item in request.POST:
                    set_info[item] = request.POST.get(item)
            if len(set_info) == 0:
                raise RuntimeError
        except Exception:
            return JsonResponse({"error": "no avaliable change"})
        if user.authority != 'admin' and equip.status == 'rented':
            return JsonResponse({"error": "this is equipment is not returned"})
        for item in set_info:
            equip.__setattr__(item, set_info[item])
        equip.save()
        return JsonResponse({"message": "ok"})
    return JsonResponse({"error": "wrong request method"})


def equip_delete(request):
    if request.method == 'POST':
        if judge_cookie(request) is False:
            return JsonResponse({"error": "please login"})
        try:
            equip_id = request.POST.get('equip_id')
        except Exception:
            return JsonResponse({"error": "no such a equipment"})
        try:
            equip = Equipment.objects.get(id=equip_id)
            # user = User.objects.get(rand_str=request.COOKIES['session_id'])
            user = User.objects.get(rand_str=request.headers['jwt'])
            if user.id != equip.lessor_id and user.authority != 'admin':
                raise RuntimeError
        except Exception:
            return JsonResponse({"error": "this is not your equipment"})
        equip.delete()
        return JsonResponse({"message": "ok"})
    return JsonResponse({"error": "wrong request method"})


def equip_add(request):
    if request.method == 'POST':
        if judge_cookie(request) is False:
            return JsonResponse({"error": "please login"})
        try:
            equip_name = request.POST.get('equip_name')
            address = request.POST.get('address')
        except Exception:
            return JsonResponse({"error": "invalid parameters"})
        # user = User.objects.get(rand_str=request.COOKIES['session_id'])
        user = User.objects.get(rand_str=request.headers.get('jwt'))
        equip = Equipment()
        equip.equip_name = equip_name
        equip.lessor_name = user.username
        equip.lessor_id = user.id
        equip.address = address
        equip.contact = user.contact
        equip.status = 'unavailable'
        equip.end_time = '1970-01-01'
        equip.username = 'none'
        equip.user_id = -1
        equip.save()
        return JsonResponse({"message": "ok"})
    return JsonResponse({"error": "wrong request method"})


def equip_request_query(request):
    if request.method == 'GET':
        if judge_cookie(request) is False:
            return JsonResponse({"error": "please login"})
        # lessor = User.objects.get(rand_str=request.COOKIES['session_id'])
        lessor = User.objects.get(rand_str=request.headers.get('jwt'))
        filter_eles = {
            'lessor_name': 'str',
            'lessor_id': 'int',
            'equip_name': 'str',
            'equip_id': 'int',
            'end_time': 'str',
        }
        try:
            my_filter = get_filter(request, filter_eles)
        except Exception:
            return JsonResponse({"error": "invaild filter parameters"})
        results = SaleRequest.objects.filter(**my_filter)
        total = len(results)
        page = parse_int(request.GET.get('page'), 1)
        page_size = parse_int(request.GET.get('page_size'), 20)
        my_filter['id__gte'] = (page - 1) * page_size
        my_filter['id__lt'] = page * page_size + 1
        results = SaleRequest.objects.filter(**my_filter)
        equip_req = []
        for item in results:
            lessor = User.objects.get(username=item.lessor_name)
            equip_req.append({
                "sale_req_id": item.id,
                "equip_id": item.equip_id,
                "equip_name": item.equip_name,
                "end_time": item.end_time,
                "lessor_name": item.lessor_name,
                "lessor_id": item.lessor_id,
                "status": item.status,
                "lab_info": lessor.lab_info
            })
        return JsonResponse({"total": total, "equip_req": equip_req})
    return JsonResponse({"error": "wrong request method"})


def equip_request_decide(request):
    if request.method == 'POST':
        if judge_cookie(request) is False:
            return JsonResponse({"error": "please login"})
        if judge_manager(request) is False:
            return JsonResponse({"error": "you are not administrator"})
        try:
            sale_req_id = request.POST.get('sale_req_id')
        except Exception:
            return JsonResponse({"error": "no such a sale request"})
        try:
            decision = request.POST.get('decision')
        except Exception:
            return JsonResponse({"error": "invalid decision"})
        try:
            sale_req = SaleRequest.objects.get(id=sale_req_id)
        except Exception:
            return JsonResponse({"error": "no such a sale request"})
        equip = Equipment.objects.get(id=sale_req.equip_id)
        if decision == 'reject':
            sale_req.status = 'reject'
            sale_req.save()
            return JsonResponse({"message": "ok"})
        elif decision == 'apply':
            sale_req.status = 'apply'
            equip.status = 'onsale'
            equip.end_time = sale_req.end_time
            equip.save()
            sale_req.save()
            return JsonResponse({"message": "ok"})
        else:
            return JsonResponse({"error": "invalid decision"})
    return JsonResponse({"error": "wrong request method"})


def equip_request_add(request):
    if request.method == 'POST':
        if judge_cookie(request) is False:
            return JsonResponse({"error": "please login"})
        try:
            equip_id = request.POST.get('equip_id')
            end_time = request.POST.get('end_time')
        except Exception:
            return JsonResponse({"error": "invalid parameters"})
        try:
            equip = Equipment.objects.get(id=equip_id)
        except Exception:
            return JsonResponse({"error": "no such a equipment"})
        # user = User.objects.get(rand_str=request.COOKIES['session_id'])
        user = User.objects.get(rand_str=request.headers.get('jwt'))
        if user.username != equip.lessor_name:
            return JsonResponse({"error": "this is not your equipment"})
        sale_req = SaleRequest()
        sale_req.equip_id = equip_id
        sale_req.end_time = end_time
        sale_req.equip_name = equip.equip_name
        sale_req.lessor_name = equip.lessor_name
        sale_req.lessor_id = equip.lessor_id
        sale_req.status = 'pending'
        sale_req.save()
        return JsonResponse({"message": "ok"})
    return JsonResponse({"error": "wrong request method"})
