# admin.py

from django.contrib import admin
from .models import Product, Link  # Импортируем модели

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('url', 'name', 'sizes','updated_at', 'created_at')
    search_fields = ('name',)

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('url',)
    search_fields = ('url',)
