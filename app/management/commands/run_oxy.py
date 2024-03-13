# app/management/commands/run_oxy.py
from django.core.management.base import BaseCommand
from app.management.scripts import data_from_link  # Импортируйте ваш модуль oxy

class Command(BaseCommand):
    help = 'Run oxy process'

    def handle(self, *args, **options):
        oxy.fetch_details_from_oxy()
        self.stdout.write(self.style.SUCCESS('Successfully ran oxy process'))
