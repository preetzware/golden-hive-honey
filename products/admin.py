from django.contrib import admin
from .models import Product, Category

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'friendly_name')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'rating', 'get_image')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    ordering = ('name',)