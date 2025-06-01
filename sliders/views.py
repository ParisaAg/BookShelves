from rest_framework import generics
from .models import SliderImage
from .serializers import SliderImageSerializer

class SliderImageListCreateView(generics.ListCreateAPIView):
    queryset = SliderImage.objects.all().order_by('-created_at')
    serializer_class = SliderImageSerializer
    pagination_class = None 