from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet,SubmitReviewView

router = DefaultRouter()
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
    path('submit-review/', SubmitReviewView.as_view()),
]
