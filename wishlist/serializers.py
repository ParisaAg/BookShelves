# wishlists/serializers.py
from rest_framework import serializers
from .models import Wishlist, WishlistItem
from books.serializers import BookSerializer # Reuse your existing BookSerializer

class WishlistItemSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = WishlistItem
        fields = ['id', 'book', 'added_at']

class WishlistSerializer(serializers.ModelSerializer):
    items = WishlistItemSerializer(many=True, read_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'created_at', 'items']