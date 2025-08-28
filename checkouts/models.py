from django.db import models
from django.conf import settings
from orders.models import Order

class Payment(models.Model):
    METHOD_CHOICES = [
        ("online", "پرداخت آنلاین"),
        ("cash", "پرداخت در محل"),
    ]

    STATUS_CHOICES = [
        ("initiated", "شروع شده"),
        ("pending", "در انتظار تایید"),
        ("successful", "موفق"),
        ("failed", "ناموفق"),
        ("canceled", "لغو شده"),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, default="online")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="initiated")
    authority = models.CharField(max_length=255, blank=True, null=True)
    ref_id = models.CharField(max_length=255, blank=True, null=True)
    amount = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.status}"
