# orders/views.py
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from carts.models import Cart
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.prefetch_related('items__book').filter(user=self.request.user)

    @transaction.atomic 
    def create(self, request, *args, **kwargs):

        try:
            cart = Cart.objects.get(user=request.user)
            if cart.items.count() == 0:
                return Response({'error': 'Your cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)
        except Cart.DoesNotExist:
            return Response({'error': 'You do not have a cart.'}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(user=request.user)
        
        total_price = 0
        for cart_item in cart.items.all():
            order_item = OrderItem.objects.create(
                order=order,
                book=cart_item.book,
                quantity=cart_item.quantity,
                unit_price=cart_item.book.final_price
            )
            total_price += order_item.quantity * order_item.unit_price
            
            if cart_item.book.book_type != 'digital':
                cart_item.book.inventory -= cart_item.quantity
                cart_item.book.save(update_fields=['inventory'])

        order.total_price = total_price
        order.save()

        cart.items.all().delete()
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)