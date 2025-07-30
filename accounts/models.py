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
    



class UserActivity(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Last Seen: {self.last_seen}"
    


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
    country = models.CharField(max_length=100, default="ایران")
    city = models.CharField(max_length=100)
    street_address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.city}"