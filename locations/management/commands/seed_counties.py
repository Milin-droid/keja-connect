
from django.core.management.base import BaseCommand
from locations.models import County


class Command(BaseCommand):
    help = 'Populate the database with Kenya’s 47 counties'

    def handle(self, *args, **kwargs):
        counties = [
            'Mombasa',
            'Kwale',
            'Kilifi',
            'Tana River',
            'Lamu',
            'Taita-Taveta',
            'Garissa',
            'Wajir',
            'Mandera',
            'Marsabit',
            'Isiolo',
            'Meru',
            'Tharaka-Nithi',
            'Embu',
            'Kitui',
            'Machakos',
            'Makueni',
            'Nyandarua',
            'Nyeri',
            'Kirinyaga',
            'Murang’a',
            'Kiambu',
            'Turkana',
            'West Pokot',
            'Samburu',
            'Trans Nzoia',
            'Uasin Gishu',
            'Elgeyo-Marakwet',
            'Nandi',
            'Baringo',
            'Laikipia',
            'Nakuru',
            'Narok',
            'Kajiado',
            'Kericho',
            'Bomet',
            'Kakamega',
            'Vihiga',
            'Bungoma',
            'Busia',
            'Siaya',
            'Kisumu',
            'Homa Bay',
            'Migori',
            'Kisii',
            'Nyamira',
            'Nairobi',
        ]

        created_count = 0

        for county_name in counties:
            county, created = County.objects.get_or_create(
                name=county_name
            )

            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Success! Added {created_count} new counties. '
                f'Total counties: {County.objects.count()}'
            )
        )
