from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from taggit.managers import TaggableManager

# class UserProfileManager(models.Manager):
#     def get_queryset(self):
#         return super(UserProfileManager, self).get_queryset().filter(city='London')

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    description = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    website = models.URLField(default='')
    phone = models.IntegerField(default=0)
    image = models.ImageField(upload_to='profile_image', blank=True)
    # london = UserProfileManager()

    def __str__(self):
        return self.user.username

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)


class Category(models.Model):
    name = models.CharField(max_length=100, default='', unique=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Member(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="uploads/dp", null=True)
    modified = models.DateTimeField(auto_now=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = TaggableManager()
    phone = models.CharField(max_length=40, default='')

    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


class Tag(models.Model):
    name = models.TextField(max_length=255)

    def __str__(self):
        return self.name


class Photo(models.Model):
    owner = models.ForeignKey(User, null=True)
    caption = models.TextField(max_length=255)
    image = models.ImageField(upload_to="uploads/photos", null=True)
    tags = models.ManyToManyField(Tag)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.caption

    def image_tag(self):
        return u'<img src="%s" />' % self.image.url

    image_tag.short_description = 'Image Preview'
    image_tag.allow_tags = True


class Like(models.Model):
    owner = models.ForeignKey(Member, null=True)
    photo = models.ForeignKey(Photo, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def image_tag(self):
        return u'<img src="%s" />' % self.photo.image.url

    image_tag.short_description = 'Image with tags'
    image_tag.allow_tags = True


class Comment(models.Model):
    owner = models.ForeignKey(Member, null=True)
    photo = models.ForeignKey(Photo, null=True)
    text = models.TextField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text




