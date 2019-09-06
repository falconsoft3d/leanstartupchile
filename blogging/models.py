# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from accounts.models import Member,Category
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


# Create your models here.

class Blog(models.Model):
    author = models.ForeignKey(Member, null=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    image = models.ImageField(upload_to="uploads/blogs", null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blogging:blog-detail', kwargs={'pk':self.id})
