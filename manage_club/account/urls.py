from django.urls import re_path as url
from . import views
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import path

app_name='account'

urlpatterns = [
    url(r'^login/$',views.user_login,name="user_login"),
    path(r'logout/', auth_views.LogoutView.as_view(template_name="account/logout.html"), name='logout'),
    url(r'^register/$',views.register,name="user_register"),
    path('password-change/',
         auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html',
                                               success_url='../password-change-done/'), name='password_change'),
    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
         name='password_change_done'),
    url(r'^password-reset/$',auth_views.PasswordResetView.as_view(template_name="account/password_reset_form.html",
                                                          email_template_name="account/password_reset_email.html",
                                                          subject_template_name="account/password_reset_subject.txt",
                                                          success_url="../password-reset-done"),name="password_reset"),
    url(r'^password-reset-done/$',auth_views.PasswordResetDoneView.as_view(template_name="account/password_reset_done.html"),name="password_Reset_done"),
    url(r'^password-reset-confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
        auth_views.PasswordResetConfirmView.as_view(template_name="account/password_reset_confirm.html",success_url="../../../password-reset-complete/"),
        name="password_reset_confirm"),
    url(r'^password-reset-complete/$',auth_views.PasswordResetCompleteView.as_view(template_name="account/password_reset_complete.html"),
        name="password_reset_complete"),
    url(r'^my-information/$',views.myself,name="my_information"),
    url(r'^my-information/(?P<user_id>\d+)/$',views.myself,name="my_information"),
    url(r'^edit-my-information/$',views.myself_edit,name="edit_my_information"),
    url(r'^my-image/$',views.my_image,name="my_image"),
    url(r'^search/$',views.search,name="search"),
]