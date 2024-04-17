import json
from django.core.management.base import BaseCommand
from apps.models import Product, Variant

class Command(BaseCommand):
    help = 'Import data from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file')

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']
        with open(json_file, 'r') as f:
            data = json.load(f)

        for item in data:
            product, created = Product.objects.get_or_create(url=item['url'])
            for variant_data in item['variants']:
                Variant.objects.create(
                    product=product,
                    price=variant_data['price'],
                    name=variant_data['name'],
                    item_detail=variant_data['item_detail'],
                    color=variant_data['color'],
                    international_shipment=variant_data['international_shipment'],
                    unique_key=variant_data['unique_key'],
                    size=variant_data['size'],
                    width=variant_data['width']
                )
