# orders/serializers.py
from rest_framework import serializers
from .models import Order, OrderItem
from books.serializers import SimpleBookSerializer 

class OrderItemSerializer(serializers.ModelSerializer):
    book = SimpleBookSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'book', 'quantity', 'unit_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'created_at', 'total_price', 'items', 'shipping_address']




class CheckoutSerializer(serializers.Serializer):
    address_id = serializers.IntegerField()
