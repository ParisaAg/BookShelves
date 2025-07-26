
from rest_framework import serializers
from django.db.models import Avg
from .models import Book, Category, Author, Discount


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'bio']

class CategorySerializer(serializers.ModelSerializer):
    parent_name = serializers.CharField(source='parent.name', read_only=True, allow_null=True)
    
    children = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = [
            'id', 
            'name', 
            'slug', 
            'parent',  
            'parent_name', 
            'children'
        ]
        
        extra_kwargs = {
            'parent': {'write_only': True, 'required': False}
        }

    def get_children(self, obj):

        children = obj.children.filter(is_active=True)
        return CategorySerializer(children, many=True, context=self.context).data

class SimpleDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['name', 'discount_percent', 'end_date']

class SimpleBookSerializer(serializers.ModelSerializer):
    cover_image_url = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'cover_image_url']
        
    def get_cover_image_url(self, obj: Book) -> str | None:
        if obj.cover_image and hasattr(obj.cover_image, 'url'):
            return obj.cover_image.url
        return None


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
    
    final_price = serializers.SerializerMethodField()
    on_sale = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    cover_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'description', 'price', 'level',
            'inventory', 'is_available', 'published_year', 
            'num_pages', 'language', 'publisher', 'book_type',
            'final_price', 'on_sale', 'active_discount',
            'average_rating', 'author', 'category', 'views', 
            'sold', 'created_at', 'cover_image_url',
            'cover_image', 'author_id', 'category_id',
            'level'
        ]
        
        extra_kwargs = {
            'cover_image': {'write_only': True, 'required': False},
        }

    def get_final_price(self, obj: Book):
        numeric_price = obj.final_price
        if numeric_price == 0:
            return "رایگان"
        return numeric_price

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
    books = SimpleBookSerializer(many=True, read_only=True)
    
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