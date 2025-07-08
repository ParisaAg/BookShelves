# # views.py
# from django.utils import timezone
# from rest_framework import viewsets, filters, status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.decorators import action
# from .models import Book, Category, Author,Discount
# from .serializers import BookSerializer, CategorySerializer, AuthorSerializer,DiscountSerializer
# from .permission import IsAdminOrStaff


# class BookViewSet(viewsets.ModelViewSet):
#     queryset = Book.objects.all().order_by('-created_at')
#     serializer_class = BookSerializer
    

#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     filterset_fields = ['author_id', 'category_id'] 
#     search_fields = [
#         'title',
#         'author__first_name', 
#         'author__last_name', 
#         'category__name'
#         ]
    
#     ordering_fields = ['published_year', 'price', 'views', 'sold']

#     def get_permissions(self):
#         if self.action in ['create', 'update', 'partial_update', 'destroy']:
#             self.permission_classes = [IsAdminOrStaff]
#         else:
#             self.permission_classes = []
#         return super().get_permissions()
    
#     @action(detail=False, methods=['get'])
#     def discounted(self, request):
#         now = timezone.now()
        
#         discounted_books = Book.objects.filter(
#             discounts__is_active=True,
#             discounts__start_date__lte=now,
#             discounts__end_date__gte=now
#         ).distinct()

#         page = self.paginate_queryset(discounted_books)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)

#         serializer = self.get_serializer(discounted_books, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         instance.views += 1
#         instance.save(update_fields=['views'])
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)


# class CategoryViewSet(viewsets.ModelViewSet):

#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     permission_classes = [IsAdminOrStaff] 
#     pagination_class = None

# class AuthorViewSet(viewsets.ModelViewSet):

#     queryset = Author.objects.all()
#     serializer_class = AuthorSerializer
#     permission_classes = [IsAdminOrStaff]
#     pagination_class = None
#     throttle_classes = [] 


# class LatestBooksView(APIView):
#     def get(self, request):
#         books = Book.objects.order_by('-created_at')[:10]
#         serializer = BookSerializer(books, many=True, context={'request': request})
#         throttle_classes = [] 
#         return Response(serializer.data, status=status.HTTP_200_OK)

# class TrendingBooksView(APIView):
#     def get(self, request):
#         books = Book.objects.order_by('-views')[:10]
#         serializer = BookSerializer(books, many=True, context={'request': request})
#         throttle_classes = [] 

#         return Response(serializer.data, status=status.HTTP_200_OK)

# class TopSellersView(APIView):
#     def get(self, request):
#         books = Book.objects.order_by('-sold')[:10]
#         serializer = BookSerializer(books, many=True, context={'request': request})
#         throttle_classes = [] 

#         return Response(serializer.data, status=status.HTTP_200_OK)
    

# class DiscountViewSet(viewsets.ModelViewSet):
#     queryset = Discount.objects.all()
#     serializer_class = DiscountSerializer
#     permission_classes = [IsAdminOrStaff]
#     throttle_classes = [] 


# books/views.py

from django.utils import timezone
from rest_framework import viewsets, generics, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

from .models import Book, Category, Author, Discount
from .serializers import BookSerializer, CategorySerializer, AuthorSerializer, DiscountSerializer
from .permission import IsAdminOrStaff  # فرض بر این است که این فایل وجود دارد

# --- ViewSet های اصلی برای عملیات CRUD ---

class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet کامل برای کتاب‌ها با قابلیت جستجو، فیلتر، مرتب‌سازی و اکشن‌های سفارشی.
    """
    serializer_class = BookSerializer
    
    # بهینه‌سازی کوئری برای جلوگیری از ارسال درخواست‌های اضافی به دیتابیس
    queryset = Book.objects.select_related('author', 'category').prefetch_related('discounts', 'reviews').all()
    
    # ابزارهای فیلترینگ، جستجو و مرتب‌سازی
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__id', 'author__id', 'is_available']
    search_fields = ['title', 'author__first_name', 'author__last_name', 'description']
    ordering_fields = ['published_year', 'price', 'views', 'sold']

    def get_permissions(self):
        """تعیین سطح دسترسی بر اساس نوع اکشن (خواندن یا نوشتن)"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminOrStaff]
        else:
            # برای لیست و جزئیات، همه دسترسی دارند
            self.permission_classes = []
        return super().get_permissions()

    def retrieve(self, request, *args, **kwargs):
        """با هر بار مشاهده جزئیات کتاب، یک واحد به تعداد بازدیدها اضافه می‌شود"""
        instance = self.get_object()
        instance.views += 1
        instance.save(update_fields=['views'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='discounted')
    def list_discounted_books(self, request):
        """یک اکشن سفارشی برای نمایش لیست کتاب‌هایی که تخفیف فعال دارند"""
        now = timezone.now()
        discounted_books = self.get_queryset().filter(
            discounts__is_active=True,
            discounts__start_date__lte=now,
            discounts__end_date__gte=now
        ).distinct()

        # استفاده از سیستم صفحه‌بندی پیش‌فرض ViewSet
        page = self.paginate_queryset(discounted_books)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(discounted_books, many=True)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet برای دسته‌بندی‌ها (فقط ادمین و کارمندان)"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrStaff]
    pagination_class = None  # غیرفعال کردن صفحه‌بندی برای لیست دسته‌بندی‌ها


class AuthorViewSet(viewsets.ModelViewSet):
    """ViewSet برای نویسندگان (فقط ادمین و کارمندان)"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrStaff]
    pagination_class = None


class DiscountViewSet(viewsets.ModelViewSet):
    """ViewSet برای مدیریت تخفیف‌ها (فقط ادمین و کارمندان)"""
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [IsAdminOrStaff]


# --- View های سفارشی فقط خواندنی (ReadOnly) ---

class LatestBooksView(generics.ListAPIView):
    """نمایش ۱۰ کتاب جدید بر اساس تاریخ ایجاد"""
    serializer_class = BookSerializer
    queryset = Book.objects.select_related('author', 'category').order_by('-created_at')[:10]


class TrendingBooksView(generics.ListAPIView):
    """نمایش ۱۰ کتاب پرطرفدار بر اساس تعداد بازدید"""
    serializer_class = BookSerializer
    queryset = Book.objects.select_related('author', 'category').order_by('-views')[:10]


class TopSellersView(generics.ListAPIView):
    """نمایش ۱۰ کتاب پرفروش بر اساس تعداد فروش"""
    serializer_class = BookSerializer
    queryset = Book.objects.select_related('author', 'category').order_by('-sold')[:10]