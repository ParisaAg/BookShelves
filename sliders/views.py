from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import SliderImage
from .serializers import SliderImageSerializer
from object_storage.views import get_s3_client
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


@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('image'):
        s3_client = get_s3_client()
        file = request.FILES['image']
        try:
            s3_client.upload_fileobj(file,settings.AWS_STORAGE_BUCKET_NAME, file.name)
            return JsonResponse({'message': f'{file.name} uploaded successfully.'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)
