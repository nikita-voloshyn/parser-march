from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models import JSONField


class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.title

class Product(models.Model):
    url = models.URLField(max_length=1024)
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3)
    customized = models.BooleanField(default=False)
    product_id = models.CharField(max_length=100, unique=True)
    variation_count = models.IntegerField(default=0)
    shipping_from = models.CharField(max_length=100, blank=True, null=True)
    categories = models.ManyToManyField(Category, related_name='products')
    images = JSONField(encoder=DjangoJSONEncoder, blank=True, default=list)
    seller_best_seller = models.BooleanField(default=False)
    seller_star_seller = models.BooleanField(default=False)
    seller_reviews_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image_url = models.URLField(max_length=1024)

    def __str__(self):
        return f"Image for {self.product.title}"