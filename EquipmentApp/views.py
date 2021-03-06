from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from UserApp.models import User
from .models import Equipment, SaleRequest
from RentApp.models import RentInformation, RentRequest
from fuzzywuzzy import fuzz
from MessageApp.models import Message
from MessageApp.add_message import add_message

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


def delete_item(items):
    for item in items:
        item.delete()


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
            'username': 'str',
            'user_id': 'int',
        }
        try:
            my_filter = get_filter(request, filter_eles)
        except Exception:
            return JsonResponse({"error": "invalid filter parameters"})
        if 'ordered_by' in request.GET:
            ordered_by = request.GET.get('ordered_by')
        else:
            ordered_by = '-id'
        print('ordered_by', ordered_by)
        results = Equipment.objects.filter(**my_filter).order_by(ordered_by)
        total = len(results)
        page = parse_int(request.GET.get('page'), 1)
        page_size = parse_int(request.GET.get('page_size'), 20)
        equip = []
        if 'name_search' in request.GET:
            name_search = request.GET.get('name_search')
        else:
            name_search = ''
        for i in range((page-1)*page_size, page*page_size):
            if i >= len(results):
                break
            item = results[i]
            if_add = 1
            if name_search != '' and name_search is not None:
                value = fuzz.token_sort_ratio(name_search, item.equip_name)
                if value < 40:
                    if_add = 0
            if if_add == 1:
                equip.append({
                    'equip_id': item.id,
                    'equip_name': item.equip_name,
                    'lessor_name': item.lessor_name,
                    'address': item.address,
                    'end_time': item.end_time,
                    'contact': item.contact,
                    'status': item.status,
                    'username': item.username,
                    'score': float(item.score),
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
            if user.username != equip.lessor_name and user.authority != 'admin':
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
        add_message('sys', user.id, 0, '修改设备信息', '修改设备'+equip.equip_name+'的信息')
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
            if user.username != equip.lessor_name and user.authority != 'admin':
                raise RuntimeError
        except Exception:
            return JsonResponse({"error": "this is not your equipment"})
        sale_requests = SaleRequest.objects.filter(equip_id=equip.id)
        rent_info = RentInformation.objects.filter(equip_id=equip.id)
        rent_req = RentRequest.objects.filter(equip_id=equip.id)
        delete_item(sale_requests)
        delete_item(rent_info)
        delete_item(rent_req)
        add_message('sys', user.id, 0, '删除设备', '删除设备'+equip.equip_name)
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
        equip.address = address
        equip.contact = user.contact
        equip.status = 'unavailable'
        equip.end_time = '1970-01-01'
        equip.username = 'none'
        equip.score = '0'
        equip.score_count = '0'
        equip.save()
        add_message('sys', user.id, 0, '添加设备', '添加设备'+equip.equip_name)
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
            'equip_name': 'str',
            'equip_id': 'int',
            'end_time': 'str',
            'status': 'str',
        }
        try:
            my_filter = get_filter(request, filter_eles)
        except Exception:
            return JsonResponse({"error": "invaild filter parameters"})
        if 'ordered_by' in request.GET:
            ordered_by = request.GET.get('ordered_by')
        else:
            ordered_by = '-id'
        results = SaleRequest.objects.filter(**my_filter).order_by(ordered_by)
        total = len(results)
        page = parse_int(request.GET.get('page'), 1)
        page_size = parse_int(request.GET.get('page_size'), 20)
        equip_req = []
        for i in range((page-1)*page_size, page*page_size):
            if i >= len(results):
                break
            item = results[i]
            lessor = User.objects.get(username=item.lessor_name)
            equip_req.append({
                "sale_req_id": item.id,
                "equip_id": item.equip_id,
                "equip_name": item.equip_name,
                "end_time": item.end_time,
                "lessor_name": item.lessor_name,
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
        lessor = User.objects.get(username=equip.lessor_name)
        if decision == 'reject':
            sale_req.status = 'reject'
            sale_req.save()
            add_message('sys', 0, 0, '拒绝上架申请'+equip.equip_name)
            add_message('lessor',0, lessor.id, '管理员拒绝了您的上架申请')
            return JsonResponse({"message": "ok"})
        elif decision == 'apply':
            sale_req.status = 'apply'
            equip.status = 'onsale'
            equip.end_time = sale_req.end_time
            equip.save()
            sale_req.save()
            add_message('sys', 0, 0, '同意上架申请'+equip.equip_name)
            add_message('lessor',0, lessor.id, '管理员同意了您的上架申请')
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
        sale_req.status = 'pending'
        sale_req.save()
        add_message('sys', 0, 0, '添加上架申请', '设备'+equip.equip_name+'添加了上架申请')
        return JsonResponse({"message": "ok"})
    return JsonResponse({"error": "wrong request method"})
