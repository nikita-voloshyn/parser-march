# app/management/commands/import_from_oxy.py
import json
from django.core.management.base import BaseCommand
from app.models import Product, Category, Image  # Импортируйте модели

class Command(BaseCommand):
    help = 'Imports product data from a specified JSON file into the database'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the JSON file containing product data')

    def handle(self, *args, **options):
        file_path = options['file_path']

        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File "{file_path}" does not exist'))
            return

        for item in data:
            for product_data in item['results']:
                content = product_data['content']
                self.import_product(content)


    def import_product(self, data):
        # Создание или обновление категорий
        categories = [Category.objects.get_or_create(title=cat['title'])[0] for cat in data['categories']]

        # Создание или обновление продукта
        product, created = Product.objects.update_or_create(
            product_id=data['product_id'],
            defaults={
                'url': data['url'],
                'title': data['title'],
                'price': data['price'],
                'old_price': data.get('old_price', None),
                'currency': data['currency'],
                'customized': data['customized'],
                'variation_count': data['variation_count'],
                'shipping_from': data['shipping']['from'],
                'seller_best_seller': data['seller']['best_seller'],
                'seller_star_seller': data['seller']['star_seller'],
                'seller_reviews_count': data['seller']['reviews_count'],
            }
        )

        # Связывание продукта с категориями
        product.categories.set(categories)

        # Обработка и сохранение изображений продукта
        # Удаляем существующие изображения, чтобы избежать дубликатов
        product.product_images.all().delete()
        for img_url in data['images']:
            Image.objects.create(product=product, image_url=img_url)

        self.stdout.write(self.style.SUCCESS(f'Successfully imported product "{product.title}"'))
