# carts/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from .models import Cart, CartItem, Book
from .serializers import CartSerializer, AddCartItemSerializer, UpdateCartItemSerializer,CartItemSerializer

class CartViewSet(viewsets.ModelViewSet):
    """
    A complete ViewSet for managing the user's shopping cart.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return CartItem.objects.filter(cart__user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return AddCartItemSerializer
        if self.action == 'update' or self.action == 'partial_update':
            return UpdateCartItemSerializer
        return CartItemSerializer # Default serializer for lists/details

    def list(self, request, *args, **kwargs):

        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book_id = serializer.validated_data['book_id']
        quantity = serializer.validated_data['quantity']
        
        try:
            book = Book.objects.get(id=book_id)
            if book.book_type == Book.BookType.DIGITAL:
                return Response({'error': 'Digital books cannot be added to the cart.'}, status=status.HTTP_400_BAD_REQUEST)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found.'}, status=status.HTTP_404_NOT_FOUND)

        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, book_id=book_id)
        
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        
        cart_item.save()
        
        cart_serializer = CartSerializer(cart)
        return Response(cart_serializer.data, status=status.HTTP_200_OK)
        
    @action(detail=False, methods=['delete'])
    def clear(self, request):

        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart.items.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)