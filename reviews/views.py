# reviews/views.py
from rest_framework import viewsets, permissions
from .models import Review, Book
from .serializers import ReviewSerializer

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        book_pk = self.kwargs.get('book_pk')
        return Review.objects.filter(book_id=book_pk)

    def perform_create(self, serializer):
        book_pk = self.kwargs.get('book_pk')
        book = Book.objects.get(pk=book_pk)
        
        Review.objects.update_or_create(
            user=self.request.user, 
            book=book,
            defaults={
                'rating': serializer.validated_data['rating'],
                'comment': serializer.validated_data.get('comment', '')
            }
        )