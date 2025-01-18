from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'friendly_name')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'rating', 'display_image')
    list_filter = ('category', 'price', 'rating')
    search_fields = ('name', 'description')
    ordering = ('name',)
    list_editable = ('price', 'rating')  # Optional for inline editing

    def display_image(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" style="width: 50px; height: auto;" />', obj.image_url)
        return "No Image"
    display_image.short_description = "Image"
