from django.db import models

class Product(models.Model):
    # Базовые параметры товара
    code = models.CharField(max_length=50)  # Код товара
    title = models.CharField(max_length=255)  # Заголовок
    description = models.TextField()  # Описание
    category = models.CharField(max_length=100)  # Категория
    photos = models.JSONField(blank=True, null=True)  # Фотографии (массив ссылок)
    price = models.FloatField(default=0)  # Цена (float)
    quantity = models.IntegerField(default=1)  # Количество
    size = models.FloatField(blank=True, null=True, default=0)  # Размер в американской системе (float)
    size_2 = models.CharField(max_length=10)  # Ширина (встречается в обуви и одежде) (float)
    color = models.CharField(max_length=50)  # Цвет
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female'), ('U', 'Unisex')], default='U')  # Гендерная принадлежность (если одежда) (M/Ж/Д)
    warehouse = models.CharField(max_length=100)  # Склад - откуда товар
    showcase = models.CharField(max_length=100)  # Витрина - где опубликован
    url = models.URLField()  # URL
    created_at = models.DateTimeField(auto_now_add=True)  # Время создания
    updated_at = models.DateTimeField(auto_now=True)  # Время последнего обновления

class Variant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')  # Продукт, к которому относится вариант
    price = models.FloatField()  # Цена варианта
    title = models.CharField(max_length=255)  # Название варианта
    description = models.TextField()  # Описание варианта
    color = models.CharField(max_length=50)  # Цвет варианта
    international_shipment = models.BooleanField()  # Международная доставка (да/нет)
    unique_key = models.CharField(max_length=255)  # Уникальный ключ
    size = models.CharField(max_length=20)   # Размер в американской системе
    width = models.CharField(max_length=20)  # Ширина (встречается в обуви и одежде)
