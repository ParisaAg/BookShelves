from rest_framework import serializers
from .models import SliderImage
from django.conf import settings

class SliderImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = SliderImage
        fields = ['id', 'title', 'image_url', 'created_at']

    def get_image_url(self, obj):
        return obj.image.url

