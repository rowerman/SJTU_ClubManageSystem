from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from .forms import UserInfoForm, LoginForm, RegistrationForm, UserForm
from .models import UserInfo
from club.models import InClub
from django.http import JsonResponse
from django.contrib import messages
import tkinter.messagebox
from tkinter import *



def user_login(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])

            if user:
                login(request, user)
                return redirect('/home/')
            else:
                messages.success(request, '用户名或密码错误！')
                return redirect('/account/login/')
        else:
            return HttpResponse("Invalid login!")

    if request.method == "GET":
        login_form = LoginForm()
        return render(request, "registration/login.html", {"form": login_form})


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
    club = InClub.objects.get(member=request.user)
    return render(request, "account/myself.html", {"user": user, "userinfo": userinfo, "club": club})


@login_required(login_url='/account/login/')
def myself_edit(request):
    user = User.objects.get(username=request.user.username)
    userinfo = UserInfo.objects.get(user=request.user)

    if request.method == "POST":
        user_form = UserForm(request.POST)
        userinfo_form = UserInfoForm(request.POST)
        if user_form.is_valid() * userinfo_form.is_valid():
            user_cd = user_form.cleaned_data
            userinfo_cd = userinfo_form.cleaned_data
            print(user_cd["email"])
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
        userinfo_form = UserInfoForm(
            initial={"school": userinfo.school, "age": userinfo.age, "department": userinfo.department
                , "level": userinfo.level, "aboutme": userinfo.aboutme})
        return render(request, "account/myself_edit.html", {"user_form": user_form,
                                                            "userinfo_form": userinfo_form})


@login_required(login_url='/account/login/')
def my_image(request):
    if request.method == "POST":
        img = request.POST['img']
        userInfo = UserInfo.objects.get(user=request.user.id)
        userInfo.photo = img
        userInfo.save()
        return HttpResponse("1")
    else:
        return render(request, 'account/imagecrop.html', )
