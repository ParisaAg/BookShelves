
from django.urls import path,include
from .views import BannerListView,AnnouncementListView

urlpatterns = [
path('banners/', BannerListView.as_view()),
path('announcements/', AnnouncementListView.as_view()),
]