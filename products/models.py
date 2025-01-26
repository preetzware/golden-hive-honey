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
    has_weight = models.BooleanField(default=False)
    weight_prices = models.JSONField(
        null=True,
        blank=True,
        help_text="JSON format: {'295g': 14.99, '300g': 16.99, '350g': 18.99, '500g': 29.99}"
    )  # Stores weight-price mapping as JSON
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    price_range = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="For honey products with weights: e.g., '€14.99 - €29.99'"
    )  # Field for honey products that have weight
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=500, null=True, blank=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name

    def get_image(self):
        return self.image_url or None

    def save(self, *args, **kwargs):
        """
        Automatically generate a price range for products with weight_prices.
        """
        if self.has_weight and self.weight_prices:
            prices = self.weight_prices.values()
            if prices:
                min_price = min(prices)
                max_price = max(prices)
                self.price_range = f"€{min_price:.2f} - €{max_price:.2f}"
        else:
            self.price_range = None
        super().save(*args, **kwargs)
