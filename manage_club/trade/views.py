import json

from django.shortcuts import render
from .models import GoodType,Commodity
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from club.models import Club
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import QuerySet
from .forms import CommodityForm
from .models import Commodity,GoodType

@login_required(login_url='account/login')
@csrf_exempt
def create_good(request,club_id):
    if request.method == "GET":
        good_form = CommodityForm()
        types = GoodType.objects.all()
        return render(request,"trade/create_good.html",{"good_form":good_form,"types":types,"club_id":club_id})
    else:
        club = Club.objects.get(id=club_id)
        types = request.POST["types"]
        name = request.POST['name']
        expense = request.POST['expense']
        intro = request.POST['intro']
        contact = request.POST['contact']
        photo = request.FILES.get('photo')
        print(photo)
        new_good = Commodity()
        new_good.status = "selling"
        new_good.owner = club
        new_good.photo = photo
        new_good.name = name
        new_good.expense = expense
        new_good.intro = intro
        new_good.contact = contact
        new_good.save()
        if types:
            for type in json.loads(types):
                type = GoodType.objects.get(type=type)
                new_good.Type.add(type)
        return HttpResponse("1")


@login_required(login_url='account/login')
def list_goods(request,club_id):
    club = Club.objects.get(id=club_id)
    goods = club.owner.all()
    paginator = Paginator(goods, 3)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        goods = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        goods = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        goods = current_page.object_list
    return render(request,"trade/list_goods.html",{"club_id":club_id,"goods":goods,"page":current_page})



