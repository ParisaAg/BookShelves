
from rest_framework import serializers
from .models import Cart, CartItem
from books.models import Book

class SimpleBookSerializer(serializers.ModelSerializer):
    final_price = serializers.ReadOnlyField() 
    cover_image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'cover_image_url', 'final_price']
        
    def get_cover_image_url(self, obj: Book) -> str | None:
        if obj.cover_image and hasattr(obj.cover_image, 'url'):
            return obj.cover_image.url
        return None


class CartItemSerializer(serializers.ModelSerializer):
    book = SimpleBookSerializer(read_only=True)
    total_price = serializers.ReadOnlyField() 

    class Meta:
        model = CartItem
        fields = ['id', 'book', 'quantity', 'total_price']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'items', 'total_price']



class AddCartItemSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, default=1)

    def validate_book_id(self, value):
        if not Book.objects.filter(pk=value).exists():
            raise serializers.ValidationError("No book with the given ID was found.")
        return value


class UpdateCartItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)