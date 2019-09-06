from django.conf.urls import url
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import (
    login, logout, password_reset, password_reset_done, password_reset_confirm,
    password_reset_complete
)

from accounts import ajax
from forms import RegistrationForm
from . import views

urlpatterns = [
    url(r'^home/$', views.home, name='home'),
    url(r'^login/$', login, {'template_name': 'accounts/landing.html','extra_context':{'register_form': RegistrationForm()}},name='login'),
    url(r'^logout/$', logout, {'template_name': 'accounts/user_logged_out.html','extra_context':{'form':AuthenticationForm()}}, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^profile/$', views.view_profile, name='view_profile'),
    url(r'^profile/(?P<pk>\d+)/$', views.view_profile, name='view_profile_with_pk'),
    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    url(r'^change-password/$', views.change_password, name='change_password'),

    url(r'^reset-password/$', password_reset, {'template_name': 'accounts/reset_password.html', 'post_reset_redirect': 'accounts:password_reset_done', 'email_template_name': 'accounts/reset_password_email.html'}, name='reset_password'),

    url(r'^reset-password/done/$', password_reset_done, {'template_name': 'accounts/reset_password_done.html'}, name='password_reset_done'),

    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, {'template_name': 'accounts/reset_password_confirm.html', 'post_reset_redirect': 'accounts:password_reset_complete'}, name='password_reset_confirm'),

    url(r'^reset-password/complete/$', password_reset_complete,{'template_name': 'accounts/reset_password_complete.html'}, name='password_reset_complete'),



    url(r'^landing/$', views.landing, name='landing'),

    url(r'^member-profile/$', views.view_member_profile, name='view_member_profile'),
    url(r'^upload_dp/$', ajax.upload_member_profile, name='upload_member_profile'),
    url(r'^upload/$', views.upload_photo, name='upload_photo'),
    url(r'^feed/$', views.myfeed, name='myfeed'),
    url(r'^feed/(?P<pk>\d+)/$', views.feed, name='feed_with_pk'),
    url(r'^like_photo/$', ajax.like_photo, name='like_photo'),
    url(r'^post_comment/$', ajax.post_photo_comment, name='post_photo_comment'),
    url(r'^edit_feed/(?P<pk>\d+)/$', views.edit_feed, name='edit_with_pk'),
    url(r'^delete_feed/(?P<pk>\d+)/$', views.delete_feed, name='delete_with_pk'),

    url(r'^delete_comment/(?P<pk>\d+)/$', views.delete_comment, name='delete_comment_with_pk'),


]
