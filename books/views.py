# views.py

from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from .models import Book, Category, Author
from .serializers import BookSerializer, CategorySerializer, AuthorSerializer
from .permission import IsAdminOrStaff


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('-created_at')
    serializer_class = BookSerializer
    

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author_id', 'category_id'] 
    search_fields = [
        'title',
        'author__first_name', 
        'author__last_name', 
        'category__name'
        ]
    pagination_class = None
    ordering_fields = ['published_year', 'price', 'views', 'sold']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminOrStaff]
        else:
            self.permission_classes = []
        return super().get_permissions()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save(update_fields=['views'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrStaff] 
    pagination_class = None

class AuthorViewSet(viewsets.ModelViewSet):

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrStaff]
    pagination_class = None


class LatestBooksView(APIView):
    def get(self, request):
        books = Book.objects.order_by('-created_at')[:10]
        serializer = BookSerializer(books, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class TrendingBooksView(APIView):
    def get(self, request):
        books = Book.objects.order_by('-views')[:10]
        serializer = BookSerializer(books, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class TopSellersView(APIView):
    def get(self, request):
        books = Book.objects.order_by('-sold')[:10]
        serializer = BookSerializer(books, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    



#test

    #if wanna test this view, you can use the following code in postman:
        """
    این ViewSet به تنهایی تمام عملیات مربوط به کتاب را انجام می‌دهد:
    - GET /books/: لیست تمام کتاب‌ها (با فیلتر و جستجو)
    - POST /books/: ساختن یک کتاب جدید (با آپلود عکس)
    - GET /books/{id}/: نمایش جزئیات یک کتاب (با شمارش بازدید)
    - PUT /books/{id}/: آپدیت کامل یک کتاب
    - PATCH /books/{id}/: آپدیت بخشی از یک کتاب
    - DELETE /books/{id}/: حذف یک کتاب
    """