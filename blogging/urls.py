from django.conf.urls import url
from blogging.views import BlogListView, BlogCategoryListView, BlogDetailView, BlogCreateView, BlogDeleteView, BlogUpdateView
from . import views

urlpatterns = [
    url(r'^$', BlogListView.as_view(), name='blogging'),
    url(r'^category/(?P<category>[-\w]+)/$', BlogCategoryListView.as_view(), name="blog-category"),
    url(r'^(?P<pk>\d+)/$', BlogDetailView.as_view(), name="blog-detail"),
    url(r'^create/$', BlogCreateView.as_view(), name="blog-create"),
    url(r'^delete/(?P<pk>\d+)/$', BlogDeleteView.as_view(), name="blog-delete"),
    url(r'^update/(?P<pk>\d+)/$', BlogUpdateView.as_view(), name="blog-update"),

]
