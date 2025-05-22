from rest_framework import generics, filters
from .models import Book
from .serializers import BookSerializer
from django_filters.rest_framework import DjangoFilterBackend



class BookListView(generics.ListAPIView):
    queryset = Book.objects.all().order_by('-published_date')
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author']  # قابلیت فیلتر
    search_fields = ['title', 'description']  # قابلیت جستجو
    ordering_fields = ['published_date', 'price']  # مرتب‌سازی
    ordering = ['-published_date']  # ترتیب پیش‌فرض
