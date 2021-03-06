"""
账户相关功能：注册，短信，登录，注销
"""
import datetime
import uuid

from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from web import models
from web.forms.account import RegisterModelForm, SendSmsForm, LoginSMSForm, LoginForm


def register(request):
    """注册"""
    if request.method == 'GET':
        form = RegisterModelForm()
        return render(request, 'register.html', {'form': form})

    form = RegisterModelForm(data=request.POST)
    if form.is_valid():
        # 验证通过，写入数据库（密码要先加密）
        # instance = models.UserInfo.objects.create(**form.cleaned_data) 这个包含重复密码等数据，要写入的话或报错，需要提出再写入
        instance = form.save()  # form.save()可以过滤掉不需要的数据

        # policy_object = models.PricePolicy.objects.filter(category=1, title='个人免费版').first()
        # 创建交易记录,方式一：
        # models.Transaction.objects.create(
        #     status=2,
        #     order=str(uuid.uuid4()),
        #     user=instance,
        #     policy_object=policy_object,
        #     count=0,
        #     price=0,
        #     start_datetime=datetime.datetime.now()
        # )
        return JsonResponse({'status': True, 'data': '/Login/'})

    return JsonResponse({'status': False, 'error': form.errors})


def send_sms(request):
    """发送短信"""
    form = SendSmsForm(request, data=request.GET)
    # 只验证手机号：不能为空，格式是否正确
    if form.is_valid():
        # 校验通过之后
        # 发短信
        # 写redis
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


def login_sms(request):
    """短信登录"""
    if request.method == 'GET':
        form = LoginSMSForm()
        return render(request, 'login_sms.html', {'form': form})

    form = LoginSMSForm(request.POST)
    if form.is_valid():
        # 用户输入正确输入成功
        user_object = form.cleaned_data['mobile_phone']

        # 用户信息存入session
        request.session['user_id'] = user_object.id
        request.session.set_expiry(60 * 60 * 24 * 14)

        return JsonResponse({'status': True, 'data': '/index/'})

    return JsonResponse({'status': False, 'data': form.errors})


def login(request):
    """用户名和密码登录"""
    if request.method == 'GET':
        form = LoginForm(request)
        return render(request, 'login.html', {'form': form})
    form = LoginForm(request, data=request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user_object = models.UserInfo.objects.filter(Q(email=username) | Q(mobile_phone=username)).filter(
            password=password).first()

        if user_object:
            # 用户名密码正确
            # 用户信息存入session
            request.session['user_id'] = user_object.id
            request.session.set_expiry(60*60*24*14)

            return redirect('web:index')

        form.add_error('username', '用户名或密码错误')

    return render(request, 'login.html', {'form': form})


def logout(request):
    request.session.flush()
    return redirect('web:index')


def image_code(request):
    """生成图片验证码"""
    from io import BytesIO
    from utils.imgcode.image_code import check_code

    image_object, code = check_code()

    # 写到session中
    request.session['image_code'] = code
    # 设置过期时间
    request.session.set_expiry(60)

    stream = BytesIO()
    image_object.save(stream, 'png')

    return HttpResponse(stream.getvalue())



