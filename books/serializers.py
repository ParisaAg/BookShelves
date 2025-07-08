# books/serializers.py

from rest_framework import serializers
from django.db.models import Avg
from .models import Book, Category, Author, Discount

# یک سریالایزر ساده برای نمایش اطلاعات نویسنده و دسته‌بندی در سریالایزر کتاب
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

# یک سریالایزر ساده برای نمایش اطلاعات تخفیف فعال روی کتاب
class SimpleDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['name', 'discount_percent', 'end_date']


class BookSerializer(serializers.ModelSerializer):
    # نمایش اطلاعات کامل نویسنده و دسته‌بندی (فقط خواندنی)
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    # فیلدهایی برای ورودی (نوشتنی) هنگام ساخت یا ویرایش کتاب
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), source='author', write_only=True
    )
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )

    # فیلدهای محاسباتی که از مدل خوانده می‌شوند
    final_price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    on_sale = serializers.SerializerMethodField(read_only=True)
    average_rating = serializers.SerializerMethodField(read_only=True)
    
    # نمایش جزئیات تخفیف فعال (اگر وجود داشته باشد)
    active_discount = SimpleDiscountSerializer(source='get_active_discount', read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'description', 'price', 
            'final_price', 'on_sale', 'active_discount',
            'author', 'category', 'published_year', 'inventory', 
            'is_available', 'cover_image',
            'average_rating', 'views', 'sold','category_id'
            # فیلدهای نوشتاری
            'author_id', 'category_id'
        ]
        
        # مشخص کردن فیلدهایی که فقط برای ورودی هستند و در خروجی نمایش داده نمی‌شوند
        extra_kwargs = {
            'cover_image': {'write_only': True, 'required': False},
        }

    def get_on_sale(self, obj: Book):
        # این متد بررسی می‌کند که آیا تخفیف فعالی روی کتاب هست یا نه
        return obj.get_active_discount is not None

    def get_average_rating(self, obj: Book):
        # این متد میانگین امتیازات را محاسبه می‌کند (فرض بر وجود مدل Review)
        if hasattr(obj, 'reviews'):
            avg = obj.reviews.aggregate(avg=Avg('rating'))['avg']
            return round(avg, 1) if avg else 0
        return 0


# این سریالایزر برای مدیریت کامل تخفیف‌ها است
class DiscountSerializer(serializers.ModelSerializer):
    # برای نمایش، اطلاعات کامل کتاب‌هایی که شامل تخفیف هستند را نشان می‌دهیم
    books = BookSerializer(many=True, read_only=True)
    
    # برای ورودی (ساخت یا ویرایش تخفیف)، فقط ID کتاب‌ها را دریافت می‌کنیم
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