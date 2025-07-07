# BookShelvesApp/admin.py
from django.contrib import admin
from .models import Book, Category, Author, Discount 



@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount_percent', 'start_date', 'end_date', 'is_active')
    filter_horizontal = ('books',)