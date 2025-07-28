from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField



class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, verbose_name="About Me")
    profile_picture = CloudinaryField('image', null=True, blank=True, folder='profile_pictures')
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"