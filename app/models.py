from django.db import models

class Product(models.Model):
    url = models.URLField(unique=True)
    name = models.CharField(max_length=255)
    sizes = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on create
    updated_at = models.DateTimeField(auto_now=True)  # Automatically updated on save

    def __str__(self):
        return self.name

class Link(models.Model):
    url = models.URLField(unique=True)
