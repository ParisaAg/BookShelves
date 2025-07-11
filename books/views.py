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
from .permission import IsAdminOrStaff  


class BookViewSet(viewsets.ModelViewSet):

    serializer_class = BookSerializer
    
    queryset = Book.objects.select_related('author', 'category').prefetch_related('discounts', 'reviews').all()
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__id', 'author__id', 'is_available']
    search_fields = ['title', 'author__first_name', 'author__last_name', 'description']
    ordering_fields = ['published_year', 'price', 'views', 'sold']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminOrStaff]
        else:
            # برای لیست و جزئیات، همه دسترسی دارند
            self.permission_classes = []
        return super().get_permissions()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save(update_fields=['views'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='discounted')
    def list_discounted_books(self, request):
        now = timezone.now()
        discounted_books = self.get_queryset().filter(
            discounts__is_active=True,
            discounts__start_date__lte=now,
            discounts__end_date__gte=now
        ).distinct()

        page = self.paginate_queryset(discounted_books)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(discounted_books, many=True)
        return Response(serializer.data)
    @action(detail=True, methods=['get'])
    def related(self, request, pk=None):

        book = self.get_object()

        if not book.category:
            return Response([])
        
        related_books = Book.objects.filter(
            category=book.category
        ).exclude(
            pk=book.pk
        ).order_by('?')[:5]

        serializer = self.get_serializer(related_books, many=True)
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


class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [IsAdminOrStaff]



class LatestBooksView(generics.ListAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.select_related('author', 'category').order_by('-created_at')[:10]


class TrendingBooksView(generics.ListAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.select_related('author', 'category').order_by('-views')[:10]


class TopSellersView(generics.ListAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.select_related('author', 'category').order_by('-sold')[:10]