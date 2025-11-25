"""
Management command to initialize default data for PyCalorie app.
Run with: python manage.py init_data
"""
from django.core.management.base import BaseCommand
from pycalorie.models import Meal, Food


class Command(BaseCommand):
    help = 'Initialize default meals and sample foods'

    def handle(self, *args, **options):
        self.stdout.write('Initializing default data...')
        
        # Create default meals
        meals_data = [
            {'name': 'Breakfast', 'order': 1, 'description': 'Morning meal'},
            {'name': 'Lunch', 'order': 2, 'description': 'Midday meal'},
            {'name': 'Dinner', 'order': 3, 'description': 'Evening meal'},
            {'name': 'Snack', 'order': 4, 'description': 'Between meals'},
        ]
        
        for meal_data in meals_data:
            meal, created = Meal.objects.get_or_create(
                name=meal_data['name'],
                defaults=meal_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created meal: {meal.name}'))
            else:
                self.stdout.write(f'Meal already exists: {meal.name}')
        
        # Create sample foods
        foods_data = [
            {
                'name': 'Apple',
                'calories_per_100g': 52,
                'protein_per_100g': 0.3,
                'carbs_per_100g': 14,
                'fat_per_100g': 0.2,
                'fiber_per_100g': 2.4,
                'is_verified': True,
            },
            {
                'name': 'Banana',
                'calories_per_100g': 89,
                'protein_per_100g': 1.1,
                'carbs_per_100g': 23,
                'fat_per_100g': 0.3,
                'fiber_per_100g': 2.6,
                'is_verified': True,
            },
            {
                'name': 'Chicken Breast (Grilled)',
                'calories_per_100g': 165,
                'protein_per_100g': 31,
                'carbs_per_100g': 0,
                'fat_per_100g': 3.6,
                'fiber_per_100g': 0,
                'is_verified': True,
            },
            {
                'name': 'White Rice (Cooked)',
                'calories_per_100g': 130,
                'protein_per_100g': 2.7,
                'carbs_per_100g': 28,
                'fat_per_100g': 0.3,
                'fiber_per_100g': 0.4,
                'is_verified': True,
            },
            {
                'name': 'Egg (Large)',
                'calories_per_100g': 155,
                'protein_per_100g': 13,
                'carbs_per_100g': 1.1,
                'fat_per_100g': 11,
                'fiber_per_100g': 0,
                'is_verified': True,
            },
            {
                'name': 'Salmon (Grilled)',
                'calories_per_100g': 206,
                'protein_per_100g': 25,
                'carbs_per_100g': 0,
                'fat_per_100g': 12,
                'fiber_per_100g': 0,
                'is_verified': True,
            },
            {
                'name': 'Broccoli (Steamed)',
                'calories_per_100g': 35,
                'protein_per_100g': 2.8,
                'carbs_per_100g': 7,
                'fat_per_100g': 0.4,
                'fiber_per_100g': 2.6,
                'is_verified': True,
            },
            {
                'name': 'Whole Wheat Bread',
                'calories_per_100g': 247,
                'protein_per_100g': 13,
                'carbs_per_100g': 41,
                'fat_per_100g': 4.2,
                'fiber_per_100g': 7,
                'is_verified': True,
            },
        ]
        
        for food_data in foods_data:
            food, created = Food.objects.get_or_create(
                name=food_data['name'],
                defaults=food_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created food: {food.name}'))
            else:
                self.stdout.write(f'Food already exists: {food.name}')
        
        self.stdout.write(self.style.SUCCESS('\nData initialization complete!'))

