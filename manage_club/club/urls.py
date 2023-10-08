from django.urls import re_path as url
from . import views
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import path

app_name = "club"

urlpatterns = [
    url(r'^create-club/$',views.create_club,name="create_club"),
    url(r'^list-club/$',views.list_club,name="list_club"),
    url(r'^club-detail/(?P<club_id>\d+)/$',views.list_club_detail,name="club_detail"),
    url(r'^send-message/$',views.send_message,name="send_message"),
    url(r'^my-send/$',views.my_send,name="my_send"),
    url(r'^my-send/(?P<type>\d+)/$', views.my_send_type, name="my_send_type"),
    url(r'^my-receive/$',views.my_recceived,name="my_receive"),
    url(r'^message-detail/(?P<message_id>\d+)/$',views.message_detail,name="message_detail"),
    url(r'^join-club/(?P<club_id>\d+)/$',views.join_club,name="join_club"),
    url(r'^confirm-join/(?P<club_id>\d+)/$',views.confirm_join,name="confirm_join"),
    url(r'^my_club/$',views.my_club,name="my_club"),
]