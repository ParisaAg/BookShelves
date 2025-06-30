# serializers.py

from rest_framework import serializers
from .models import SliderImage

class SliderImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SliderImage

        fields = ['id', 'title', 'image', 'image_url', 'created_at']
        extra_kwargs = {

            'image': {'write_only': True}
        }
        read_only_fields = ['id', 'created_at', 'image_url']

    def get_image_url(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return obj.image.url
        return None