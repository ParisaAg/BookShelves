from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import Banner, Announcement
from .serializers import BannerSerializer, AnnouncementSerializer

class BannerListView(ListAPIView):
    queryset = Banner.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = BannerSerializer

class AnnouncementListView(ListAPIView):
    queryset = Announcement.objects.all().order_by('-created_at')
    serializer_class = AnnouncementSerializer
