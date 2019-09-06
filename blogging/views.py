# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect

from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView, \
                                 UpdateView, RedirectView
from models import Blog
from accounts.models import Category
from forms import BlogForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from accounts.models import Member

# Create your views here.
class BlogListView(ListView):

    template_name = 'blogging/blogs.html'
    model = Blog
    context_object_name = 'blogs'  # Default: object_list
    paginate_by = 9
    queryset = Blog.objects.filter(active=True)

    def get_context_data(self, **kwargs):
        context = super(BlogListView, self).get_context_data(**kwargs)
        context['categorys'] = Category.objects.annotate(num_blogs=Count('blog')).order_by('id')
        context['current_user'] = self.request.user
        current_user = self.request.user
        is_member = False
        if current_user.id is not None:
            if Member.objects.filter(user__id=current_user.id) is not None:

                owner = Member.objects.filter(user__id=current_user.id).first()
                if owner is not None:
                    is_member = True
        context['is_member'] = is_member
        context['blog_total'] = Blog.objects.all().count()
        return context

class BlogCategoryListView(ListView):

    template_name = 'blogging/blogs_category.html'
    model = Blog
    context_object_name = 'blogs'  # Default: object_list
    paginate_by = 9


    def get_context_data(self, **kwargs):
        context = super(BlogCategoryListView, self).get_context_data(**kwargs)
        context['categorys'] = Category.objects.annotate(num_blogs=Count('blog')).order_by('id')
        context['current_user'] = self.request.user
        current_user = self.request.user
        is_member = False
        if current_user.id is not None:
            if Member.objects.filter(user__id=current_user.id) is not None:

                owner = Member.objects.filter(user__id=current_user.id).first()
                if owner is not None:
                    is_member = True
        context['is_member'] = is_member
        context['now_category'] = Category.objects.filter(name=self.kwargs['category']).first()
        context['blog_total'] = Blog.objects.all().count()
        return context

    def get_queryset(self):
        qs = super(BlogCategoryListView, self).get_queryset()
        category = Category.objects.filter(name=self.kwargs['category']).first()
        return qs.filter(category__pk=category.id).filter(active=True)


class BlogDetailView(DetailView):

    template_name = "blogging/blog_detail.html"
    model = Blog

    def get_context_data(self, **kwargs):
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        context['current_user'] = self.request.user
        return context


class BlogCreateView(CreateView):

    template_name = "blogging/blog_create.html"
    form_class = BlogForm

    def form_valid(self, form):
        """
        Assign the author to the request.user
        """
        form.instance.author = Member.objects.filter(user__pk = self.request.user.id).first()
        return super(BlogCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(BlogCreateView, self).get_context_data(**kwargs)
        context['current_user'] = self.request.user

        return context


class BlogRedirectView(RedirectView):
    url = reverse_lazy('blogging:blogging')


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blogging:blogging')


class BlogUpdateView(UpdateView):
    template_name = "blogging/blog_update.html"
    model = Blog
    form_class = BlogForm

    def get_context_data(self, **kwargs):
        context = super(BlogUpdateView, self).get_context_data(**kwargs)
        context['current_user'] = self.request.user

        return context



