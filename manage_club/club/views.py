from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST
from .models import message
from .forms import ClubCreateForm
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import InClub,Club
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .forms import messageForm
from django.db.models import Q

@login_required(login_url='/account/login')
@csrf_exempt
def create_club(request):
    if request.method == "GET":
        club_form = ClubCreateForm()
        return render(request,"club/create_club.html",{"club_form":club_form})
    else:
        club_form = ClubCreateForm(request.POST)
        if club_form.is_valid():
            new_club = club_form.save(commit=False)
            new_club.lead_name = request.user.username
            new_club.save()
            return HttpResponseRedirect(reverse('club:list_club'))
        else:
            return HttpResponse("The input in invalid~")

@login_required(login_url='/account/login')
@require_GET
def list_club(request):

    clubs = Club.objects.all()
    paginator = Paginator(clubs,3)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        clubs = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        clubs = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        clubs = current_page.object_list

    return render(request,"club/list_club.html",{"clubs":clubs,"page":current_page})

@login_required(login_url='/account/login')
@require_GET
def list_club_detail(request,club_id):
    clubInfo = Club.objects.get(id=club_id)
    return render(request,"club/club_detail.html",{"club":clubInfo})

@login_required(login_url='account/login')
@csrf_exempt
def send_message(request):
    if request.method == "POST":
        message_form = messageForm(data=request.POST)
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.sender = request.user
            try:
                receiver = User.objects.get(username=message.receiver_name)
                message.reciver = receiver
                message.save()
                return HttpResponseRedirect(reverse("club:my_send"))
            except:
                return HttpResponse("用户不存在！")
        else:
            return HttpResponse("2")
    else:
        message_form = messageForm()
        return render(request, 'club/send_message.html',{"message_form":message_form})

@login_required(login_url='account/login')
def my_send(request):
    messages = message.objects.filter(sender=request.user)
    paginator = Paginator(messages,3)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        messages = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        messages = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        messages = current_page.object_list
    return render(request,"club/my_send.html",{"messages":messages,"page":current_page})

@login_required(login_url='account/login')
def my_send_type(request,type):
    if type == 1:
        messages = message.objects.filter(Q(sender=request.user)&Q(receiver_read=True))
    else:
        messages = message.objects.filter(Q(sender=request.user)&Q(receiver_read=False))
    paginator = Paginator(messages,3)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        messages = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        messages = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        messages = current_page.object_list
    return render(request,"club/my_send.html",{"messages":messages,"page":current_page})

@login_required(login_url='account/login')
def my_recceived(request):
    messages = message.objects.filter(reciver=request.user)
    paginator = Paginator(messages,3)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        messages = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        messages = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        messages = current_page.object_list
    return render(request,"club/my_receive.html",{"messages":messages,"page":current_page})

@login_required(login_url='account/login')
def message_detail(request,message_id):
    Message = message.objects.get(id=message_id)
    Message.receiver_read = True
    Message.save()
    return render(request,"club/message_detail.html",{"Message":Message})


@login_required(login_url='/account/login')
@csrf_exempt
def join_club(request,club_id):
    club = Club.objects.get(id=club_id)
    try:
        inclub = InClub.objects.get(member=request.user)
        inclub.In_club.add(club)
        inclub.save()
        return HttpResponseRedirect(reverse('club:my_club'))
    except:
        inclub = InClub()
        inclub.member = request.user
        inclub.save()
        inclub.In_club.add(club)
        inclub.save()
        return HttpResponse("2")

@login_required(login_url='account/login')
@require_GET
def confirm_join(request,club_id):
    club = Club.objects.get(id=club_id)
    return render(request,"club/confirm_join.html",{"club":club})

@login_required(login_url='/account/login')
def my_club(request):
    clubs = InClub.objects.get(member=request.user)
    return render(request,"club/my_club.html",{"clubs":clubs})


