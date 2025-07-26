from django_filters import rest_framework as filters
from .models import Book

class BookFilter(filters.FilterSet):
    price = filters.RangeFilter()

    class Meta:
        model = Book
        fields = {
            'price': ['exact'],
            'level': ['exact'],
            'book_type': ['exact'],
            'language': ['exact'],
            'is_available': ['exact'],
            'category__id': ['exact'],
            'author__id': ['exact'],
        }