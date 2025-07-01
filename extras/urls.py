
from django.urls import path,include
from .views import BannerListView,AnnouncementListView


path('banners/', BannerListView.as_view()),
path('announcements/', AnnouncementListView.as_view()),
