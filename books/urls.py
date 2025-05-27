from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateAPIView,
    BookDeleteAPIView,
    BookUpdateAPIView
)
from .views import (
    CategoryListCreateView,
    LatestBooksView,
    CategoryRetrieveView,
    CategoryUpdateView,
    CategoryDeleteView,
    AuthorListView,
)

urlpatterns = [
    path('', BookListView.as_view(), name='book-list'),
    path('<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('create/', BookCreateAPIView.as_view(), name='book-create'),
    path('<int:id>/edit/', BookUpdateAPIView.as_view(), name='book-edit'),
    path('<int:id>/delete/', BookDeleteAPIView.as_view(), name='book-delete'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveView.as_view(), name='category-retrieve'),
    path('categories/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),
    path('authors/', AuthorListView.as_view(), name='author-list'),
    path('latest/', LatestBooksView.as_view(), name='latest-books'),

]