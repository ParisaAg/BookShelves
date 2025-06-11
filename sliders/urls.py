from django.urls import path
from .views import SliderImageUploadView,SliderImageDetailView

urlpatterns = [
    path('', SliderImageUploadView.as_view(), name='slider-list-create'),
    path('<int:pk>/', SliderImageDetailView.as_view(), name='slider-detail'),
]



