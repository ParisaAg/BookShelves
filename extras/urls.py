
from django.urls import path,include
from .views import BannerListView,AnnouncementListView,BannerDetailView,AnnouncementDetailView

urlpatterns = [
path('banners/', BannerListView.as_view(), name='banner-list'),
path('announcements/', AnnouncementListView.as_view(), name='announcement-list'),
 path('banners/<int:pk>/', BannerDetailView.as_view(), name='banner-detail'),
path('announcements/<int:pk>/', AnnouncementDetailView.as_view(), name='announcement-detail'),
]