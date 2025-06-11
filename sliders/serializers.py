from rest_framework import serializers
from .models import SliderImage
from django.conf import settings
from cloudinary.utils import cloudinary_url

class SliderImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = SliderImage
        fields = ['id', 'title', 'image_url', 'created_at']

    def get_image_url(self, obj):
        if obj.image:
            try:
            # اگر شیء CloudinaryResource باشه
                return obj.image.url
            except AttributeError:
            # اگر فقط رشته باشه
                return f"https://res.cloudinary.com/{settings.CLOUDINARY_STORAGE['CLOUD_NAME']}/image/upload/{obj.image}"
        return None
