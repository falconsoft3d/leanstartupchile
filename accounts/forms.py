from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
import re

from accounts.models import Member, Category, Photo


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class EditProfileForm(forms.ModelForm):
    template_name='/something/else'

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',

        )


class MemberPhotoForm(forms.ModelForm):
    category_field = forms.ModelChoiceField(queryset=Category.objects.distinct())

    class Meta:
        model = Member
        fields = ('image','phone', 'category_field','tags')


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
        ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs = {
            'class': 'form-control'
        }
        ))


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('image', 'caption')
        widgets = {
            'caption': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
                })
        }


class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)

    def clean_name(self):
        name = self.cleaned_data['name']
        if ' ' in name:
            raise forms.ValidationError("Spaces not allowed")

        return name

