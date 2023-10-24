from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.defaulttags import csrf_token
from django.urls import reverse
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from .forms import UserInfoForm, LoginForm, RegistrationForm, UserForm, SearchForm
from .models import UserInfo
from club.models import InClub
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render
from cryptography.hazmat.primitives import hashes
import os
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import  PKCS1_v1_5
import base64
from urllib import parse
from django.shortcuts import render
from django.http import *

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto import Random
import base64

def user_login(request):
    if request.method == "GET":
        # 生成RSA密钥对
        login_form = LoginForm()

        #随机
        gen_random = Random.new().read
        # 生成秘钥
        rsakey = RSA.generate(1024,gen_random)
        public_pem = rsakey.publickey().exportKey()
        private_pem = rsakey.exportKey()
        with open("rsa.private.pem", mode="wb") as f:
            f.write(private_pem)

        # 将公钥设置为Cookie
        response = render(request, 'registration/login.html', {
            'form': login_form,
            'public_key': public_pem.decode('utf-8')
        })
        response.set_cookie('publicKey', public_pem.decode('utf-8'))
        return response
    else:
        login_form = LoginForm(request.POST)  

        if login_form.is_valid():
                            
            cd = login_form.cleaned_data
            password = cd['password']
            with open("rsa.private.pem", mode="r") as f:
                    prikey = f.read()
                    rsa_pk = RSA.importKey(prikey)
                    rsa = PKCS1_v1_5.new(rsa_pk)
                    result = rsa.decrypt(base64.b64decode(password), None)
            user = authenticate(username=cd['username'],password=result.decode("utf-8"))

            if user:
                login(request, user)
                return redirect('/home/homepage/')
            else:
                messages.success(request, '用户名或密码错误！')
                return redirect('/account/login/')
        else:
            return HttpResponse("Invalid login!")

def register(request):
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            print("1")
            UserInfo.objects.create(user=new_user)
            return HttpResponseRedirect(reverse('account:user_login'))
        else:
            messages.success(request, '对不起，您不能登录！')
            return redirect('/account/register/')
    else:
        user_form = RegistrationForm()
        return render(request, "account/register.html", {"form": user_form})


@login_required(login_url='/account/login/')
def myself(request):
    user = User.objects.get(username=request.user.username)
    userinfo = UserInfo.objects.get(user=user)
    try:
        club = InClub.objects.get(member=request.user)
    except:
        club = None
    return render(request,"account/myself.html",{"user1":user,"userinfo":userinfo,"club":club})

@login_required(login_url='/account/login/')
def myself_version(request,user_id):
    user = User.objects.get(id=user_id)
    userinfo = UserInfo.objects.get(user=user)
    try:
        club = InClub.objects.get(member=user)
    except:
        club = None
    return render(request,"account/myself_SeeOnly.html",{"user1":user,"userinfo":userinfo,"club":club})

@login_required(login_url='/account/login/')
def myself_edit(request):
    user = User.objects.get(username=request.user.username)
    userinfo = UserInfo.objects.get(user=request.user)

    if request.method == "POST":
        user_form = UserForm(request.POST)
        userinfo_form = UserInfoForm(request.POST)
        if user_form.is_valid()*userinfo_form.is_valid():
            user_cd = user_form.cleaned_data
            userinfo_cd = userinfo_form.cleaned_data
            user.email = user_cd["email"]
            userinfo.school = userinfo_cd["school"]
            userinfo.department = userinfo_cd["department"]
            userinfo.age = userinfo_cd["age"]
            userinfo.level = userinfo_cd["level"]
            userinfo.aboutme = userinfo_cd["aboutme"]
            user.save()
            userinfo.save()
        return HttpResponseRedirect('/account/my-information')
    else:
        user_form = UserForm(instance=request.user)
        userinfo_form = UserInfoForm(initial={"school":userinfo.school,"age":userinfo.age,"department":userinfo.department
                                              ,"level":userinfo.level,"aboutme":userinfo.aboutme})
        return render(request,"account/myself_edit.html",{"user_form":user_form,
                                                          "userinfo_form":userinfo_form,"userinfo":userinfo})

@login_required(login_url='/account/login/')
def my_image(request):
    if request.method == "POST":
        img = request.POST['img']
        userInfo = UserInfo.objects.get(user=request.user.id)
        userInfo.photo = img
        userInfo.save()
        return HttpResponse("1")
    else:
        return render(request,'account/imagecrop.html',)

@login_required(login_url='/account/login/')
@csrf_exempt
def search(request):
    if request.method == "GET":
        type = "1"
        search_form = SearchForm()
        return render(request,"account/search.html",{"search_form":search_form,"type":type})
    else:
        type = "2"
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            keyword = request.POST['keyword']
            results = User.objects.filter(username__icontains=keyword)
            if results:
                return render(request,"account/search.html",{"search_form":search_form,"results":results,"type":type})
            else:
                results = User.objects.none()
                return render(request,"account/search.html",{"search_form":search_form,"results":results,"type":type})
        else:
            return HttpResponse("2")       #表单错误


