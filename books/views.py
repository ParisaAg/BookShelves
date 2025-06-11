# views.py

from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from .models import Book, Category, Author
from .serializers import BookSerializer, CategorySerializer, AuthorSerializer
from .permission import IsAdminOrStaff


# --- ViewSet ها جایگزین تمام کلاس های CRUD قبلی می شوند ---

class BookViewSet(viewsets.ModelViewSet):
    """
    این ViewSet به تنهایی تمام عملیات مربوط به کتاب را انجام می‌دهد:
    - GET /books/: لیست تمام کتاب‌ها (با فیلتر و جستجو)
    - POST /books/: ساختن یک کتاب جدید (با آپلود عکس)
    - GET /books/{id}/: نمایش جزئیات یک کتاب (با شمارش بازدید)
    - PUT /books/{id}/: آپدیت کامل یک کتاب
    - PATCH /books/{id}/: آپدیت بخشی از یک کتاب
    - DELETE /books/{id}/: حذف یک کتاب
    """
    queryset = Book.objects.all().order_by('-created_at')
    serializer_class = BookSerializer
    
    # تنظیمات فیلترینگ، جستجو و مرتب‌سازی
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author_id', 'category_id'] # فیلتر بر اساس ID
    search_fields = ['title', 'description']
    ordering_fields = ['published_year', 'price', 'views', 'sold']

    def get_permissions(self):
        # برای عملیات نوشتن (create, update, destroy) نیاز به دسترسی ادمین/استف با شد
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminOrStaff]
        # برای بقیه عملیات (list, retrieve) نیاز به دسترسی نیست
        else:
            self.permission_classes = []
        return super().get_permissions()

    def retrieve(self, request, *args, **kwargs):
        # بازنویسی متد retrieve برای اضافه کردن شمارنده بازدید
        instance = self.get_object()
        instance.views += 1
        instance.save(update_fields=['views'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    این ViewSet تمام عملیات مربوط به دسته‌بندی را انجام می‌دهد.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrStaff] # دسترسی فقط برای ادمین/استاف


class AuthorViewSet(viewsets.ModelViewSet):
    """
    این ViewSet تمام عملیات مربوط به نویسنده را انجام می‌دهد.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrStaff]


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