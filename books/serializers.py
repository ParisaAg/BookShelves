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

    class Meta:
        model = Book
   
        fields = [
            'id', 'title', 'description', 'price', 'published_year', 'inventory',
            'is_available', 'created_at', 'views', 'sold',
            'author', 'author_id',
            'category', 'category_id',
            'cover_image', 'cover_image_url',
            'average_rating'
        ]
        
       
        extra_kwargs = {
            'cover_image': {'write_only': True}
        }
    
        read_only_fields = ['views', 'sold', 'created_at']

    
    def get_cover_image_url(self, obj):
        if obj.cover_image and hasattr(obj.cover_image, 'url'):
            return obj.cover_image.url
        return None 

    def get_average_rating(self, obj):
        # این کد شما عالی بود، فقط در صورت نبودن مدل Review خطا می‌دهد
        # مطمئن شوید مدل Review با related_name='reviews' به Book متصل است
        if hasattr(obj, 'reviews'):
            avg = obj.reviews.aggregate(avg=Avg('rating'))['avg']
            return round(avg, 1) if avg else 0
        return 0
