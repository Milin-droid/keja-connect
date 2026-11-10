from django.core.management.base import BaseCommand, CommandError
from django.db import connection


class Command(BaseCommand):
    help = 'Create the isolated KejaConnect PostgreSQL schema if needed'

    def handle(self, *args, **options):
        if connection.vendor != 'postgresql':
            raise CommandError('KejaConnect schema setup requires PostgreSQL.')

        with connection.cursor() as cursor:
            cursor.execute('CREATE SCHEMA IF NOT EXISTS keja_connect')

        self.stdout.write(self.style.SUCCESS('KejaConnect database schema is ready.'))
