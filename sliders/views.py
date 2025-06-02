from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import SliderImage
from .serializers import SliderImageSerializer
from django.conf import settings
from django.http import JsonResponse
import boto3 
from django.views.decorators.csrf import csrf_exempt

def get_s3_client():
    return boto3.client(
        's3',
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )



@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        s3_client = get_s3_client()
        file = request.FILES['file']
        try:
            s3_client.upload_fileobj(file, settings.AWS_STORAGE_BUCKET_NAME, file.name)
            return JsonResponse({'message': f'{file.name} uploaded successfully.'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)




class SliderImageListCreateView(generics.ListCreateAPIView):
    queryset = SliderImage.objects.all().order_by('-created_at')
    serializer_class = SliderImageSerializer
    pagination_class = None 