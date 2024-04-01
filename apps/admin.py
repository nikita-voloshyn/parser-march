from django.contrib import admin
from .models import Product, Size

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'created_at', 'updated_at']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['image_links']

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['product', 'size', 'width']
    search_fields = ['product__name']
