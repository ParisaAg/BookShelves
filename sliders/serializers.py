from rest_framework import serializers
from .models import SliderImage
from cloudinary.utils import cloudinary_url

class SliderImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = SliderImage
        fields = ['id', 'title', 'image_url', 'created_at']

    def get_image_url(self, obj):
        url, _ = cloudinary_url(str(obj.image))  # 👈 همین خط اصلاح شد
        return url
