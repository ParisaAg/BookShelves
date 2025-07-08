# books/serializers.py

from rest_framework import serializers
from django.db.models import Avg
from .models import Book, Category, Author, Discount

# سریالایزرهای ساده برای نمایش اطلاعات تو در تو (Nested)
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'bio']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class SimpleDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['name', 'discount_percent', 'end_date']


# --- سریالایزر اصلی کتاب ---
class BookSerializer(serializers.ModelSerializer):
    # نمایش اطلاعات کامل به صورت فقط خواندنی (برای GET)
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    active_discount = SimpleDiscountSerializer(source='get_active_discount', read_only=True)

    # دریافت ID برای ایجاد یا ویرایش (برای POST, PUT)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), source='author', write_only=True, label="Author ID"
    )
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True, label="Category ID"
    )
    
    # فیلدهای محاسباتی و فقط خواندنی
    final_price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    on_sale = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Book
        # لیست کامل و صحیح فیلدها
        fields = [
            'id', 'title', 'description', 'price', 'final_price', 'on_sale', 
            'active_discount', 'author', 'category', 'published_year', 
            'inventory', 'is_available', 'cover_image', 'average_rating', 
            'views', 'sold', 'num_pages', 'language', 'publisher', 'created_at',
            # فیلدهای نوشتاری
            'author_id', 'category_id'
        ]
        
        extra_kwargs = {
            # فیلد عکس فقط برای ورودی (آپلود) استفاده می‌شود و در خروجی نمایش داده نمی‌شود
            'cover_image': {'write_only': True, 'required': False},
        }

    def get_on_sale(self, obj: Book) -> bool:
        """بررسی می‌کند که آیا کتاب تخفیف فعال دارد یا خیر"""
        return obj.get_active_discount is not None

    def get_average_rating(self, obj: Book) -> float:
        """میانگین امتیازات کتاب را محاسبه می‌کند"""
        # فرض بر این است که مدلی به نام Review با related_name='reviews' به Book متصل است
        if hasattr(obj, 'reviews'):
            avg = obj.reviews.aggregate(rating_avg=Avg('rating'))['rating_avg']
            return round(avg, 1) if avg else 0
        return 0


# --- سریالایزر برای مدیریت تخفیف‌ها ---
class DiscountSerializer(serializers.ModelSerializer):
    # در نمایش، اطلاعات کامل کتاب‌ها نشان داده می‌شود
    books = BookSerializer(many=True, read_only=True)
    
    # در ورودی، فقط لیست ID کتاب‌ها دریافت می‌شود
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