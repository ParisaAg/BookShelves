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

    def post(self, request, *args, **kwargs):
       
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True): 
            serializer.save()
            instance = serializer.instance
            return Response(self.get_serializer(instance).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        # 1. گرفتن همه آبجکت ها از دیتابیس
        queryset = self.get_queryset()
        
        # 2. سریالایز کردن لیست آبجکت ها (مهم: many=True)
        serializer = self.get_serializer(queryset, many=True)
        
        # 3. برگرداندن پاسخ
        return Response(serializer.data)