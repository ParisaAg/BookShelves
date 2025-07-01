
from django.urls import path,include
from .views import BannerListView,AnnouncementListView


path('api/banners/', BannerListView.as_view()),
path('api/announcements/', AnnouncementListView.as_view()),
