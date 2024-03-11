from django.core.management.base import BaseCommand
from app.models import Size  # Импортируйте модель Size

class Command(BaseCommand):
    help = 'Updates the availability of all sizes to "In Stock".'

    def handle(self, *args, **options):
        updated_count = Size.objects.all().update(stock="In Stock")
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {updated_count} sizes to "In Stock".'))
