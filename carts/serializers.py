
from rest_framework import serializers
from .models import Cart, CartItem
from books.models import Book 

class SimpleBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'price', 'cover_image']


class CartItemSerializer(serializers.ModelSerializer):
    book = SimpleBookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(), source='book', write_only=True
    )
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'book', 'book_id', 'quantity', 'total_price']

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.book.price


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart

        fields = ['id', 'created_at', 'items', 'total_price']

    def get_total_price(self, cart: Cart):

        return sum([item.quantity * item.book.price for item in cart.items.all()])