from __future__ import unicode_literals
from django.conf.urls import url
from django.views.generic import TemplateView

from .views import ContactUsView
import views

urlpatterns = [
    url(r'^$', ContactUsView.as_view(),  {}, name='contactus'),
    url(r'^success/$', views.contact_success,
        {}, name='contactus-success'),
]
