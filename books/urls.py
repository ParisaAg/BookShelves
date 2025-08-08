# books/urls.py
from django.urls import path, include
from rest_framework_nested import routers
from .views import (
    BookViewSet, CategoryViewSet, AuthorViewSet, DiscountViewSet,
    LatestBooksView, TrendingBooksView, TopSellersView, PopularCategoriesView
)
from reviews.views import ReviewViewSet

router = routers.SimpleRouter()
router.register(r'', BookViewSet, basename='book') 
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'discounts', DiscountViewSet, basename='discount')

books_router = routers.NestedSimpleRouter(router, r'', lookup='slug')
books_router.register(r'reviews', ReviewViewSet, basename='book-reviews')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(books_router.urls)),
    
    # These paths create the URLs you are trying to access
    path('latest-books/', LatestBooksView.as_view(), name='latest-books'),
    path('trending-books/', TrendingBooksView.as_view(), name='trending-books'),
    path('top-sellers/', TopSellersView.as_view(), name='top-sellers'),
    path('popular-categories/', PopularCategoriesView.as_view(), name='popular-categories'),
]