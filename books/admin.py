from django.contrib import admin
from .models import Author, Category, Book, Discount

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'slug', 'is_active')
    list_filter = ('is_active', 'parent')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)} 

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')
    search_fields = ('first_name', 'last_name')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'book_type', 'level', 'price', 'inventory', 'is_available')
    list_filter = ('book_type', 'level', 'is_available', 'category', 'author')
    search_fields = ('title', 'author__first_name', 'author__last_name')
    list_editable = ('price', 'inventory', 'is_available')
    autocomplete_fields = ('author', 'category')

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount_percent', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    filter_horizontal = ('books',) # A better UI for ManyToMany fields