# blog/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.utils import timezone
from .models import Post, BlogCategory, Tag
from .serializers import PostListSerializer, PostDetailSerializer, BlogCategorySerializer, TagSerializer
from books.permission import IsAdminOrStaff 

class PostViewSet(viewsets.ModelViewSet):

    lookup_field = 'slug' 

    def get_queryset(self):
        if self.request.user.is_staff:
            return Post.objects.all()
        return Post.objects.filter(status='published', published_at__lte=timezone.now())

    def get_serializer_class(self):

        if self.action == 'retrieve':
            return PostDetailSerializer
        return PostListSerializer

    def get_permissions(self):

        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminOrStaff]
        else:
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        return super().get_permissions()

class BlogCategoryViewSet(viewsets.ModelViewSet):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrStaff]

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrStaff]