# your_app/urls.py

from django.urls import path, include
from rest_framework_nested import routers 
from rest_framework.routers import DefaultRouter
from reviews.views import ReviewViewSet
from .views import (
    BookViewSet,
    CategoryViewSet,
    AuthorViewSet,
    LatestBooksView,
    TrendingBooksView,
    TopSellersView,
    DiscountViewSet,
    PopularCategoriesView ,
  
)

router = DefaultRouter()

router.register(r'books', BookViewSet, basename='book')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'discounts', DiscountViewSet, basename='discount')
books_router = routers.NestedSimpleRouter(router, r'books', lookup='book')
books_router.register(r'reviews', ReviewViewSet, basename='book-reviews')

urlpatterns = [

    path('', include(router.urls)),
    path('', include(books_router.urls)),


    
    path('latest-books/', LatestBooksView.as_view(), name='latest-books'),
    path('trending-books/', TrendingBooksView.as_view(), name='trending-books'),
    path('top-sellers/', TopSellersView.as_view(), name='top-sellers'),
    path('popular-cat/', PopularCategoriesView.as_view(), name='popular-cat'),

    
]