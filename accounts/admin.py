from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile,UserActivity 
from django.shortcuts import render
from django.urls import path
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta


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
    five_minutes_ago = timezone.now() - timedelta(minutes=5)
    online_activities = UserActivity.objects.filter(last_seen__gte=five_minutes_ago)
    online_users = [activity.user for activity in online_activities]

    context = {
        'title': 'Online Users',
        'online_users': online_users,
        'online_count': len(online_users),
        # Required for the admin template
        'has_permission': request.user.is_staff,
        'site_header': admin.site.site_header,
        'site_title': admin.site.site_title,
        'app_list': admin.site.get_app_list(request)
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

