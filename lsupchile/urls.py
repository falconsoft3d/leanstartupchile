from django.conf.urls import url, include
from django.contrib import admin
from lsupchile import views
from django.conf import settings
from django.conf.urls.static import static
from accounts import views as acviews

urlpatterns = [
    url(r'^$', acviews.home, name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^account/', include('accounts.urls', namespace='accounts')),
    url(r'^blogging/', include('blogging.urls', namespace='blogging')),
    url(r'^oauth/', include('social_django.urls', namespace='social')),  # <--
    url(r'^contact/', include('contactus.urls', namespace='contact'),),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
