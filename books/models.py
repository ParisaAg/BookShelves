from django.db import models
from cloudinary.models import CloudinaryField 
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from django.utils import timezone
from autoslug import AutoSlugField

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="نام دسته‌بندی")
    subtitle = models.CharField(max_length=255, blank=True, verbose_name="زیرعنوان")

    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name="دسته‌بندی والد"
    )
    
    slug = AutoSlugField(populate_from='name', unique=True, always_update=True, null=True, blank=True)
    
    description = models.TextField(blank=True, verbose_name="توضیحات")
    
    image = CloudinaryField(null=True, blank=True, folder='category_images', verbose_name="تصویر دسته‌بندی")

    is_active = models.BooleanField(default=True, verbose_name="فعال است؟")

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
        constraints = [
            models.CheckConstraint(check=~models.Q(pk=models.F('parent')), name='prevent_self_parentage')
        ]

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])

class Author(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
 
class Book(models.Model):
    class BookType(models.TextChoices):
        PHYSICAL = 'physical', 'فیزیکی'
        DIGITAL = 'digital', 'دیجیتال'
        BOTH = 'both', 'هر دو نسخه'

    class BookLevel(models.TextChoices):
        BEGINNER = 'beginner', 'مبتدی'
        INTERMEDIATE = 'intermediate', 'متوسط'
        ADVANCED = 'advanced', 'پیشرفته'

    title = models.CharField(max_length=255)
    is_available = models.BooleanField(default=True)
    inventory = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    description = models.TextField()
    published_year = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books')
    cover_image = CloudinaryField('image', null=True, blank=True, folder='book_covers')
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)      
    sold = models.PositiveIntegerField(default=0)  
    num_pages = models.PositiveIntegerField(default=0)
    language = models.CharField(max_length=100, blank=True)
    publisher = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    book_type = models.CharField(max_length=10, choices=BookType.choices, default=BookType.PHYSICAL)
    digital_file_link = models.URLField(max_length=1024, null=True, blank=True, verbose_name="لینک فایل دیجیتال")
    level = models.CharField(max_length=20, choices=BookLevel.choices, blank=True, null=True, verbose_name="سطح کتاب")


    @property
    def get_active_discount(self):
        now = timezone.now()
        return self.discounts.filter(is_active=True, start_date__lte=now, end_date__gte=now).first()

    @property
    def final_price(self):
        if self.book_type == self.BookType.DIGITAL:
            return Decimal('0.00')
        
        if self.price is None:
            return Decimal('0.00')

        active_discount = self.get_active_discount
        if active_discount:
            discount_amount = self.price * (Decimal(active_discount.discount_percent) / 100)
            return (self.price - discount_amount).quantize(Decimal('0.01'))
        
        return self.price

    def __str__(self):
        return self.title


class Discount(models.Model):
    name = models.CharField(max_length=255, verbose_name="campaign name")
    books = models.ManyToManyField('Book', related_name='discounts', verbose_name="discounted books")
    discount_percent = models.PositiveIntegerField(
        verbose_name="discount percentage",
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    start_date = models.DateTimeField(verbose_name="start date")
    end_date = models.DateTimeField(verbose_name="end date")
    is_active = models.BooleanField(default=True, verbose_name="is active?")

    def __str__(self):
        return f"{self.name} ({self.discount_percent}%)"

    class Meta:
        verbose_name = "discount"
        verbose_name_plural = "discounts"