from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.


class Banner(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    image_url = CloudinaryField('banners')
    button_text = models.CharField(max_length=50, blank=True, null=True)
    button_link = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    gradient_from = models.CharField(max_length=20, default="#000000")
    gradient_to = models.CharField(max_length=20, default="#ffffff")
    def __str__(self):
        return self.title


class Announcement(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message