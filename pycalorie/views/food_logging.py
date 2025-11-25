"""
Food Logging views - Manual food entry, editing, and deletion.
Users can create food entries without needing pre-existing Food database records.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.http import require_POST
from datetime import datetime

from ..models import Food, Meal, FoodEntry, DailyLog


@login_required
def food_log(request):
    """
    Manual food logging - user directly enters food details.
    No pre-existing Food database entry required.
    """
    if request.method == 'POST':
        try:
            # Get form data
            food_name = request.POST.get('food_name')
            quantity = float(request.POST.get('quantity'))
            meal_id = request.POST.get('meal_id')
            date_str = request.POST.get('date')
            time_str = request.POST.get('time')
            notes = request.POST.get('notes', '')
            
            # Nutritional data (user can enter or leave blank)
            calories = float(request.POST.get('calories', 0))
            protein = float(request.POST.get('protein', 0))
            carbs = float(request.POST.get('carbs', 0))
            fat = float(request.POST.get('fat', 0))
            
            # Parse date and time
            entry_date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else timezone.now().date()
            entry_time = datetime.strptime(time_str, '%H:%M').time() if time_str else timezone.now().time()
            
            # Get meal if provided
            meal = Meal.objects.get(id=meal_id) if meal_id else None
            
            # Create food entry directly without Food FK
            FoodEntry.objects.create(
                user=request.user,
                food_name=food_name,
                quantity=quantity,
                calories=calories,
                protein=protein,
                carbs=carbs,
                fat=fat,
                meal=meal,
                date=entry_date,
                time=entry_time,
                notes=notes,
                is_ai_generated=False,
            )
            
            messages.success(request, f'Successfully logged {food_name}!')
            return redirect('dashboard:index')
            
        except Exception as e:
            messages.error(request, f'Error logging food: {str(e)}')
    
    # GET request - show form
    meals = Meal.objects.all()
    
    context = {
        'meals': meals,
        'today': timezone.now().date(),
        'now': timezone.now().time(),
    }
    
    return render(request, 'dashboard/food_log.html', context)


@login_required
def search_food(request):
    """
    AJAX endpoint to search for foods in database.
    Returns suggestions to help users with nutritional data.
    """
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'foods': []})
    
    foods = Food.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query),
        is_verified=True
    ).order_by('name')[:20]
    
    results = [{
        'id': food.id,
        'name': food.name,
        'calories_per_100g': food.calories_per_100g,
        'protein_per_100g': food.protein_per_100g,
        'carbs_per_100g': food.carbs_per_100g,
        'fat_per_100g': food.fat_per_100g,
        'serving_size': food.serving_size,
    } for food in foods]
    
    return JsonResponse({'foods': results})


@login_required
def edit_food_entry(request, entry_id):
    """Edit an existing food entry."""
    entry = get_object_or_404(FoodEntry, id=entry_id, user=request.user)
    
    if request.method == 'POST':
        try:
            entry.food_name = request.POST.get('food_name')
            entry.quantity = float(request.POST.get('quantity'))
            entry.calories = float(request.POST.get('calories', 0))
            entry.protein = float(request.POST.get('protein', 0))
            entry.carbs = float(request.POST.get('carbs', 0))
            entry.fat = float(request.POST.get('fat', 0))
            entry.meal_id = request.POST.get('meal_id')
            entry.notes = request.POST.get('notes', '')
            entry.save()
            
            messages.success(request, 'Food entry updated successfully!')
            return redirect('dashboard:index')
            
        except Exception as e:
            messages.error(request, f'Error updating entry: {str(e)}')
    
    meals = Meal.objects.all()
    context = {'entry': entry, 'meals': meals}
    return render(request, 'dashboard/edit_food_entry.html', context)


@login_required
@require_POST
def delete_food_entry(request, entry_id):
    """Delete a food entry."""
    entry = get_object_or_404(FoodEntry, id=entry_id, user=request.user)
    entry.delete()
    
    messages.success(request, 'Food entry deleted successfully!')
    return redirect('dashboard:index')


@login_required
def food_log_history(request):
    """View historical food log entries."""
    from datetime import timedelta
    
    # Get date range from query params
    days = int(request.GET.get('days', 7))
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=days)
    
    entries = FoodEntry.objects.filter(
        user=request.user,
        date__gte=start_date,
        date__lte=end_date
    ).select_related('meal').order_by('-date', '-time')
    
    context = {
        'entries': entries,
        'start_date': start_date,
        'end_date': end_date,
        'days': days,
    }
    
    return render(request, 'dashboard/food_log_history.html', context)


@login_required
@require_POST
def add_water(request):
    """Add water intake (250ml increment)."""
    today = timezone.now().date()
    daily_log, _ = DailyLog.objects.get_or_create(
        user=request.user,
        date=today
    )
    
    # Add 250ml (0.25 liters)
    daily_log.total_water_liters += 0.25
    daily_log.save()
    
    profile = request.user.profile
    
    return JsonResponse({
        'success': True,
        'total_water': daily_log.total_water_liters * 1000,  # ml
        'goal': profile.water_goal_liters * 1000,  # ml
    })


@login_required
def create_food(request):
    """
    Create a new custom food item in the database.
    This is for creating reusable food items.
    """
    if request.method == 'POST':
        try:
            food = Food.objects.create(
                name=request.POST.get('name'),
                description=request.POST.get('description', ''),
                calories_per_100g=float(request.POST.get('calories_per_100g')),
                protein_per_100g=float(request.POST.get('protein_per_100g', 0)),
                carbs_per_100g=float(request.POST.get('carbs_per_100g', 0)),
                fat_per_100g=float(request.POST.get('fat_per_100g', 0)),
                serving_size=request.POST.get('serving_size', '100g'),
                is_verified=False,
                created_by=request.user,
            )
            
            messages.success(request, f'Created {food.name}! It will be verified by admins.')
            return redirect('pycalorie:food_log')
            
        except Exception as e:
            messages.error(request, f'Error creating food: {str(e)}')
    
    return render(request, 'dashboard/create_food.html')
