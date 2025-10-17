from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
from django.conf import settings

# =========================FOODITEMMODEL===========================================
class FoodItem(models.Model):
    name = models.CharField(max_length=100)
   
    calories_per_100g = models.FloatField()
    protein_per_100g = models.FloatField(default=0)
    carbs_per_100g = models.FloatField(default=0)
    fat_per_100g = models.FloatField(default=0)
    category = models.CharField(max_length=50, blank=True, null=True)
  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ===================================================================================

# =========================USERMEAL===========================================
class UserMeal(models.Model):
  
    MEAL_TYPE_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ]

   
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    
    quantity_grams = models.FloatField()
    meal_name = models.CharField(mmax_length=120)
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPE_CHOICES)
    meal_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s {self.food_item.name} on {self.meal_date}"
# ===================================================================================


# =========================USERPROFILE===========================================
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    height_cm = models.FloatField(blank=True, null=True)
    weight_kg = models.FloatField(blank=True, null=True)
    activity_level = models.CharField(max_length=20, blank=True, null=True)
    goal = models.CharField(max_length=50, blank=True, null=True)
    daily_calorie_target = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
   
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

# ===================================================================================


# =========================FOODITEMMODEL===========================================
# ================================================================================