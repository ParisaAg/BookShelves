from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from .models import Banner, Announcement
from .serializers import BannerSerializer, AnnouncementSerializer

class BannerListView(ListCreateAPIView):
    queryset = Banner.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = BannerSerializer

class AnnouncementListView(ListCreateAPIView):
    queryset = Announcement.objects.all().order_by('-created_at')
    serializer_class = AnnouncementSerializer
