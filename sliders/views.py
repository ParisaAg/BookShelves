from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import SliderImage
from .serializers import SliderImageSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
class SliderImageListCreateView(generics.ListCreateAPIView):
    queryset = SliderImage.objects.all().order_by('-created_at')
    serializer_class = SliderImageSerializer
    parser_classes = [MultiPartParser, FormParser]

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
        title = request.data.get('title')
        file = request.FILES.get('image')

        if not file:
            return Response({'error': 'No image provided'}, status=400)

        # ساخت نام یکتا
        filename = f"{uuid.uuid4().hex}_{file.name}"

        try:
            s3_client = boto3.client(
                's3',
                endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )

            s3_client.upload_fileobj(
                file,
                settings.AWS_STORAGE_BUCKET_NAME,
                filename,
                ExtraArgs={'ContentType': file.content_type}
            )

            file_url = f"{settings.AWS_S3_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/{filename}"

            slider = SliderImage.objects.create(title=title, image=file_url)
            serializer = SliderImageSerializer(slider)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=500)

