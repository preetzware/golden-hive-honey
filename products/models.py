from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=254, unique=True)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name or self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    has_weight = models.BooleanField(default=False)  # Indicates if the product has weight options
    weight_prices = models.JSONField(
    null=True, 
    blank=True, 
    help_text="JSON format: {'295g': 14.99, '300g': 16.99, '350g': 18.99, '500g': 29.99}")# Stores weight-price mapping as JSON
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)  # Adjusted
    image_url = models.URLField(max_length=500, null=True, blank=True)  # Reduced max_length

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name

    def get_image(self):
        return self.image_url or None 
