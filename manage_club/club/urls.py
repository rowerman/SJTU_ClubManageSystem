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
    url(r'^my-send-type/(?P<type>\d+)/$', views.my_send_type, name="my_send_type"),
    url(r'^my-receive/$',views.my_recceived,name="my_receive"),
    url(r'^message-detail/(?P<message_id>\d+)/$',views.message_detail,name="message_detail"),
    url(r'^join-club/(?P<club_id>\d+)/$',views.join_club,name="join_club"),
    url(r'^exit-club/$',views.exit_club,name="exit_club"),
    url(r'^confirm-join/(?P<club_id>\d+)/$',views.confirm_join,name="confirm_join"),
    url(r'^my_club/$',views.my_club,name="my_club"),
    url(r'^manage-Myclub/$',views.manage_Myclub,name="manage_Myclub"),
    url(r'^manage-member/(?P<club_id>\d+)/$',views.manage_member,name="manage_member"),
    url(r'^delete-member/(?P<club_id>\d+)/$',views.delete_member,name="delete_member"),
    url(r'^manage-clubInfo/(?P<club_id>\d+)/$',views.manage_clubInfo,name="manage_clubInfo"),
    url(r'^club-image/(?P<club_id>\d+)/$',views.club_image,name="club_image"),
    url(r'^create-activity/(?P<club_id>\d+)/$',views.create_activity,name="create_activity"),
    url(r'^list-activity/(?P<club_id>\d+)/$',views.list_activity,name="list_activity"),
    url(r'^activity-detail/(?P<activity_id>\d+)/(?P<club_id>\d+)/$',views.activity_detail,name="activity_detail"),
    url(r'^activity-detail/(?P<activity_id>\d+)/$',views.activity_detail_version,name="activity_detail"),
    url(r'^delete-activity/$',views.delete_activity,name="delete_activity"),
    url(r'^all-activity/$',views.all_activity,name="all_activity"),
    url(r'^fan-Club/$',views.fan_Club,name="fan_Club"),

    url(r'^create-ad/(?P<club_id>\d+)/$',views.create_ad,name="create_ad"),
    url(r'^list-ads/(?P<club_id>\d+)/$',views.list_ads,name="list_ads"),
    url(r'^ad-detail-owner/(?P<ad_id>\d+)/$',views.ad_detail_owner,name="ad_detail_owner"),
    url(r'^ad-detail-other/(?P<ad_id>\d+)/$',views.ad_detail_other,name="ad_detail_other"),
    url(r'^ad-detail-edit/(?P<ad_id>\d+)/$',views.ad_detail_edit,name="ad_detail_edit"),
]