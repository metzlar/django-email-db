from django_email_db.backend import MessageFilters

from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('Found E-mail filters:\n')
        for f in MessageFilters().filters:
            self.stdout.write(str(f)+'\n')