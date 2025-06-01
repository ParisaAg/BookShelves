from django.shortcuts import render

from rest_framework import generics, permissions,status
from .models import Order,OrderItem
from carts.models import Cart
from .serializers import OrderSerializer,OrderInvoiceSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        cart, _ = Cart.objects.get_or_create(user=user)
        cart_items = cart.items.all()

        if not cart_items.exists():
            raise ValueError("Cart is empty.")

        # ساخت سفارش
        order = serializer.save(user=user)

        for item in cart_items:
            if item.quantity > item.book.inventory:
                raise ValueError(f"Not enough inventory for '{item.book.title}'.")

            # ساخت آیتم سفارش
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price=item.book.price
            )

            # به‌روزرسانی کتاب
            item.book.sold += item.quantity
            item.book.inventory = max(item.book.inventory - item.quantity, 0)
            item.book.save()

        # پاک‌سازی سبد خرید
        cart_items.delete()


class UserOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')




class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        
        return Order.objects.filter(user=self.request.user)
    



class CancelOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, user=request.user)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        if order.status != 'pending':
            return Response({"detail": "Only pending orders can be cancelled."}, status=status.HTTP_400_BAD_REQUEST)

        order.status = 'cancelled'
        order.save()

        return Response({"detail": "Order cancelled successfully."}, status=status.HTTP_200_OK)
    



class OrderInvoiceView(generics.RetrieveAPIView):
    serializer_class = OrderInvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise PermissionDenied("you don't have permission to access this order.")
        return obj