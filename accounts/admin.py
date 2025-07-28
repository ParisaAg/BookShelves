from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile
from django.shortcuts import render
from django.urls import path
from django.core.cache import cache



class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'
    
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth_date')




def online_users_view(request):
    online_keys = cache.keys('online-user-*')
    online_user_ids = [int(key.split('-')[-1]) for key in online_keys]
    online_users = User.objects.filter(id__in=online_user_ids)

    context = {
        'title': 'کاربران آنلاین',
        'online_users': online_users,
        'online_count': len(online_user_ids),
    }
    return render(request, 'admin/online_users.html', context)

original_get_urls = admin.site.get_urls

def get_urls():
    urls = original_get_urls()
    custom_urls = [
        path('online-users/', admin.site.admin_view(online_users_view), name='online-users'),
    ]
    return custom_urls + urls

admin.site.get_urls = get_urls

