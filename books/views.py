from django.db.models import Sum
from django.utils import timezone
from rest_framework import viewsets, generics, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book, Category, Author, Discount
from .serializers import BookSerializer, CategorySerializer, AuthorSerializer, DiscountSerializer
from .permission import IsAdminOrStaff  
from orders.models import Order 
from .filters import BookFilter


class BookViewSet(viewsets.ModelViewSet):

    serializer_class = BookSerializer
    queryset = Book.objects.select_related('author', 'category').prefetch_related('discounts', 'reviews').all().order_by('-created_at')
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BookFilter
    search_fields = [
        'title',
        'author__first_name',
        'author__last_name',
        'category__name',
        'publisher',
        'description'
    ]
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

    @action(detail=True, methods=['get'])
    def related(self, request, pk=None):
        book = self.get_object()
        if not book.category:
            return Response([])

        related_books = Book.objects.filter(category=book.category).exclude(pk=book.pk).order_by('?')[:5]
        serializer = self.get_serializer(related_books, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def download(self, request, pk=None):
        book = self.get_object()

        if not book.digital_file_link:
            return Response({'error': 'No digital file available for this book.'}, status=status.HTTP_404_NOT_FOUND)

        is_free_digital = book.book_type == Book.BookType.DIGITAL
        has_purchased = Order.objects.filter(user=request.user, items__book_id=book.id, status='Completed').exists()

        if has_purchased or is_free_digital:
            return Response({'download_link': book.digital_file_link})
        else:
            return Response({'error': 'You must purchase this book to download it.'}, status=status.HTTP_403_FORBIDDEN)



class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrStaff] 
    
    def get_queryset(self):

        if self.action == 'list':
            return Category.objects.filter(parent__isnull=True, is_active=True)
        
        return Category.objects.filter(is_active=True)

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    #permission_classes = [IsAdminOrStaff]
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


class PopularCategoriesView(generics.ListAPIView):

    serializer_class = CategorySerializer 
    
    def get_queryset(self):
        queryset = Category.objects.annotate(
            total_sold=Sum('books__sold')
        ).order_by('-total_sold')[:5] 
        
        return queryset
    