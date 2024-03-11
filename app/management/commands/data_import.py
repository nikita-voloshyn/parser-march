from django.core.management.base import BaseCommand
from app.models import Product, Size
import json

class Command(BaseCommand):
    help = 'Import products from JSON file into the database.'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='The JSON file path to import data from.')

    def handle(self, *args, **options):
        file_path = options['json_file']
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

            for item in data:
                product, created = Product.objects.get_or_create(
                    product_id=item['product_id'],
                    defaults={
                        'name': item['product_name'],
                        'price': item['product_price'],
                        'description': item['product_description'] if item['product_description'] else "",
                    }
                )

                for size_info in item['available_sizes']:
                    Size.objects.create(
                        product=product,
                        valueId=size_info['valueId'],
                        value=size_info['value'],
                        stock=size_info['stock'],
                        shipping=size_info['shipping'],
                        isSameDayShippingWindow=size_info['isSameDayShippingWindow'],
                        quantitySourceType=size_info['quantitySourceType'],
                        href=size_info['href'],
                        selectable=size_info['selectable']
                    )

        self.stdout.write(self.style.SUCCESS(f'Successfully imported products from {file_path}'))
