

from rest_framework import serializers
from .models import Order, OrderItem, Book

class OrderItemSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['book_title', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField() 
    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'created_at', 'items']
    


class OrderItemInvoiceSerializer(serializers.ModelSerializer):
    book = serializers.StringRelatedField()

    class Meta:
        model = OrderItem
        fields = ['book', 'quantity', 'price']

class OrderInvoiceSerializer(serializers.ModelSerializer):
    items = OrderItemInvoiceSerializer(many=True, read_only=True)  
    user = serializers.StringRelatedField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'created_at', 'items']


