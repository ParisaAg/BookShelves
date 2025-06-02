from django.urls import path
from .views import SliderImageListCreateView

urlpatterns = [
    path('', SliderImageListCreateView.as_view(), name='slider-images'),
]



