# TODO[10.6.2016]: Refactor code, remove unused imports
# Views for AJAX Requests

import json, itertools

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from accounts.forms import LoginForm, PhotoForm, MemberPhotoForm
from accounts.models import Photo, Member, Comment, Like

from annoying.functions import get_object_or_None
from django.urls import reverse
# Create your views here.


def upload_member_profile(request):
    """
    Method (AJAX) that allows the `logged user` to upload a profile pic
    """
    uploader = request.user

    form = MemberPhotoForm()
    data = {
        'status': 1,
    }

    if request.method == 'POST':
        existing_dp = get_object_or_None(Member, user__pk=uploader.id)
        if existing_dp is not None:
            form = MemberPhotoForm(request.POST, request.FILES, instance=uploader.member)
        else:
            form = MemberPhotoForm(request.POST, request.FILES)
        if form.is_valid():

            print("CategoryID", form.cleaned_data['category_field'])
            # check if user has already uploaded a profile picture
            existing_dp = get_object_or_None(Member, user__pk=uploader.id)

            obj = form.save(commit=False)
            obj.user = uploader
            obj.category = form.cleaned_data['category_field']
            if existing_dp is not None:
                obj.id = existing_dp.id
            obj.save()
            form.save_m2m()

            data['status'] = 1

    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')

def post_photo_comment(request):
    data = {
        'status': 0
    }

    if request.user.is_authenticated() and request.method == 'POST':
        post_data = request.POST

        photo = get_object_or_None(Photo, pk=post_data['photo_id'])
        comment = Comment(
            owner=request.user.member,
            photo=photo,
            text=post_data['comment_text']
            )
        resp = comment.save()
        data['status'] = 1

    data = json.dumps(data)
    return HttpResponseRedirect(reverse('accounts:feed_with_pk', kwargs={'pk': photo.owner.pk}))

def like_photo(request):
    data = {
        'status': 0
    }

    # TODO: Check if like already exists
    if request.user.is_authenticated() and request.method == 'POST':
        post_data = request.POST

        photo = get_object_or_None(Photo, pk=post_data['photo_id'])

        check_like = get_object_or_None(Like,
            owner=request.user.member,
            photo=photo
            )

        if check_like is None:
            like = Like(
                owner=request.user.member,
                photo=photo,
                )
            like.save()
            data['status'] = 1

    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')
