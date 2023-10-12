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
def create_good(request,club_id):
    return
