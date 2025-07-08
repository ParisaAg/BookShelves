
from .models import Book, Category, Author,Discount
from rest_framework import serializers
from django.db.models import Avg
from .models import Discount


class SimpleDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['name', 'discount_percent']

        
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name','bio'] 

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']



class BookSerializer(serializers.ModelSerializer):
    
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    
    
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), source='author', write_only=True
    )
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    cover_image_url = serializers.SerializerMethodField(read_only=True)
    average_rating = serializers.SerializerMethodField(read_only=True)
    #on_sale = serializers.SerializerMethodField(read_only=True)
    final_price = serializers.SerializerMethodField(read_only=True)
    active_discount = SimpleDiscountSerializer(source='get_active_discount', read_only=True)

    class Meta:
        model = Book
   
        fields = [
           'id', 'title', 'author', 'price', 
            'active_discount', 'final_price', 
            'cover_image', 'inventory', 'is_available','average_rating'
        ]
        
       
        extra_kwargs = {
            'cover_image': {'write_only': True},
            #'price': {'read_only': True} 

        }
    
        read_only_fields = ['views', 'created_at']

    def get_on_sale(self, obj):
        return obj.discount_percentage is not None and obj.discount_percentage > 0
            
    def get_final_price(self, obj):
        return obj.final_price
    

    def get_cover_image_url(self, obj):
        if obj.cover_image and hasattr(obj.cover_image, 'url'):
            return obj.cover_image.url
        return None 

    def get_average_rating(self, obj):
        if hasattr(obj, 'reviews'):
            avg = obj.reviews.aggregate(avg=Avg('rating'))['avg']
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
            'id', 
            'name', 
            'discount_percent', 
            'start_date', 
            'end_date', 
            'is_active',
            'books',      # این فیلد برای نمایش (GET) است
            'book_ids'    # این فیلد برای ورودی (POST, PUT) است
        ]
