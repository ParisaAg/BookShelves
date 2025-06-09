
# class SliderImageListCreateView(generics.ListCreateAPIView):
#     queryset = SliderImage.objects.all().order_by('-created_at')
#     serializer_class = SliderImageSerializer
#     parser_classes = [MultiPartParser, FormParser]

# def post(self, request, *args, **kwargs):
#     print("FILES:", request.FILES)
#     print("DATA:", request.data)
#     serializer = self.get_serializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     print("ERRORS:", serializer.errors)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import MultiPartParser, FormParser

from django.utils.decorators import method_decorator
from django.conf import settings
import boto3
import uuid

from .models import SliderImage
from .serializers import SliderImageSerializer


@method_decorator(csrf_exempt, name='dispatch')
class SliderImageUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)