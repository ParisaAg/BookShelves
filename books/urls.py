from django.urls import path, include
from rest_framework_nested import routers
from reviews.views import ReviewViewSet
from .views import (
    BookViewSet,
    CategoryViewSet,
    AuthorViewSet,
    LatestBooksView,
    TrendingBooksView,
    TopSellersView,
    DiscountViewSet,
    PopularCategoriesView,
)

# Main router for books
router = routers.SimpleRouter()
router.register(r'', BookViewSet, basename='book')  # Books list & detail by ID
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'discounts', DiscountViewSet, basename='discount')

books_router = routers.NestedSimpleRouter(router, r'', lookup='pk')
books_router.register(r'reviews', ReviewViewSet, basename='book-reviews')

urlpatterns = [


    path('latest-books/', LatestBooksView.as_view(), name='latest-books'),
    path('trending-books/', TrendingBooksView.as_view(), name='trending-books'),
    path('top-sellers/', TopSellersView.as_view(), name='top-sellers'),
    path('popular-cat/', PopularCategoriesView.as_view(), name='popular-cat'),

    # Include the main and nested routers
    path('', include(router.urls)),
    path('', include(books_router.urls)),
]
