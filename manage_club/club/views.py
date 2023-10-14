from itertools import chain
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST
from .models import message, Activity
from .forms import ClubCreateForm, ActivityForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import InClub,Club,Advertisement
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .forms import messageForm
from django.db.models import QuerySet, Q
from .forms import ClubForm,CreateAdvertisementForm,AdvertisementForm
from account.forms import SearchForm

@login_required(login_url='/account/login/')
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
            new_club.leader = request.user
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

@login_required(login_url='/account/login/')
def list_club(request):
    if request.method == "GET":
        search_form = SearchForm()
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

        return render(request,"club/list_club.html",{"clubs":clubs,"page":current_page,"search_form":search_form})
    else:
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            keyword = request.POST['keyword']
            try:
                clubs = Club.objects.filter(name__icontains=keyword)
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
                return render(request, "club/list_club.html",
                              {"search_form": search_form, "clubs": clubs, "page": current_page})
            except:
                clubs = Club.objects.none()
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
                return render(request,"club/list_club.html",
                              {"search_form": search_form, "clubs": clubs, "page": current_page})
        else:
            return HttpResponse("1")
@login_required(login_url='/account/login/')
@require_GET
def list_club_detail(request,club_id):
    club = Club.objects.get(id=club_id)
    name = request.user.username
    user = User.objects.get(id=request.user.id)
    theman = InClub.objects.get(member=user)
    members = club.In_club.all()
    if theman in members:
        type = "1"
    else:
        type = "2"

    return render(request,"club/club_detail.html",{"club":club,"type":type,"name":name})

@login_required(login_url='/account/login/')
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

@login_required(login_url='/account/login/')
def my_send(request):
    if request.method == "GET":
        search_form = SearchForm()
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
        return render(request,"club/my_send.html",{"messages":messages,"page":current_page,"search_form":search_form})
    else:
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            keyword = request.POST['keyword']
            try:
                messages = message.objects.filter(receiver_name=keyword)
                paginator = Paginator(messages, 3)
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
                return render(request,"club/my_send.html",{"search_form":search_form,"messages":messages,"page":current_page})
            except:
                messages = message.objects.none()
                paginator = Paginator(messages, 3)
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
                return render(request,"club/my_send.html",{"search_form":search_form,"messages":messages,"page":current_page})
        else:
            return HttpResponse("2")       #表单错误


@login_required(login_url='/account/login/')
def my_send_type(request,type):
    if request.method == "GET":
        search_form = SearchForm()
        if type == "1":
            messages = message.objects.filter(sender=request.user,receiver_read="yes")
        else:
            messages = message.objects.filter(sender=request.user,receiver_read="no")
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
        return render(request,"club/my_send_type.html",{"messages":messages,"page":current_page,"search_form":search_form,"type":type})
    else:
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            keyword = request.POST['keyword']
            if type == "1":
                try:
                    messages = message.objects.filter(receiver_name=keyword,receiver_read="yes")
                    paginator = Paginator(messages, 3)
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
                    return render(request,"club/my_send_type.html",{"search_form":search_form,"messages":messages,"page":current_page,"type":type})
                except:
                    messages = message.objects.none()
                    paginator = Paginator(messages, 3)
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
                    return render(request,"club/my_send_type.html",{"search_form":search_form,"messages":messages,"page":current_page,"type":type})
            else:
                try:
                    messages = message.objects.filter(receiver_name=keyword,receiver_read="no")
                    paginator = Paginator(messages, 3)
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
                    return render(request,"club/my_send.html",{"search_form":search_form,"messages":messages,"page":current_page,"type":type})
                except:
                    messages = message.objects.none()
                    paginator = Paginator(messages, 3)
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
                    return render(request,"club/my_send.html",{"search_form":search_form,"messages":messages,"page":current_page,"type":type})
        else:
            return HttpResponse("2")       #表单错误


@login_required(login_url='/account/login/')
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

@login_required(login_url='/account/login/')
def message_detail(request,message_id):
    Message = message.objects.get(id=message_id)
    Message.receiver_read = "yes"
    Message.save()
    return render(request,"club/message_detail.html",{"Message":Message})


@login_required(login_url='/account/login/')
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
    return HttpResponseRedirect(reverse('club:list_club'))

@login_required(login_url='/account/login/')
@csrf_exempt
def exit_club(request):
    club_id = request.POST['club_id']
    club = Club.objects.get(id=club_id)
    club.num_of_mem = club.num_of_mem - 1
    inclub = InClub.objects.get(member=request.user)
    club.In_club.remove(inclub)
    club.save()
    return HttpResponse("1")


@login_required(login_url='/account/login/')
@require_GET
def confirm_join(request,club_id):
    club = Club.objects.get(id=club_id)
    return render(request,"club/confirm_join.html",{"club":club})

@login_required(login_url='/account/login/')
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

@login_required(login_url='/account/login/')
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

@login_required(login_url='/account/login/')
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

@login_required(login_url='/account/login/')
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

@login_required(login_url='/account/login/')
def manage_clubInfo(request,club_id):
    club = Club.objects.get(id=club_id)
    if request.method == "GET":
        club_form = ClubForm(initial={"name":club.name,"club_id":club.club_id,"Aboutme":club.Aboutme})
        return render(request,"club/manage_clubInfo.html",{"club_form":club_form,"club":club})
    else:
        club_form = ClubForm(request.POST)
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

@login_required(login_url='/account/login/')
def all_activity(request):
    if request.method == "GET":
        search_form = SearchForm()
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

        return render(request,"club/all_activity.html",{"activities":activities,"page":current_page,"search_form":search_form})
    else:
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            keyword = request.POST['keyword']
            try:
                activites = Activity.objects.filter(Q(name__icontains=keyword) or Q(belong__name__icontains=keyword))
                paginator = Paginator(activites, 3)
                page = request.GET.get('page')
                try:
                    current_page = paginator.page(page)
                    activites = current_page.object_list
                except PageNotAnInteger:
                    current_page = paginator.page(1)
                    activites = current_page.object_list
                except EmptyPage:
                    current_page = paginator.page(paginator.num_pages)
                    activites = current_page.object_list
                return render(request,"club/all_activity.html",
                              {"search_form":search_form,"page":current_page,"activities":activites})
            except:
                activites = message.objects.none()
                paginator = Paginator(activites, 3)
                page = request.GET.get('page')
                try:
                    current_page = paginator.page(page)
                    activites = current_page.object_list
                except PageNotAnInteger:
                    current_page = paginator.page(1)
                    activites = current_page.object_list
                except EmptyPage:
                    current_page = paginator.page(paginator.num_pages)
                    activites = current_page.object_list
                return render(request,"club/all_activity.html",{"search_form":search_form,"activites":activites,"page":current_page})
        else:
            return HttpResponse("errorForm!")

@login_required(login_url='/account/login/')
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

@login_required(login_url='/account/login/')
@csrf_exempt
def create_ad(request,club_id):
    if request.method == "GET":
        create_add_form = CreateAdvertisementForm()
        return render(request,"club/create_ad.html",{"form":create_add_form})
    else:
        club = Club.objects.get(id=club_id)
        create_ad_form = CreateAdvertisementForm(request.POST,request.FILES)
        if create_ad_form.is_valid():
            new_ad = create_ad_form.save(commit=False)
            new_ad.owner = club
            new_ad.save()
            return redirect("club:list_ads",club_id)

@login_required(login_url='/account/login/')
def list_ads(request,club_id):
    if request.method == "GET":
        search_form = SearchForm()
        club = Club.objects.get(id=club_id)
        ads = club.advertisement.all()
        paginator = Paginator(ads, 3)
        page = request.GET.get('page')
        try:
            current_page = paginator.page(page)
            ads = current_page.object_list
        except PageNotAnInteger:
            current_page = paginator.page(1)
            ads = current_page.object_list
        except EmptyPage:
            current_page = paginator.page(paginator.num_pages)
            ads = current_page.object_list
        return render(request,"club/list_ads.html",{"ads":ads,"page":current_page,"search_form":search_form,"club_id":club_id})
    else:
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            keyword = request.POST['keyword']
            try:
                ads = Advertisement.objects.filter(title__icontains=keyword)
                paginator = Paginator(ads, 3)
                page = request.GET.get('page')
                try:
                    current_page = paginator.page(page)
                    ads = current_page.object_list
                except PageNotAnInteger:
                    current_page = paginator.page(1)
                    ads = current_page.object_list
                except EmptyPage:
                    current_page = paginator.page(paginator.num_pages)
                    ads = current_page.object_list
                return render(request,"club/list_ads.html",{"ads":ads,"page":current_page,"search_form":search_form,"club_id":club_id})
            except:
                ads = Advertisement.objects.none()
                paginator = Paginator(ads, 3)
                page = request.GET.get('page')
                try:
                    current_page = paginator.page(page)
                    ads = current_page.object_list
                except PageNotAnInteger:
                    current_page = paginator.page(1)
                    ads = current_page.object_list
                except EmptyPage:
                    current_page = paginator.page(paginator.num_pages)
                    ads = current_page.object_list
                return render(request, "club/list_ads.html", {"ads": ads, "page": current_page, "search_form": search_form})
        else:
            return HttpResponse("errorForm!")

@login_required(login_url='/account/login/')
def ad_detail_owner(request,ad_id):
    ad = Advertisement.objects.get(id=ad_id)
    club_name = ad.owner.name
    return render(request,"club/ad_detail_owner.html",{"ad":ad,"club_name":club_name})

def ad_detail_other(request,ad_id):
    ad = Advertisement.objects.get(id=ad_id)
    return render(request,"club/ad_detail_other.html",{"ad":ad})

def ad_detail_edit(request,ad_id):
    ad = Advertisement.objects.get(id=ad_id)
    if request.method == "GET":
        ad_form = AdvertisementForm(initial={"title":ad.title,"content":ad.content,"video":ad.video,
                                             "attach":ad.attach,"show":ad.show})
        return render(request,"club/ad_detail_edit.html",{"ad_form":ad_form})
    else:
        ad_form = AdvertisementForm(request.POST,request.FILES)
        if ad_form.is_valid():
            ad_cd = ad_form.cleaned_data
            ad.title = ad_cd['title']
            ad.content = ad_cd['content']
            ad.video =ad_cd['video']
            ad.attach = ad_cd['attach']
            ad.show = ad_cd['show']
            ad.save()
            return redirect("club:ad_detail_owner",ad_id)
        else:
            return HttpResponse("errorForm!")
















