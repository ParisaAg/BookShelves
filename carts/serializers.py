from rest_framework import serializers
from .models import CartItem,Cart


class CartItemSerializer(serializers.ModelSerializer):
    book = serializers.StringRelatedField()

    class Meta:
        model = CartItem
        fields = ['id', 'book', 'quantity']



class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'items']
