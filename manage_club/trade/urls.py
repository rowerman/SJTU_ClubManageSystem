from django.urls import re_path as url
from . import views

app_name = "trade"

urlpatterns = [
    url(r'^create-good/(?P<club_id>\d+)/$',views.create_good,name="create_good"),
    url(r'^list-goods/(?P<club_id>\d+)/$',views.list_goods,name="list_goods"),
]