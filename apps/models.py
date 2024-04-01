from django.db import models

class Product(models.Model):
    url = models.URLField()
    # Add other fields as needed

class Variant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    price = models.FloatField()
    name = models.TextField()
    item_detail = models.TextField()
    color = models.CharField(max_length=100)
    international_shipment = models.BooleanField()
    unique_key = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    size = models.FloatField()
    width = models.CharField(max_length=10)

    class Meta:
        unique_together = ('product', 'size', 'width')
