# serializers.py

from .models import Book, Category, Author
from rest_framework import serializers
from django.db.models import Avg

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
    on_sale = serializers.SerializerMethodField(read_only=True)
    final_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Book
   
        fields = [
            'id', 'title', 'description', 'published_year', 'inventory',
            'is_available', 'created_at', 'views', 'sold',
            'num_pages', 'language', 'publisher',
            'author', 'author_id',
            'price', 'discount_price', 
            'final_price', 'on_sale', 
            'category', 'category_id',
            'cover_image', 'cover_image_url',
            'average_rating'
        ]
        
       
        extra_kwargs = {
            'cover_image': {'write_only': True},
            #'price': {'read_only': True} 

        }
    
        read_only_fields = ['views', 'created_at']

    def get_on_sale(self, obj):
        return obj.discount_price is not None
     
    def get_cover_image_url(self, obj):
        if obj.cover_image and hasattr(obj.cover_image, 'url'):
            return obj.cover_image.url
        return None 

    def get_average_rating(self, obj):
        if hasattr(obj, 'reviews'):
            avg = obj.reviews.aggregate(avg=Avg('rating'))['avg']
            return round(avg, 1) if avg else 0
        return 0
    
    def get_final_price(self, obj):
        return obj.final_price