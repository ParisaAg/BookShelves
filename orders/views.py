# orders/views.py
import requests
import json
from django.db import transaction
from django.conf import settings
from django.shortcuts import redirect
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import Order, OrderItem
from carts.models import Cart
from accounts.models import Address
from .serializers import OrderSerializer, CheckoutSerializer

#this is for check 
ZARINPAL_REQUEST_URL = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZARINPAL_VERIFY_URL = "https://api.zarinpal.com/pg/v4/payment/verify.json"
CALLBACK_URL = 'https://your-frontend-domain.com/payment/verify?order_id={order_id}'

class OrderViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.prefetch_related('items__book').filter(user=self.request.user)


class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        input_serializer = CheckoutSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        address_id = input_serializer.validated_data['address_id']
        user = request.user

        try:
            cart = Cart.objects.prefetch_related('items__book').get(user=user)
            if cart.items.count() == 0:
                return Response({'error': 'Your cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)
            
            shipping_address = Address.objects.get(id=address_id, user=user)
        except (Cart.DoesNotExist, Address.DoesNotExist):
            return Response({'error': 'Invalid cart or address.'}, status=status.HTTP_400_BAD_REQUEST)

        for item in cart.items.all():
            if item.book.book_type != 'digital' and item.book.inventory < item.quantity:
                return Response(
                    {'error': f"Not enough stock for '{item.book.title}'. Only {item.book.inventory} left."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        order = Order.objects.create(
            user=user,
            total_price=cart.total_price,
            shipping_address=shipping_address
        )
        
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                book=cart_item.book,
                quantity=cart_item.quantity,
                unit_price=cart_item.book.final_price
            )
            if cart_item.book.book_type != 'digital':
                cart_item.book.inventory -= cart_item.quantity
                cart_item.book.save(update_fields=['inventory'])
        
        cart.items.all().delete()
        

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PaymentVerificationView(APIView):

    def get(self, request, *args, **kwargs):
        # This is a placeholder for the real verification logic
        # which would check query params from the gateway and update the order status.
        return Response({"message": "This endpoint is ready for payment verification."})