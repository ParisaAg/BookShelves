
from rest_framework import serializers
from .models import Banner,Announcement

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = [
            'id', 'title', 'subtitle', 'image', 
            'button_text', 'button_link', 
            'gradient_from', 'gradient_to'
        ]


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['id', 'message']
