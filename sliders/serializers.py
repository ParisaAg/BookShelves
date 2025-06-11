# serializers.py

from rest_framework import serializers
from .models import SliderImage

class SliderImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SliderImage
        # 'image' را به فیلدها اضافه میکنیم تا در ورودی دریافت شود
        fields = ['id', 'title', 'image', 'image_url', 'created_at']
        extra_kwargs = {
            # 'image' را فقط برای نوشتن (آپلود) در نظر میگیریم
            # و در خروجی جیسان نمایش داده نمیشود
            'image': {'write_only': True}
        }
        # فیلد 'image_url' چون با متد ساخته میشود، همیشه فقط خواندنی است
        read_only_fields = ['id', 'created_at', 'image_url']

    def get_image_url(self, obj):
        # این متد حالا به درستی کار خواهد کرد چون obj.image مقدار دارد
        if obj.image and hasattr(obj.image, 'url'):
            return obj.image.url
        return None