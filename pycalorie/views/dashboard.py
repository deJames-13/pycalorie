"""
Dashboard view - Main calorie tracking overview.
Shows today's progress, macros, quick actions, and weekly chart.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
import json

from ..models import FoodEntry, DailyLog, Meal
from accounts.models import UserProfile
from ..services.calculator_service import calculate_nutrition_percentage, calculate_macros


@login_required
def dashboard(request):
    """
    Main dashboard view showing today's calorie progress.
    Features: Circular progress, macro cards, quick actions, food log.
    """
    user = request.user
    today = timezone.now().date()
    
    # Get or create user profile
    profile, _ = UserProfile.objects.get_or_create(user=user)
    
    # Check if onboarding is complete
    if not profile.is_onboarding_complete:
        messages.info(request, 'Please complete your profile setup to get started!')
        return redirect('accounts:onboarding')
    
    # Get or create today's daily log
    daily_log, _ = DailyLog.objects.get_or_create(
        user=user,
        date=today,
        defaults={'calorie_goal': profile.daily_calorie_goal}
    )
    
    # Update daily log totals
    daily_log.update_totals()
    
    # Get today's food entries
    today_entries = FoodEntry.objects.filter(
        user=user, 
        date=today
    ).select_related('meal').order_by('time')
    
    # Calculate totals for today
    total_calories = sum(entry.total_calories for entry in today_entries)
    total_protein = sum(entry.total_protein for entry in today_entries)
    total_carbs = sum(entry.total_carbs for entry in today_entries)
    total_fat = sum(entry.total_fat for entry in today_entries)
    
    # Debug output
    print(f"DEBUG - Total calories: {total_calories}")
    print(f"DEBUG - Profile daily_calorie_goal: {profile.daily_calorie_goal}")
    
    # Calculate percentages
    calorie_goal = profile.daily_calorie_goal or 2000
    print(f"DEBUG - Calorie goal: {calorie_goal}")
    
    calorie_percentage = calculate_nutrition_percentage(total_calories, calorie_goal)
    print(f"DEBUG - Calorie percentage: {calorie_percentage}")
    
    calorie_remaining = calorie_goal - total_calories
    
    # Calculate macro goals and percentages
    macro_goals = calculate_macros(calorie_goal)
    protein_percentage = calculate_nutrition_percentage(total_protein, macro_goals['protein_g'])
    carbs_percentage = calculate_nutrition_percentage(total_carbs, macro_goals['carbs_g'])
    fat_percentage = calculate_nutrition_percentage(total_fat, macro_goals['fat_g'])
    
    # Weekly calorie data for chart (last 7 days)
    weekly_data = []
    for i in range(7):
        date = today - timedelta(days=6-i)
        try:
            log = DailyLog.objects.get(user=user, date=date)
            calories = log.total_calories
        except DailyLog.DoesNotExist:
            calories = 0
        
        weekly_data.append({
            'date': date.isoformat(),
            'calories': round(calories, 1),
            'goal': calorie_goal,
        })
    
    # Water tracking
    water_consumed = daily_log.total_water_liters * 1000  # Convert to ml
    water_goal = profile.water_goal_liters * 1000  # Convert to ml
    water_percentage = calculate_nutrition_percentage(water_consumed, water_goal)
    
    context = {
        'profile': profile,
        'daily_log': daily_log,
        'today': today,
        'today_entries': today_entries,
        'total_calories': round(total_calories, 0),
        'total_protein': round(total_protein, 1),
        'total_carbs': round(total_carbs, 1),
        'total_fat': round(total_fat, 1),
        'calorie_goal': calorie_goal,
        'calorie_percentage': min(calorie_percentage, 100),
        'calorie_remaining': round(calorie_remaining, 0),
        'protein_percentage': min(protein_percentage, 100),
        'carbs_percentage': min(carbs_percentage, 100),
        'fat_percentage': min(fat_percentage, 100),
        'weekly_data': json.dumps(weekly_data),
        'water_consumed': round(water_consumed, 0),
        'water_goal': round(water_goal, 0),
        'water_percentage': min(water_percentage, 100),
    }
    
    # Debug context
    print(f"DEBUG - Context calorie_percentage: {context['calorie_percentage']}")
    print(f"DEBUG - Context total_calories: {context['total_calories']}")
    print(f"DEBUG - Context calorie_goal: {context['calorie_goal']}")
    
    return render(request, 'dashboard/index.html', context)
