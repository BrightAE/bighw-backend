from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
from UserApp.models import User
from django.contrib.auth.hashers import make_password, check_password
import RegisterApp.send_email
import random
import string
import time

# from django.views.decorators.csrf import csrf_exempt


def hello_world(request):
    return HttpResponse("<h1>Hello world !</h1>")


# @csrf_exempt
def logon(request):
    if request.method != 'POST':
        return JsonResponse({"error": "require POST"})
    all_index = ['username', 'password', 'student_id', 'email', 'contact']
    for index in all_index:
        if index not in request.Post or len(request.POST[index]) == 0:
            return JsonResponse({"error": "invalid parameters"})

    input_username = request.POST['username']
    input_password = request.POST['password']
    input_email = request.POST['email']
    input_student_id = int(request.POST['id'])
    input_contact = request.POST['contact']

    items = User.objects.all()
    for item in items:
        if item.student_id == input_student_id or item.username == input_username:
            return JsonResponse({"error": "user exists"})

    test = User()
    test.username = input_username
    test.password = make_password(input_password)
    test.student_id = input_student_id
    test.email = input_email
    test.contact = input_contact
    test.authority = 'user'
    test.active = False
    test.lab_info = ''
    test.rand_str = ''
    test.save()

    items = User.objects.all()
    for item in items:
        print(item.id, ' ', item.username, ' ', item.password, ' ', item.email, ' ', item.student_id, ' ', item.authority, ' ',
              item.active)

    rand_str = RegisterApp.send_email.get_rand_str(40)
    RegisterApp.send_email.send_register_email(test.mail, rand_str)

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
        if index not in request.Post or len(request.POST[index]) == 0:
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

    if len(saved_user.rand_str) > 0:
        return JsonResponse({'error': 'has logged in'})

    rand_str = get_rand_str(88)
    saved_user.rand_str = rand_str
    saved_user.save()
    response = JsonResponse({'message': 'ok'})
    response.set_cookie('session_id', rand_str)
    return response


def logout(request):
    if request.method != 'POST':
        return JsonResponse({"error": "require POST"})
    print(request)
    print(request.COOKIES['session_id'])

    saved_user = User.objects.filter(rand_str=request.COOKIES['session_id'])
    if saved_user.exists():
        saved_user = User.objects.get(rand_str=request.COOKIES['session_id'])
        print("success logout: ", saved_item.username)
        response = JsonResponse({saved_item.username: "the-old-user-name"})
        saved_item.delete()
        return response

    return JsonResponse({'error': 'no valid session'})
#
#
#
# def logout(request):
#     if request.method != 'POST':
#         return JsonResponse({"error": "require POST"})
#     print(request)
#     print(request.COOKIES['session_id'])
#
#     saved_session = MySession.objects.filter(sessionID=request.COOKIES['session_id'])
#     if saved_session.exists():
#         saved_item = MySession.objects.get(sessionID=request.COOKIES['session_id'])
#         print("success logout: ", saved_item.username)
#         response = JsonResponse({saved_item.username: "the-old-user-name"})
#         saved_item.delete()
#         return response
#
#     return JsonResponse({'error': 'no valid session'})
#
#
# def record_add(request):
#     if request.method != 'POST':
#         return JsonResponse({"error": "require POST"})
#     if ('name' not in request.POST) or ('time' not in request.POST) or ('content' not in request.POST):
#         return JsonResponse({'error': 'invalid parameters'})
#
#     saved_session = MySession.objects.filter(sessionID=request.COOKIES['session_id'])
#     if not saved_session.exists():
#         return JsonResponse({"error": "please login"})
#     saved_session = MySession.objects.get(sessionID=request.COOKIES['session_id'])
#     print("user adding record: ", saved_session.username)
#     add_name = request.POST['name']
#     add_time = request.POST['time']
#     add_content = request.POST['content']
#     if min(len(add_name), len(add_content)) == 0:
#         return JsonResponse({'error': 'invalid parameters'})
#     print(type(add_time))
#     try:
#         add_time = int(add_time)
#     except:
#         return JsonResponse({'error': 'invalid parameters'})
#     if add_time <= 0:
#         return JsonResponse({'error': 'invalid parameters'})
#     temp = MyData()
#     temp.name = add_name
#     temp.time = add_time
#     temp.content = add_content
#     temp.user = saved_session.username
#     temp.save()
#
#     items = MyData.objects.all()
#     for item in items:
#         print(item.id, ' ', item.name, ' ', item.time, ' ', item.content, ' ', item.user)
#
#     return JsonResponse({'record_id': temp.id})
#
#
# def record_delete(request, del_id):
#     if request.method != 'POST':
#         return JsonResponse({"error": "require POST"})
#
#     saved_session = MySession.objects.filter(sessionID=request.COOKIES['session_id'])
#     if not saved_session.exists():
#         return JsonResponse({"error": "please login"})
#     saved_session = MySession.objects.get(sessionID=request.COOKIES['session_id'])
#     print("user deleting record: ", saved_session.username)
#
#     try:
#         del_id = int(del_id)
#     except:
#         return JsonResponse({'error': 'invalid parameters'})
#     if del_id <= 0:
#         return JsonResponse({'error': 'invalid parameters'})
#
#     saved_data = MyData.objects.filter(id=del_id)
#     if not saved_data.exists():
#         return JsonResponse({"error": "unknown record"})
#     saved_data = MyData.objects.get(id=del_id)
#     print("content to delete:  ", saved_data.content)
#     print("    time:  ", saved_data.time)
#     if (saved_data.time == -233) or (saved_data.user != saved_session.username):
#         return JsonResponse({"error": "unknown record"})
#     saved_data.time = -233
#     saved_data.save()
#     return JsonResponse({'record_id': del_id})
#
#
# def record_update(request, upd_id):
#     if request.method != 'POST':
#         return JsonResponse({"error": "require POST"})
#
#     saved_session = MySession.objects.filter(sessionID=request.COOKIES['session_id'])
#     if not saved_session.exists():
#         return JsonResponse({"error": "please login"})
#     saved_session = MySession.objects.get(sessionID=request.COOKIES['session_id'])
#     print("user updating record: ", saved_session.username)
#
#     try:
#         upd_id = int(upd_id)
#     except:
#         return JsonResponse({'error': 'invalid parameters'})
#     if upd_id <= 0:
#         return JsonResponse({'error': 'invalid parameters'})
#
#     saved_data = MyData.objects.filter(id=upd_id)
#     if not saved_data.exists():
#         return JsonResponse({"error": "unknown record"})
#     saved_data = MyData.objects.get(id=upd_id)
#     print("content to update:  ", saved_data.content)
#     print("    time:  ", saved_data.time)
#     if (saved_data.time == -233) or (saved_data.user != saved_session.username):
#         return JsonResponse({"error": "unknown record"})
#
#     for index in request.POST:
#         if index != 'name' and index != 'time' and index != 'content':
#             return JsonResponse({"error": "unknown record filed"})
#         # print(index)
#
#     for index in request.POST:
#         if index == 'name':
#             saved_data.name = request.POST['name']
#         if index == 'time':
#             saved_data.time = request.POST['time']
#         if index == 'content':
#             saved_data.content = request.POST['content']
#
#     saved_data.save()
#
#     items = MyData.objects.all()
#     for item in items:
#         print(item.id, ' ', item.name, ' ', item.time, ' ', item.content, ' ', item.user)
#     return JsonResponse({'record_id': upd_id})
#
#
# def record_get(request, get_id):
#     if request.method != 'GET':
#         return JsonResponse({"error": "require GET"})
#
#     saved_session = MySession.objects.filter(sessionID=request.COOKIES['session_id'])
#     if not saved_session.exists():
#         return JsonResponse({"error": "please login"})
#     saved_session = MySession.objects.get(sessionID=request.COOKIES['session_id'])
#     print("user getting record: ", saved_session.username)
#
#     saved_data = MyData.objects.filter(id=get_id)
#     if not saved_data.exists():
#         return JsonResponse({"error": "unknown record"})
#     saved_data = MyData.objects.get(id=get_id)
#     if (saved_data.time == -233) or (saved_data.user != saved_session.username):
#         return JsonResponse({"error": "unknown record"})
#
#     return JsonResponse({'record_id': get_id, 'name': saved_data.name, 'content': saved_data.content,
#                          'time': get_peking_time(saved_data.time)})
#
#
# def record_query(request):
#     if request.method != 'GET':
#         return JsonResponse({"error": "require GET"})
#
#     saved_session = MySession.objects.filter(sessionID=request.COOKIES['session_id'])
#     if not saved_session.exists():
#         return JsonResponse({"error": "please login"})
#     saved_session = MySession.objects.get(sessionID=request.COOKIES['session_id'])
#     print("user querying record: ", saved_session.username)
#
#     upd_name = request.GET.get('name')
#     result_list = []
#     if upd_name is None or len(upd_name) == 0:
#         items = MyData.objects.all()
#         for item in items:
#             if item.time >= 0:
#                 result_list.append({'record_id': item.id, 'name': item.name, 'content': item.content,
#                                     'time': get_peking_time(item.time)})
#     else:
#         items = MyData.objects.all()
#         for item in items:
#             if item.name.find(upd_name) >= 0 and item.time >= 0:
#                 # print(item.time,"type:",type(item.time))
#                 result_list.append({'record_id': item.id, 'name': item.name, 'content': item.content,
#                                     'time': get_peking_time(item.time)})
#
#     return JsonResponse({'list': result_list})
#
#
# # def invalid_url():
# #     return HttpResponse(status=404)
#
#
# def get_rand_str(length):
#     rand_str = ""
#     for i in range(length):
#         rand_str += random.choice(string.ascii_letters + string.digits)
#     return rand_str
#
#
# def create_session(rand_str, username):
#     print("CREATING:  ", username, ' ', rand_str)
#     temp = MySession()
#     temp.sessionID = rand_str
#     temp.username = username
#     temp.save()
#
#     items = MySession.objects.all()
#     for item in items:
#         print(item.sessionID, ' ', item.username)
#
#
# def get_peking_time(num):
#     time_stamp = num/1000.0
#     time_array = time.localtime(time_stamp)
#     # print(time_array)
#     style_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array) + '.' + str(num%1000).zfill(3)
#     # print(style_time)
#     return style_time
