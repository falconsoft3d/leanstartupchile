from django.contrib import admin
from accounts.models import UserProfile, Member, Category, Photo, Tag, Like, Comment
from accounts.forms import CategoryAdminForm

admin.site.register(UserProfile)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_info', 'city', 'phone', 'website')

    def user_info(self, obj):
        return obj.description

    def get_queryset(self, request):
        queryset = super(UserProfileAdmin, self).get_queryset(request)
        queryset = queryset.order_by('-phone', 'user')
        return queryset

    user_info.short_description = 'Info'

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ('name', 'created')
    form = CategoryAdminForm


admin.site.register(Category, CategoryAdmin)

admin.site.register(Member)
admin.site.register(Photo)
admin.site.register(Tag)
admin.site.register(Like)
admin.site.register(Comment)
