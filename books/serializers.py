# books/serializers.py

from rest_framework import serializers
from django.db.models import Avg
from .models import Book, Category, Author, Discount

# --- سریالایزرهای کمکی برای نمایش ---
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


# --- سریالایزر اصلی کتاب (نسخه نهایی و اصلاح شده) ---
class BookSerializer(serializers.ModelSerializer):
    # بخش نمایشی (فقط خواندنی)
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    active_discount = SimpleDiscountSerializer(source='get_active_discount', read_only=True)

    # بخش ورودی (فقط نوشتنی) - برای ساخت و ویرایش کتاب
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), source='author', write_only=True, label="Author ID"
    )
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True, label="Category ID"
    )
    
    # بخش فیلدهای محاسباتی (فقط خواندنی)
    final_price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    on_sale = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Book
        # لیست کامل و نهایی تمام فیلدها برای جلوگیری از خطای AssertionError
        fields = [
            'id', 'title', 'description', 'price', 
            'final_price', 'on_sale', 'active_discount',
            'author', 'category', 'published_year', 
            'inventory', 'is_available', 'cover_image', 
            'average_rating', 'views', 'sold', 'num_pages', 
            'language', 'publisher', 'created_at',
            
            # فیلدهای نوشتاری که حتما باید در لیست باشند
            'author_id', 
            'category_id'
        ]
        
        extra_kwargs = {
            # فیلد عکس فقط برای ورودی (آپلود) است و در خروجی نمایش داده نمی‌شود
            'cover_image': {'write_only': True, 'required': False},
        }

    def get_on_sale(self, obj: Book) -> bool:
        """بررسی می‌کند که آیا کتاب تخفیف فعال دارد یا خیر"""
        return obj.get_active_discount is not None

    def get_average_rating(self, obj: Book) -> float:
        """میانگین امتیازات کتاب را محاسبه می‌کند"""
        if hasattr(obj, 'reviews'):
            avg = obj.reviews.aggregate(rating_avg=Avg('rating'))['rating_avg']
            return round(avg, 1) if avg else 0
        return 0


# --- سریالایزر برای مدیریت کامل تخفیف‌ها ---
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