from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import SliderImage
from .serializers import SliderImageSerializer

class SliderImageListCreateView(generics.ListCreateAPIView):
    queryset = SliderImage.objects.all().order_by('-created_at')
    serializer_class = SliderImageSerializer
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)