from django.db import models
from django.conf import settings
from autoslug import AutoSlugField
from cloudinary.models import CloudinaryField

class BlogCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="نام دسته‌بندی")
    slug = AutoSlugField(populate_from='name', unique=True, always_update=True, allow_unicode=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "دسته‌بندی بلاگ"
        verbose_name_plural = "دسته‌بندی‌های بلاگ"

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="نام تگ")
    slug = AutoSlugField(populate_from='name', unique=True, always_update=True, allow_unicode=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "تگ"
        verbose_name_plural = "تگ‌ها"

class Post(models.Model):
    class PostStatus(models.TextChoices):
        DRAFT = 'draft', 'پیش‌نویس'
        PUBLISHED = 'published', 'منتشر شده'

    title = models.CharField(max_length=255, verbose_name="عنوان پست")
    slug = AutoSlugField(populate_from='title', unique=True, always_update=True, allow_unicode=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='blog_posts')
    content = models.TextField(verbose_name="محتوای پست")
    status = models.CharField(max_length=10, choices=PostStatus.choices, default=PostStatus.DRAFT)
    
    cover_image = CloudinaryField(null=True, blank=True, folder='blog_covers', verbose_name="عکس کاور")

    source_url = models.URLField(max_length=1024, blank=True, null=True, verbose_name="لینک منبع")

    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')

    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True, verbose_name="تاریخ انتشار")

    class Meta:
        ordering = ['-published_at']
        verbose_name = "پست"
        verbose_name_plural = "پست‌ها"

    def __str__(self):
        return self.title

class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField('image', folder='blog_gallery_images')
    caption = models.CharField(max_length=255, blank=True, verbose_name="عنوان عکس")

    def __str__(self):
        return f"Image for post: {self.post.title}"