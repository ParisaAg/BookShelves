from django.urls import path
from .views import SliderImageUploadView

urlpatterns = [
    path('', SliderImageUploadView.as_view(), name='slider-list-create'),

]



