from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import Wishlist, WishlistItem, Book
from .serializers import WishlistSerializer

class WishlistViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]

    def list(self, request):
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='add-item')
    def add_to_wishlist(self, request):
        book_id = request.data.get('book_id')
        if not book_id:
            return Response({'error': 'Book ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found.'}, status=status.HTTP_404_NOT_FOUND)

        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        item, item_created = WishlistItem.objects.get_or_create(wishlist=wishlist, book=book)

        if not item_created:
            return Response({'message': 'Book is already in your wishlist.'}, status=status.HTTP_200_OK)

        return Response(WishlistSerializer(wishlist).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='remove-item')
    def remove_from_wishlist(self, request):
        book_id = request.data.get('book_id')
        if not book_id:
            return Response({'error': 'Book ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            wishlist = Wishlist.objects.get(user=request.user)
            item = WishlistItem.objects.get(wishlist=wishlist, book_id=book_id)
            item.delete()
            return Response(WishlistSerializer(wishlist).data, status=status.HTTP_200_OK)
        except (Wishlist.DoesNotExist, WishlistItem.DoesNotExist):
            return Response({'error': 'Item not found in your wishlist.'}, status=status.HTTP_404_NOT_FOUND)