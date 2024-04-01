import json
from datetime import datetime
from apps.models import (Product, Variant)

def import_data_from_json(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    for item in data:
        # Создаем или получаем объект Product по URL-адресу
        product, created = Product.objects.get_or_create(url=item['url'])

        # Итерируем по вариантам и создаем объекты Variant
        for variant_data in item['variants']:
            Variant.objects.create(
                product=product,
                price=variant_data['price'],
                name=variant_data['name'],
                item_detail=variant_data['item_detail'],
                color=variant_data['color'],
                international_shipment=variant_data['international_shipment'],
                unique_key=variant_data['unique_key'],
                created_at=datetime.fromisoformat(variant_data['created_at']),
                updated_at=datetime.fromisoformat(variant_data['updated_at']),
                size=variant_data['size'],
                width=variant_data['width']
            )

if __name__ == "__main__":
    json_file_path = "path/to/your/json/file.json"
    import_data_from_json(json_file_path)