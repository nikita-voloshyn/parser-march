from django.db import models

class Product(models.Model):
    product_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

class Size(models.Model):
    product = models.ForeignKey(Product, related_name='sizes', on_delete=models.CASCADE)
    valueId = models.CharField(max_length=10)
    value = models.CharField(max_length=10)
    stock = models.CharField(max_length=50)
    shipping = models.CharField(max_length=100)
    isSameDayShippingWindow = models.BooleanField(default=False)
    quantitySourceType = models.CharField(max_length=50)
    href = models.URLField(max_length=200)
    selectable = models.BooleanField(default=False)
