# books/serializers.py

from rest_framework import serializers
from django.db.models import Avg
from .models import Book, Category, Author, Discount

class AuthorSerializer(serializers.ModelSerializer):
    """سریالایزر ساده برای نمایش اطلاعات نویسنده"""
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'bio']

class CategorySerializer(serializers.ModelSerializer):
    """سریالایزر ساده برای نمایش اطلاعات دسته‌بندی"""
    class Meta:
        model = Category
        fields = ['id', 'name']

class SimpleDiscountSerializer(serializers.ModelSerializer):
    """سریالایزر ساده برای نمایش اطلاعات تخفیف فعال روی کتاب"""
    class Meta:
        model = Discount
        fields = ['name', 'discount_percent', 'end_date']


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    active_discount = SimpleDiscountSerializer(source='get_active_discount', read_only=True)

    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), source='author', write_only=True, label="Author ID"
    )
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True, label="Category ID"
    )
    
    final_price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    on_sale = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    cover_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'description', 'price', 
            'inventory', 'is_available', 'published_year', 
            'num_pages', 'language', 'publisher',
            
            'final_price', 'on_sale', 'active_discount',
            'average_rating',
            
            'author', 'category', 
    
            'views', 'sold', 'created_at',

            'cover_image_url',
            
            'cover_image', 
            'author_id', 
            'category_id',
        ]
        
        extra_kwargs = {
            'cover_image': {'write_only': True, 'required': False},
        }

    def get_cover_image_url(self, obj: Book) -> str | None:
        if obj.cover_image and hasattr(obj.cover_image, 'url'):
            return obj.cover_image.url
        return None

    def get_on_sale(self, obj: Book) -> bool:
        return obj.get_active_discount is not None

    def get_average_rating(self, obj: Book) -> float:
        if hasattr(obj, 'reviews'):
            avg = obj.reviews.aggregate(rating_avg=Avg('rating'))['rating_avg']
            return round(avg, 1) if avg else 0
        return 0


class DiscountSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)
    
    book_ids = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(), 
        source='books', 
        many=True, 
        write_only=True
    )
    
    class Meta:
        model = Discount
        fields = [
            'id', 'name', 'discount_percent', 'start_date', 'end_date', 
            'is_active', 'books', 'book_ids'
        ]