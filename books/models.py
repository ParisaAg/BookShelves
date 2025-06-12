from django.db import models
from cloudinary.models import CloudinaryField 
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Author(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
 
class Book(models.Model):
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
    price = models.DecimalField(max_digits=6, decimal_places=2)
    discount_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    @property
    def final_price(self):
        if self.discount_price:
            return self.discount_price
        return self.price
    def __str__(self):
        return self.title