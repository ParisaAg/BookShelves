

from rest_framework import serializers
from .models import Banner, Announcement

class BannerSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True, required=False)

    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Banner
        fields = [
            'id', 'title', 'subtitle',
            'image',  
            'image_url',  
            'button_text', 'button_link',
            'gradient_from', 'gradient_to'
        ]

    

    def get_image_url(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return obj.image.url
        return None

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['id', 'message']