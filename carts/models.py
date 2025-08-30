
from django.db import models
from django.conf import settings
from books.models import Book
from django.core.validators import MinValueValidator
from decimal import Decimal

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self) -> Decimal:
        return sum([item.total_price for item in self.items.all()])

    def clear(self):
        self.items.all().delete()
        
    def __str__(self):
        return f"Cart for {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )

    @property
    def total_price(self) -> Decimal:
        return self.quantity * self.book.final_price

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cart', 'book'], name='unique_cart_book')
        ]
    def __str__(self):
        return f"{self.quantity} x {self.book.title} in cart {self.cart.id}"