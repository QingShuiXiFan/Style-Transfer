# 存放各种与表单有关的类
from django import forms
from django.contrib.auth.models import User  # Django 默认的用户模型User类
from captcha.fields import CaptchaField


# 登录表单类
class LoginForm(forms.Form):
    # username = forms.CharField() # 相当于<input name='username' type='text' ...>
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=256,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))  # 用widget来规定相应HTML元素的类型
    captcha = CaptchaField(label='验证码')


class RegistrationForm(forms.ModelForm):  # ModelForm是和该应用Model相关的类
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:  # 内部类，
        model = User
        fields = ("email", "username")
