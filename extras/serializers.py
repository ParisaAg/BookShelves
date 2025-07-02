

from rest_framework import serializers
from .models import Banner, Announcement

class BannerSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Banner
        fields = [
            'id', 'title', 'subtitle',
            'image_url',  
            'button_text', 'button_link',
            'gradient_from', 'gradient_to'
        ]

    
    def get_image_url(self, obj):

        if obj.image_url and hasattr(obj.image_url, 'url'):
            return obj.image_url.url
        return None

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['id', 'message']