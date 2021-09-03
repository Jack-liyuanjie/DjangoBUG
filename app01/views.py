import re

from django.shortcuts import render, HttpResponse
import random

from utils.tencent.sms import send_sms_single
from django.conf import settings


def send_sms(request):
    """ 发送短信
        ?tpl=login  -> 1080886
        ?tpl=register -> 1080888
    """
    tpl = request.GET.get('tpl')
    template_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)
    if not template_id:
        return HttpResponse('模板不存在')

    code = random.randrange(1000, 9999)
    res = send_sms_single('13267886101', template_id, [code, ])

    if res['result'] == 0:
        return HttpResponse('成功')
    else:
        return HttpResponse(res['errmsg'])


from app01 import models
from django import forms
from django.core.exceptions import ValidationError


class UserValidator:
    @classmethod
    def valid_phone(cls, value):
        if not re.match(r'1[1-57-9]\d{9}', value):
            raise ValidationError('手机格式不正确')
        return True


class RegisterModelForm(forms.ModelForm):
    mobile_phone = forms.CharField(max_length=11,
                                   validators=[UserValidator.valid_phone],
                                   label='手机号',
                                   )

    password = forms.CharField(widget=forms.PasswordInput(),
                               label='密码', )

    confirm_password = forms.CharField(widget=forms.PasswordInput(),
                                       label='重复密码')

    code = forms.CharField(label='验证码')

    class Meta:
        model = models.UserInfo
        fields = ['username', 'email', 'password', 'confirm_password', 'mobile_phone', 'code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入%s' % field.label


def register(request):
    form = RegisterModelForm()
    return render(request, 'app01/register.html', {'form': form})
