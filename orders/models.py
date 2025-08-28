from django.db import models
from django.conf import settings
from books.models import Book
from decimal import Decimal

class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "در انتظار پرداخت"),
        ("paid", "پرداخت شده"),
        ("shipped", "ارسال شده"),
        ("completed", "تکمیل شده"),
        ("canceled", "لغو شده"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self) -> Decimal:
        return sum([item.total_price for item in self.items.all()])

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self) -> Decimal:
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.book.title} (Order {self.order.id})"
