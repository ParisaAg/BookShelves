from rest_framework import generics, filters
from rest_framework.generics import RetrieveAPIView,CreateAPIView,UpdateAPIView,DestroyAPIView,ListAPIView
from .models import Book,Category,Author
from .serializers import BookSerializer,CategorySerializer,AuthorSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .permission import IsAdminOrStaff



class BookListView(generics.ListAPIView):
    queryset = Book.objects.all().order_by('-published_date')
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author'] 
    search_fields = ['title', 'description']  
    ordering_fields = ['published_date', 'price']  
    ordering = ['-published_date']





class BookDetailView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer



class BookCreateAPIView(CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrStaff]


class BookUpdateAPIView(UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrStaff]
    lookup_field = 'id'



class BookDeleteAPIView(DestroyAPIView):
    queryset = Book.objects.all()
    permission_classes = [IsAdminOrStaff]
    lookup_field = 'id'




class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrStaff]

class CategoryRetrieveView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrStaff]

class CategoryUpdateView(generics.UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrStaff]

class CategoryDeleteView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrStaff]

class AuthorListView(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer



class LatestBooksView(ListAPIView):
    queryset = Book.objects.all().order_by('-created_at')[:10] 
    serializer_class = BookSerializer