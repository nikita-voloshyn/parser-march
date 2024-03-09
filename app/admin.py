from django.contrib import admin
from .models import Product, Category

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'currency', 'product_id']
    # Настройте другие опции админки по желанию

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']