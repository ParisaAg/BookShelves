# books/serializers.py

from rest_framework import serializers
from .models import Order, OrderItem, Book

class OrderItemSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = OrderItem
        fields = ['book', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'created_at', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        
            book = item_data['book']
            #book.sold += item_data['quantity']
            book.inventory -= item_data['quantity']
            book.save()

        return order
    



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


