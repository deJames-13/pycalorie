from django.contrib import admin
from .models import (
    Food, Meal, FoodEntry, DailyLog, CaloriePrediction, FoodImage
)


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ['name', 'calories_per_100g', 'protein_per_100g', 'carbs_per_100g', 'fat_per_100g', 'is_verified', 'created_by']
    list_filter = ['is_verified', 'created_at']
    search_fields = ['name', 'description']
    raw_id_fields = ['created_by']


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'description']
    ordering = ['order', 'name']


@admin.register(FoodEntry)
class FoodEntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'food_name', 'meal', 'quantity', 'date', 'time', 'total_calories', 'is_ai_generated']
    list_filter = ['date', 'meal', 'is_ai_generated', 'created_at']
    search_fields = ['user__username', 'food_name', 'food__name']
    raw_id_fields = ['user', 'food', 'daily_log']
    date_hierarchy = 'date'


@admin.register(FoodImage)
class FoodImageAdmin(admin.ModelAdmin):
    list_display = ['food_entry', 'image', 'ai_confidence', 'created_at']
    list_filter = ['created_at']
    search_fields = ['food_entry__food_name', 'food_entry__user__username']
    raw_id_fields = ['food_entry']
    readonly_fields = ['thumbnail', 'created_at']


@admin.register(DailyLog)
class DailyLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'total_calories', 'calorie_goal', 'calorie_remaining', 'calorie_percentage', 'total_water_liters']
    list_filter = ['date', 'created_at']
    search_fields = ['user__username']
    raw_id_fields = ['user']
    date_hierarchy = 'date'


@admin.register(CaloriePrediction)
class CaloriePredictionAdmin(admin.ModelAdmin):
    list_display = ['user', 'predicted_food_name', 'predicted_calories', 'predicted_quantity', 'confidence_score', 'ai_model_used', 'was_saved_to_log', 'created_at']
    list_filter = ['ai_model_used', 'was_saved_to_log', 'created_at']
    search_fields = ['user__username', 'food_description', 'predicted_food_name']
    raw_id_fields = ['user']
    readonly_fields = ['created_at']
