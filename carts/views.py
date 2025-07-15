
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from .models import Cart, CartItem, Book
from .serializers import CartSerializer, AddCartItemSerializer, UpdateCartItemSerializer

class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return AddCartItemSerializer
        if self.action == 'partial_update':
            return UpdateCartItemSerializer
        return CartSerializer

    def list(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def create(self, request):
        serializer = AddCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book_id = serializer.validated_data['book_id']
        quantity = serializer.validated_data['quantity']

        book = Book.objects.get(id=book_id)
        if book.book_type == Book.BookType.DIGITAL:
            return Response({'error': 'Digital books cannot be added to the cart.'}, status=status.HTTP_400_BAD_REQUEST)

        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, book_id=book_id)
        
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        
        cart_item.save()
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        serializer = UpdateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quantity = serializer.validated_data['quantity']
            
        try:
            item = CartItem.objects.get(id=pk, cart__user=request.user)
            item.quantity = quantity
            item.save()
            cart = self.get_object() # get the cart to serialize
            return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not found in your cart.'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """حذف یک آیتم از سبد خرید."""
        try:
            item = CartItem.objects.get(id=pk, cart__user=request.user)
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not found.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['delete'])
    def clear(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart.items.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self):
      cart, _ = Cart.objects.get_or_create(user=self.request.user)
      return cart