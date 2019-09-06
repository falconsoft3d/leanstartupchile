import json, itertools
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.views import logout as original_logout
from django.contrib.auth.views import login as original_login
from django.contrib.sessions.backends.base import SessionBase
from django.contrib.auth import authenticate, login as auth_login
from accounts.forms import (

    RegistrationForm,
    EditProfileForm,
    MemberPhotoForm,
    PhotoForm,
)

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm, AuthenticationForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

from accounts.models import Member, Photo, Category, Like, Comment
from annoying.functions import get_object_or_None

def alt_logout(request, *args, **kwargs):
    """
    Info on why this exists: http://code.djangoproject.com/ticket/6941
    Clears out any session data on logout that would otherwise persist
    for any subsequent logins regardless of user_id.
    """
    for sesskey in request.session.keys():
        del request.session[sesskey]
    return original_logout(request, *args, **kwargs)

def alt_login(request, *args, **kwargs):
    """
    Info on why this exists: http://code.djangoproject.com/ticket/6941
    Clears out any session data on login that would otherwise persist
    for any subsequent logins regardless of user_id.
    Session data is only cleared if the test cookie is not present.
    If its present, the session data is already cleared and this does nothing.
    """
    if SessionBase.TEST_COOKIE_NAME not in request.session:
        for sesskey in request.session.keys():
            del request.session[sesskey]
    return original_login(request, *args, **kwargs)


def register(request):
    if request.method =='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            messages.info(request, "Thanks for registering. You are now logged in.")
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            auth_login(request, new_user)
            return redirect(reverse('accounts:home'))
    else:
        form = RegistrationForm()

    args = {'register_form': form,'form': AuthenticationForm()}
    return render(request, 'accounts/landing.html', args)

def view_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            print('valid')
            form.save()
            return redirect(reverse('accounts:view_profile'))
        print('not valid')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'current_user': user, 'form': form}
        return render(request, 'accounts/logged/account_edit_profile.html', args)

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect(reverse('accounts:view_profile'))
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'accounts/edit_profile.html', args)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('accounts:view_profile'))
        else:

            return redirect(reverse('accounts:change_password'))
    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form, 'current_user':request.user}
        return render(request, 'accounts/logged/account_change_password.html', args)


def home(request):
    categorys = Category.objects.all()[:10]
    userlist = []
    users = User.objects.all()
    likenums = {}
    for user in users:
        num=0;
        for photo in Photo.objects.filter(owner__id=user.id):
            num = num + Like.objects.filter(photo__pk=photo.id).count()
        print num
        member = Member.objects.filter(user__id=user.id).first()
        likenums[user.id] = num
    print likenums


    return render(request, 'accounts/logged/home.html', {'current_user':request.user,'likenums':likenums, 'categorys': categorys})

    # args = {'current_user':request.user, 'categorys':categorys}
    # return render(request, 'accounts/logged/home.html', args)


#landing page with login and signup function


def landing(request):
    context = {
        'form': AuthenticationForm(),
        'register_form': RegistrationForm()
    }
    return render(request, 'accounts/landing.html', context)

# member settings.


def view_member_profile(request, username=None):

    if username is None:
        user = request.user

    else:
        user = User.objects.get(username=username)

    if Member.objects.filter(user__pk=user.id).first() is not None:
        member_profile_form = MemberPhotoForm(initial = {'category_field': user.member.category.pk }, instance=user.member)
    else:
        member_profile_form = MemberPhotoForm()

    dp_obj = get_object_or_None(Member, user__pk=user.id)
    if dp_obj is None:
        user_dp = False
    else:
        user_dp = dp_obj

    user_photos = Photo.objects.filter(owner__pk=user.id)
    photos_count = user_photos.count()

    return render(request, 'accounts/logged/account_member_profile.html', {
        'current_user': user,
        'user': user,
        'user_dp': user_dp,
        'photos': user_photos,
        'count': photos_count,
        'dp_form': member_profile_form
    })

#upload photo


def upload_photo(request):
    """
    Method that lets user upload an image
    """
    uploader = request.user
    form = PhotoForm()

    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = uploader
            obj.save()

            return redirect(reverse('accounts:myfeed'))
    else:
        form = PhotoForm()

    return render(request, 'accounts/logged/upload_photo.html', {'form': form, 'current_user':request.user})


def feed(request, pk=None):
    """
    View that displays the uploaded photos of users that the
    `logged user` follows
    """
    user = User.objects.get(pk=pk)
    current_user = request.user
    member = Member.objects.filter(user__pk=user.id).first()

    if user.id == request.user.id and member.active:
        return redirect(reverse('accounts:myfeed'))
    photos = []
    liked_photos = []
    is_member = False
    following_photos = Photo.objects.filter(owner__id=user.id)

    if following_photos is not None:
        photos.append(following_photos)

    # flatten list of photos
    chain = itertools.chain(*photos)
    photos = list(chain)
    if current_user.id is not None:
        if Member.objects.filter(user__id=current_user.id) is not None:

            owner = Member.objects.filter(user__id=current_user.id).first()
            if owner is not None and owner.active:
                is_member = True
            for photo in photos:
                photo_like = get_object_or_None(Like,
                                                owner=owner,
                                                photo=photo
                                                )
                if photo_like:
                    liked_photos.append(photo.pk)


    print("Liked photos", liked_photos)
    return render(request, 'accounts/logged/feed.html', {
        'photos': photos,
        'liked_photos': liked_photos,
        'owner':user,
        'current_user':request.user,
        'is_member':is_member,
        })

def myfeed(request):
    user = request.user
    photos = []
    liked_photos = []
    # user_following = Follow.objects.filter(follower__id=user.id)
    users = User.objects.all()[:10]
    following_photos = Photo.objects.filter(owner__id=user.id)

    if following_photos is not None:
        photos.append(following_photos)

    # flatten list of photos
    chain = itertools.chain(*photos)
    photos = list(chain)
    for photo in photos:
        photo_like = get_object_or_None(Like,
                                        owner=user.member,
                                        photo=photo
                                        )
        if photo_like:
            liked_photos.append(photo.pk)

    return render(request, 'accounts/logged/myfeed.html', {
        'photos': photos,
        'liked_photos': liked_photos,
        'user': user,
        'current_user':request.user,
    })


def edit_feed(request, pk=None):

    photo = Photo.objects.filter(pk=pk).first()

    print("photo", photo)

    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            form.save()

            return redirect(reverse('accounts:myfeed'))
    else:

        form = PhotoForm(initial={'caption': photo.caption, 'image': photo.image})

    return render(request, 'accounts/logged/edit_feed.html', {
        'form': form,
        'image': photo.image,
        'current_user': request.user,
        })

def delete_feed(request, pk=None):

    photo = Photo.objects.filter(pk=pk).first()

    photo.delete()

    return redirect(reverse('accounts:myfeed'))


# for blogging system
#
# def view_blog(request):
#
#     return render(request, 'accounts/blogging/blogging.html', {'current_user':request.user})


# for contact us system


def view_contact_us(request):

    return render(request, 'accounts/contactus/view_contact_us.html', {'current_user': request.user})


def delete_comment(request, pk=None):

    comment = Comment.objects.filter(pk=pk).first()

    comment.delete()
    return redirect(reverse('accounts:myfeed'))