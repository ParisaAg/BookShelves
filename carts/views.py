
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from .models import Cart, CartItem
from books.models import Book 
from .serializers import CartSerializer, CartItemSerializer

class CartViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]

    def list(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def create(self, request):
        book_id = request.data.get('book_id')
        quantity = int(request.data.get('quantity', 1))

        if not book_id:
            return Response({'error': 'Book ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found.'}, status=status.HTTP_404_NOT_FOUND)

        if book.book_type == Book.BookType.DIGITAL:
            return Response(
                {'error': 'کتاب‌های دیجیتال قابل افزودن به سبد خرید نیستند. لطفاً از لینک دانلود استفاده کنید.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)

        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        
        cart_item.save()
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        try:
            # توجه: pk شناسه CartItem است
            item = CartItem.objects.get(id=pk, cart__user=request.user)
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not found in your cart.'}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        quantity = int(request.data.get('quantity', 0))
        if quantity <= 0:
            return self.destroy(request, pk)
            
        try:
            item = CartItem.objects.get(id=pk, cart__user=request.user)
            item.quantity = quantity
            item.save()
            return Response(CartItemSerializer(item).data, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not found in your cart.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['delete'])
    def clear(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart.items.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)