# your_app/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    BookViewSet,
    CategoryViewSet,
    AuthorViewSet,
    LatestBooksView,
    TrendingBooksView,
    TopSellersView,
)

router = DefaultRouter()

router.register(r'books', BookViewSet, basename='book')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'authors', AuthorViewSet, basename='author')

urlpatterns = [
    path('', include(router.urls)),

    path('latest-books/', LatestBooksView.as_view(), name='latest-books'),
    path('trending-books/', TrendingBooksView.as_view(), name='trending-books'),
    path('top-sellers/', TopSellersView.as_view(), name='top-sellers'),
]