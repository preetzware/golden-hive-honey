# Generated by Django 5.1.4 on 2025-01-21 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_has_weight_product_weight_prices'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='weight_prices',
            field=models.JSONField(blank=True, help_text="JSON format: {'295g': 14.99, '300g': 16.99, '350g': 18.99, '500g': 29.99}", null=True),
        ),
    ]
