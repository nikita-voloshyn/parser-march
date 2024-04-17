from django.db import models

class Product(models.Model):
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Variant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    price = models.FloatField()
    name = models.CharField(max_length=255)
    item_detail = models.TextField()
    color = models.CharField(max_length=50)
    international_shipment = models.BooleanField()
    unique_key = models.CharField(max_length=255)
    size = models.CharField(max_length=10)
    width = models.CharField(max_length=20)
