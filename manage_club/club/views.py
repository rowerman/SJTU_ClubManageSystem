from itertools import chain
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST
from .models import message, Activity
from .forms import ClubCreateForm, ActivityForm
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import InClub,Club
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .forms import messageForm
from django.db.models import QuerySet
from .forms import ClubForm

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

            try:
                inclub = InClub.objects.get(member=request.user)
                inclub.In_club.add(new_club)
                inclub.save()
            except:
                inclub = InClub()
                inclub.member = request.user
                inclub.save()
                inclub.In_club.add(new_club)

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
        club.num_of_mem = club.num_of_mem + 1
        club.save()
    except:
        inclub = InClub()
        inclub.member = request.user
        inclub.save()
        inclub.In_club.add(club)

        club.num_of_mem = club.num_of_mem + 1
        club.save()
    return HttpResponseRedirect(reverse('club:my_club'))

@login_required(login_url='account/login')
@require_GET
def confirm_join(request,club_id):
    club = Club.objects.get(id=club_id)
    return render(request,"club/confirm_join.html",{"club":club})

@login_required(login_url='/account/login')
def my_club(request):
    try:
        inclubs = InClub.objects.get(member_id=request.user.id)
    except:
        inclubs = None
    if inclubs:
        clubs = inclubs.In_club.all()
    else:
        clubs = Club.objects.none()
    print(clubs)
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
    return render(request,"club/my_club.html",{"clubs":clubs,"page":current_page})

@login_required(login_url='/account/login')
def manage_Myclub(request):
    if request.method == "GET":
        clubs = Club.objects.filter(lead_name=request.user.username)
        paginator = Paginator(clubs, 3)
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
        return render(request,"club/manage_Myclub.html",{"clubs":clubs,"page":current_page})

@login_required(login_url='/account/login')
@require_GET
def manage_member(request,club_id):
    club = Club.objects.get(id=club_id)
    tmp = club.In_club.all()
    commons = User.objects.filter(member__in=tmp).distinct()
    print(commons)
    paginator = Paginator(commons, 8)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        members = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        members = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        members = current_page.object_list
    return render(request,"club/manage_member.html",{"club":club,"commons":commons,"page":current_page})

@login_required(login_url='/account/login')
@csrf_exempt
def delete_member(request,club_id):
    member_id = request.POST["member_id"]
    club = Club.objects.get(id=club_id)
    try:
        ThemanInclub = InClub.objects.get(member_id=member_id)
        ThemanInclub.delete()
        club.num_of_mem = club.num_of_mem - 1
        club.save()
        return HttpResponse("1")
    except:
        return HttpResponse("2")

@login_required(login_url='account/login')
def manage_clubInfo(request,club_id):
    club = Club.objects.get(id=club_id)
    if request.method == "GET":
        club_form = ClubForm(initial={"name":club.name,"club_id":club.club_id,"Aboutme":club.Aboutme})
        return render(request,"club/manage_clubInfo.html",{"club_form":club_form,"club":club})
    else:
        club_form = ClubForm(request.POST)
        print(club_form)
        if club_form.is_valid():
            club_cd = club_form.cleaned_data
            club.name = club_cd['name']
            club.club_id = club_cd['club_id']
            club.Aboutme = club_cd['Aboutme']
            club.save()
            return HttpResponseRedirect(reverse('club:manage_clubInfo',args=[club_id]))
        else:
            return HttpResponse("Form error!")

@login_required(login_url='/account/login/')
def club_image(request,club_id):
    if request.method == "POST":
        img = request.POST['img']
        club = Club.objects.get(id=club_id)
        club.photo = img
        club.save()
        return HttpResponse("1")
    else:
        club = Club.objects.get(id=club_id)
        return render(request,'club/imagecrop.html',{"club":club})


@login_required(login_url='/account/login/')
def create_activity(request,club_id):
    club = Club.objects.get(id=club_id)
    if request.method == "GET":
        activity_form = ActivityForm()
        return render(request,"club/create_activity.html",{"activity_form":activity_form,"club":club})
    else:
        activity_form = ActivityForm(request.POST)
        if activity_form.is_valid():
            activity = activity_form.save(commit=False)
            activity.belong = club
            activity.save()
            return HttpResponseRedirect(reverse('club:list_activity',args=[club_id]))
        else:
            return HttpResponse("errorForm!")

@login_required(login_url='/account/login/')
def list_activity(request,club_id):
    club = Club.objects.get(id=club_id)
    activities = club.launch.all()
    paginator = Paginator(activities, 4)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        activities = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        activities = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        activities = current_page.object_list
    return render(request,"club/list_activity.html",{"activities":activities,"club":club,"page":current_page})

@login_required(login_url='/account/login/')
@require_GET
def activity_detail(request,activity_id,club_id):
    activity = Activity.objects.get(id=activity_id)
    return render(request,"club/activity_detail.html",{"activity":activity,"club_id":club_id})

@login_required(login_url='/account/login/')
@require_GET
def activity_detail_version(request,activity_id):
    activity = Activity.objects.get(id=activity_id)
    return render(request,"club/activity_detail_version.html",{"activity":activity})

@login_required(login_url='/account/login/')
@csrf_exempt
def delete_activity(request):
    activity_id = request.POST['activity_id']
    activity = Activity.objects.get(id=activity_id)
    try:
        activity.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")

@login_required(login_url='account/login')
def all_activity(request):
    activities = Activity.objects.all()
    paginator = Paginator(activities, 4)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        activities = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        activities = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        activities = current_page.object_list

    return render(request,"club/all_activity.html",{"activities":activities,"page":current_page})

@login_required(login_url='/account/login')
@csrf_exempt
@require_POST
def fan_Club(request):
    club_id = request.POST.get("id")
    action = request.POST.get("action")
    if club_id and action:
        try:
            club = Club.objects.get(id=club_id)
            if action == "follow":
                club.fans.add(request.user)
                return HttpResponse("1")
            else:
                club.fans.remove(request.user)
                return HttpResponse("2")
        except:
            return HttpResponse("no!")










