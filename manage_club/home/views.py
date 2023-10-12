from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST
# Create your views here.
@login_required(login_url='/account/login/')
@require_GET
def homepage(request):
    return render(request,"home/homepage.html")