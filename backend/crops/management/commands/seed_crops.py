from django.core.management.base import BaseCommand
from crops.models import Crop

class Command(BaseCommand):
    help = 'Seed the database with sample crop data'

    def handle(self, *args, **options):
        crops = [
            {
                'name': 'Maize',
                'scientific_name': 'Zea mays',
                'planting_season': 'Rainy',
                'growth_period_days': 90,
                'optimal_temp_min': 18,
                'optimal_temp_max': 30,
                'optimal_rainfall_min': 500,
                'optimal_rainfall_max': 1200,
                'soil_type': 'Loamy',
            },
            {
                'name': 'Wheat',
                'scientific_name': 'Triticum aestivum',
                'planting_season': 'Winter',
                'growth_period_days': 120,
                'optimal_temp_min': 10,
                'optimal_temp_max': 25,
                'optimal_rainfall_min': 300,
                'optimal_rainfall_max': 800,
                'soil_type': 'Clay',
            },
            {
                'name': 'Rice',
                'scientific_name': 'Oryza sativa',
                'planting_season': 'Rainy',
                'growth_period_days': 150,
                'optimal_temp_min': 20,
                'optimal_temp_max': 35,
                'optimal_rainfall_min': 800,
                'optimal_rainfall_max': 2000,
                'soil_type': 'Silty',
            },
            {
                'name': 'Soybeans',
                'scientific_name': 'Glycine max',
                'planting_season': 'Summer',
                'growth_period_days': 100,
                'optimal_temp_min': 15,
                'optimal_temp_max': 30,
                'optimal_rainfall_min': 400,
                'optimal_rainfall_max': 1200,
                'soil_type': 'Loamy',
            },
        ]

        for crop_data in crops:
            crop, created = Crop.objects.get_or_create(
                name=crop_data['name'],
                defaults=crop_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added crop: {crop.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Crop already exists: {crop.name}"))

        self.stdout.write(self.style.SUCCESS('Successfully seeded crops.'))