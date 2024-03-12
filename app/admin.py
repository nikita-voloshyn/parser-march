from django.contrib import admin
from .models import Product, Size

class SizeInline(admin.TabularInline):  # Или используйте admin.StackedInline для другого отображения
    model = Size
    extra = 1  # Количество пустых форм для новых объектов

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'name', 'price')
    search_fields = ('product_id', 'name')
    inlines = [SizeInline]
