from django.db import models

class EtsyProduct(models.Model):
    url = models.URLField()
    # Добавьте другие поля по мере необходимости

class EtsyVariant(models.Model):
    product = models.ForeignKey(EtsyProduct, related_name='variants', on_delete=models.CASCADE)
    price = models.FloatField()
    name = models.TextField()
    item_detail = models.TextField()
    international_shipment = models.BooleanField()
    unique_key = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    size = models.FloatField()
    width = models.CharField(max_length=10)

    class Meta:
        unique_together = ('product', 'size', 'width')

class BootBarnProduct(models.Model):
    url = models.URLField()
    # Добавьте другие поля по мере необходимости

class BootBarnVariant(models.Model):
    product = models.ForeignKey(BootBarnProduct, related_name='variants', on_delete=models.CASCADE)
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
