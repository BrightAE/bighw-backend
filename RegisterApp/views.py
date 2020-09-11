# from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
from UserApp.models import User, AuthorityRequest
# from django.contrib.auth.hashers import make_password, check_password
import RegisterApp.send_email
import random
import string
# import json
# import time

# from django.views.decorators.csrf import csrf_exempt


def hello_world(request):
    return HttpResponse("<h1>Hello world !</h1>")


# @csrf_exempt
def logon(request):
    if request.method != 'POST':
        return JsonResponse({"error": "require POST"})
    all_index = ['username', 'password', 'student_id', 'email', 'contact']
    # print(request.POST['email'])
    for index in all_index:
        if index not in request.POST or len(request.POST[index]) == 0:
            return JsonResponse({"error": "invalid parameters"})

    input_username = request.POST['username']
    input_password = request.POST['password']
    input_email = request.POST['email']
    input_student_id = int(request.POST['student_id'])
    input_contact = request.POST['contact']

    items = User.objects.all()
    for item in items:
        if item.student_id == input_student_id or item.username == input_username:
            return JsonResponse({"error": "user exists"})

    test = User()
    test.username = input_username
    test.password = input_password
    test.student_id = input_student_id
    test.email = input_email
    test.contact = input_contact
    test.authority = 'user'
    test.active = False
    test.lab_info = ' '
    test.rand_str = ''
    test.save()

    # items = User.objects.all()
    # for item in items:
    #     print(item.id, ' ', item.username, ' ', item.password, ' ', item.email,
    #           ' ', item.student_id, ' ', item.authority, ' ',
    #           item.active)

    rand_str = RegisterApp.send_email.get_rand_str(40)
    RegisterApp.send_email.send_register_email(test.email, rand_str)

    test.rand_str = rand_str
    test.save()

    return JsonResponse({'message': "ok"})


def active(request, rand_str):
    if request.method != 'GET':
        return JsonResponse({"error": "require GET"})
    saved_user = User.objects.filter(rand_str=rand_str)
    if not saved_user.exists():
        return JsonResponse({'error:': "no such Register Apply"})
    saved_user = User.objects.get(rand_str=rand_str)
    # print(saved_account.username)
    saved_user.active = 1
    saved_user.rand_str = ''
    saved_user.save()
    # print(saved_account.active)
    return JsonResponse({"message": "ok"})


def get_rand_str(length):
    rand_str = ""
    for i in range(length):
        rand_str += random.choice(string.ascii_letters + string.digits)
    return rand_str


def login(request):
    if request.method != 'POST':
        return JsonResponse({"error": "require POST"})
    all_index = ['username', 'password']
    for index in all_index:
        if index not in request.POST or len(request.POST[index]) == 0:
            return JsonResponse({"error": "invalid parameters"})
    login_username = request.POST['username']
    login_password = request.POST['password']

    # items = User.objects.all()
    # for item in items:
    #     print(item.id, ' ', item.username, ' ', item.password)

    test_exist = User.objects.filter(username=login_username)
    if not test_exist.exists():
        return JsonResponse({"error": "no such a user"})

    saved_user = User.objects.get(username=login_username)
    if login_password != saved_user.password:
        return JsonResponse({"error": "password is wrong"})

    # if len(saved_user.rand_str) > 0:
    #     return JsonResponse({'error': 'has logged in'})

    rand_str = get_rand_str(88)
    saved_user.rand_str = rand_str
    saved_user.save()
    # response = JsonResponse({'message': 'ok'})
    # response.set_cookie('session_id', rand_str)
    response = JsonResponse({'message': 'ok', 'jwt': rand_str})
    return response


def logout(request):
    if request.method != 'POST':
        return JsonResponse({"error": "require POST"})
    print("try to logout")
    print(request.META)
    print(request.META['HTTP_JWT'])
    if not check_login(request):
        return JsonResponse({"error": "please login"})
    # print(request)
    print(request.META['HTTP_JWT'])
    # return JsonResponse({'error': 'TEST'})
    saved_user = User.objects.get(rand_str=request.META['HTTP_JWT'])
    print("success logout: ", saved_user.username)
    response = JsonResponse({'message': 'ok'})
    saved_user.rand_str = ''
    saved_user.save()
    return response


def query_all(request):
    if request.method != 'GET':
        return JsonResponse({"error": "require GET"})

    if not check_login(request):
        return JsonResponse({"error": "please login"})
    saved_user = User.objects.get(rand_str=request.META['HTTP_JWT'])
    if saved_user.authority != 'admin':
        return JsonResponse({"error": "not admin"})
    print("admin querying ALL: ", saved_user.username)

    filt = request.GET['filter']
    page_id = int(request.GET['page'])
    page_size = int(request.GET['page_size'])
    result_list = User.objects.all()
    if filt == 'lessor':
        result_list = User.objects.filter(authority='lessor')
    left = min(len(result_list), (page_id-1)*page_size)
    right = min(len(result_list), page_id*page_size)
    return_list = []
    i = left
    while i < right:
        tmp = result_list[i]
        return_list.append({'username': tmp.username, 'student_id': tmp.student_id, 'user_id': tmp.id,
                            'email': tmp.email, 'contact': tmp.contact, 'authority': tmp.authority,
                            'lab_info': tmp.lab_info})
        i += 1

    # return JsonResponse(json.dumps(return_list, separators=(',', ':'), indent=4))
    return JsonResponse({'total': len(result_list), 'users': return_list})


def set_authority(request):
    if request.method != 'POST':
        return JsonResponse({"error": "require POST"})

    if not check_login(request):
        return JsonResponse({"error": "please login"})
    saved_user = User.objects.get(rand_str=request.META['HTTP_JWT'])
    if saved_user.authority != 'admin':
        return JsonResponse({"error": "not admin"})

    all_index = ['user_id', 'authority']
    for index in all_index:
        if index not in request.POST or len(request.POST[index]) == 0:
            return JsonResponse({"error": "invalid parameters"})
    user_id = request.POST['user_id']
    authority = request.POST['authority']
    if not User.objects.filter(id=user_id).exists():
        return JsonResponse({"error": "no such user"})
    if authority not in ['user', 'lessor']:
        return JsonResponse({"error": "no such authority"})
    set_user = User.objects.get(id=user_id)
    set_user.authority = authority
    set_user.save()

    return JsonResponse({'message': 'ok'})


def delete_user(request):
    if request.method != 'POST':
        return JsonResponse({"error": "require POST"})

    if not check_login(request):
        return JsonResponse({"error": "please login"})
    saved_user = User.objects.get(rand_str=request.META['HTTP_JWT'])
    if saved_user.authority != 'admin':
        return JsonResponse({"error": "not admin"})
    print("admin deleting: ", saved_user.username)
    if 'user_id' not in request.POST or len(request.POST['user_id']) == 0:
        return JsonResponse({"error": "invalid parameters"})
    user_id = request.POST['user_id']
    if not User.objects.filter(id=user_id).exists():
        return JsonResponse({"error": "no such user"})
    del_user = User.objects.get(id=user_id)
    del_user.delete()

    return JsonResponse({'message': 'ok'})


def user_info(request):
    if request.method != 'GET':
        return JsonResponse({"error": "require GET"})

    if not check_login(request):
        return JsonResponse({"error": "please login"})
    user = User.objects.get(rand_str=request.META['HTTP_JWT'])

    return JsonResponse({'user_id': user.id, 'student_id': user.student_id, 'username': user.username,
                         'authority': user.authority})


def decide_auth_request(request):
    if request.method != 'POST':
        return JsonResponse({"error": "require POST"})

    if not check_login(request):
        return JsonResponse({"error": "please login"})
    saved_user = User.objects.get(rand_str=request.META['HTTP_JWT'])
    if saved_user.authority != 'admin':
        return JsonResponse({"error": "not admin"})
    print("admin deciding auth: ", saved_user.username)
    all_index = ['auth_req_id', 'decision']
    for index in all_index:
        if index not in request.POST or len(request.POST[index]) == 0:
            return JsonResponse({"error": "invalid parameters"})
    auth_req_id = request.POST['auth_req_id']
    decision = request.POST['decision']
    if decision not in ['apply', 'reject']:
        return JsonResponse({"error": "no such decision:"+decision})
    if not AuthorityRequest.objects.filter(id=auth_req_id).exists():
        return JsonResponse({"error": "no such auth_request"})
    auth_req = AuthorityRequest.objects.get(id=auth_req_id)
    auth_req.status = decision
    auth_req.save()

    if decision == 'apply':
        req_user = User.objects.get(id=auth_req.user_id)
        req_user.authority = 'lessor'
        req_user.lab_info = auth_req.lab_info
        req_user.save()

    return JsonResponse({'message': 'ok'})


def add_auth_request(request):
    if request.method != 'POST':
        return JsonResponse({"error": "require POST"})

    if not check_login(request):
        return JsonResponse({"error": "please login"})
    saved_user = User.objects.get(rand_str=request.META['HTTP_JWT'])
    if saved_user.authority != 'user':
        return JsonResponse({"error": "not a normal user"})
    print("user requesting auth: ", saved_user.username)
    all_index = ['lab_info', 'detail']
    for index in all_index:
        if index not in request.POST or len(request.POST[index]) == 0:
            return JsonResponse({"error": "invalid parameters"})
    auth_req = AuthorityRequest()
    auth_req.user_id = saved_user.id
    auth_req.username = saved_user.username
    auth_req.lab_info = request.POST['lab_info']
    auth_req.detail = request.POST['detail']
    auth_req.status = 'pending'
    auth_req.save()

    return JsonResponse({'message': 'ok'})


def query_auth_request(request):
    if request.method != 'GET':
        return JsonResponse({"error": "require GET"})

    if not check_login(request):
        return JsonResponse({"error": "please login"})
    saved_user = User.objects.get(rand_str=request.META['HTTP_JWT'])
    # if saved_user.authority != 'admin':
    #     return JsonResponse({"error": "not admin"})
    print("user querying auth_request: ", saved_user.username)

    all_index = ['page', 'page_size', 'status']
    for index in all_index:
        if index not in request.GET or len(request.GET[index]) == 0:
            return JsonResponse({"error": "invalid parameters"})
    if request.GET['status'] not in ['all', 'pending']:
        return JsonResponse({"error": "invalid parameters"})
    page_id = int(request.GET['page'])
    page_size = int(request.GET['page_size'])

    if 'user_id' in request.GET:
        user_id = int(request.GET['user_id'])
        if saved_user.authority != 'admin' and saved_user.id != user_id:
            return JsonResponse({"error": "not admin"})
        if request.GET['status'] == 'all':
            result_list = AuthorityRequest.objects.filter(user_id=user_id)
        else:
            result_list = AuthorityRequest.objects.filter(user_id=user_id, status='pending')
    else:
        if saved_user.authority != 'admin':
            return JsonResponse({"error": "not admin"})
        if request.GET['status'] == 'all':
            result_list = AuthorityRequest.objects.all()
        else:
            result_list = AuthorityRequest.objects.filter(status='pending')
    left = min(len(result_list), (page_id-1)*page_size)
    right = min(len(result_list), page_id*page_size)
    return_list = []
    i = left
    while i < right:
        item = result_list[i]
        # print("TRY!!! ", item.user_id)
        temp_user = User.objects.get(id=item.user_id)
        return_list.append({'auth_req_id': item.id, 'user_id': item.user_id,
                            'username': item.username, 'lab_info': item.lab_info, 'detail': item.detail,
                            'email': temp_user.email, 'contact': temp_user.contact, 'status': item.status})
        i += 1

    # return JsonResponse(json.dumps(return_list, separators=(',', ':'), indent=4))
    return JsonResponse({'total': len(result_list), 'auth_req': return_list})

# def check_login(request):
#     return 'session_id' in request.COOKIES and len(request.COOKIES['session_id']) > 0\
#            and User.objects.filter(rand_str=request.COOKIES['session_id']).exists()


def check_login(request):
    return 'HTTP_JWT' in request.META and User.objects.filter(rand_str=request.META['HTTP_JWT']).exists()
