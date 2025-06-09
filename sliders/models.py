
from django.db import models
from cloudinary.models import CloudinaryField

class SliderImage(models.Model):
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='test/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"SliderImage {self.id}"
    
