# views.py

from rest_framework.generics import GenericAPIView
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

from .models import SliderImage
from .serializers import SliderImageSerializer

class SliderImageUploadView(GenericAPIView):
    queryset = SliderImage.objects.all()
    serializer_class = SliderImageSerializer
    parser_classes = [MultiPartParser, FormParser]
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

    def post(self, request, *args, **kwargs):
       
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True): 
            serializer.save()
            instance = serializer.instance
            return Response(self.get_serializer(instance).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class SliderImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SliderImage.objects.all()
    serializer_class = SliderImageSerializer