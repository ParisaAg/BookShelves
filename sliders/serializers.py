from rest_framework import serializers
from .models import SliderImage



class SliderImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = SliderImage
        fields = ['id', 'title', 'image', 'created_at']

    def get_image(self, obj):
        if obj.image:
            return obj.image.url  # This returns the full URL
        return None
