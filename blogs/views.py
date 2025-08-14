
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import F

from .models import Post, BlogCategory, Tag
from .serializers import PostListSerializer, PostDetailSerializer, BlogCategorySerializer, TagSerializer
from books.permission import IsAdminOrStaff 

class PostViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        if self.request.user.is_staff:
            return Post.objects.all()
        return Post.objects.filter(status='published', published_at__lte=timezone.now())

    def get_serializer_class(self):
        if self.action in ['list', 'most_viewed', 'recent']:
            return PostListSerializer
        return PostDetailSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminOrStaff]
        else:
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        return super().get_permissions()


    def retrieve(self, request, *args, **kwargs):
        post = self.get_object()
        post.view_count = F('view_count') + 1
        post.save(update_fields=['view_count'])
        post.refresh_from_db()
        serializer = self.get_serializer(post)
        return Response(serializer.data)


    @action(detail=False, methods=['get'])
    def most_viewed(self, request):
        queryset = self.get_queryset().order_by('-view_count')[:5] 
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        queryset = self.get_queryset().order_by('-published_at')[:5] 
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class BlogCategoryViewSet(viewsets.ModelViewSet):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    #lookup_field = 'pk'
    permission_classes = [IsAdminOrStaff]

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    #lookup_field = 'pk'
    permission_classes = [IsAdminOrStaff]