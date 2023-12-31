from django import forms
from django.contrib.auth.models import User
from .models import UserInfo
from captcha.fields import CaptchaField
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    captcha = CaptchaField(label="Captcha", error_messages={"invalid":u'验证码错误'})
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password",widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm password",widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username","email")

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise  forms.ValidationError("password do not match!")
        return cd['password2']

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ("school","department","age","level","phone","aboutme")

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)

class SearchForm(forms.Form):
    keyword = forms.CharField(label="keyword",max_length=200)