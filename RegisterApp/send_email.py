import random
import string
from django.core.mail import send_mail
from django.conf import settings


def get_rand_str(length):
    rand_str = ""
    for i in range(length):
        rand_str += random.choice(string.ascii_letters + string.digits)
    return rand_str


def send_register_email(to, rand_str):
    title = "注册激活链接"
    body = "请点击下面的链接激活你的账号: http://127.0.0.1:8000/api/active/{0}".format(rand_str)
    print(body)
    send_mail(title, body, settings.DEFAULT_FROM_EMAIL, [to])
