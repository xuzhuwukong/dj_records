#!/usr/bin/env python
# coding:utf-8
from django import forms
from django.forms import widgets
from django.contrib.auth.models import User

wid01 = widgets.PasswordInput()
wid02 = widgets.TextInput()


# 检测登陆或注册页面表单字段的合法性
class LoginCheck(forms.Form):
    id_username = forms.CharField(min_length=2, label="用户名")
    id_password = forms.CharField(min_length=3, label="密码", widget=wid01)


class RegCheck(forms.Form):
    id_username = forms.CharField(min_length=2, label="用户名")
    id_password = forms.CharField(min_length=3, label="密码", widget=wid01)
    id_password2 = forms.CharField(min_length=3, label="确认密码", widget=wid01)


class CheckPublish(forms.Form):
    publish_name = forms.CharField(min_length=2)
    #publish_email = forms.EmailField()
    #publish_addr = forms.CharField(min_length=2)


class CheckBook(forms.Form):
    pass


class CheckAuthor(forms.Form):
    pass
