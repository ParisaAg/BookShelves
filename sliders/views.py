# views.py

from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

from .models import SliderImage
from .serializers import SliderImageSerializer

class SliderImageUploadView(GenericAPIView):
    queryset = SliderImage.objects.all()
    serializer_class = SliderImageSerializer
    parser_classes = [MultiPartParser, FormParser]

    # این متد باید داخل کلاس باشد
    def post(self, request, *args, **kwargs):
        # مطمئن شوید که سریالایزر از نسخه اصلاح شده قبلی است
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True): # raise_exception=True برای دیباگ بهتر است
            serializer.save()
            instance = serializer.instance
            return Response(self.get_serializer(instance).data, status=status.HTTP_201_CREATED)
        # با وجود raise_exception=True این خط دیگر لازم نیست، اما بودنش ضرری ندارد
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)