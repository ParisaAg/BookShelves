# orders/views.py
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem
from carts.models import Cart
from .serializers import OrderSerializer,CheckoutSerializer 
from rest_framework.views import APIView
from django.db import transaction
from accounts.models import Address


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
                return Response({'error': 'سبد خرید شما خالی است.'}, status=status.HTTP_400_BAD_REQUEST)

            shipping_address = Address.objects.get(id=address_id, user=user)
        except (Cart.DoesNotExist, Address.DoesNotExist):
            return Response({'error': 'سبد خرید یا آدرس نامعتبر است.'}, status=status.HTTP_400_BAD_REQUEST)

        for item in cart.items.all():
            if item.book.book_type != 'digital' and item.book.inventory < item.quantity:
                return Response(
                    {'error': f"موجودی کتاب '{item.book.title}' کافی نیست. فقط {item.book.inventory} عدد باقی مانده."},
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



