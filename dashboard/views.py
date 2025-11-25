from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum, Q
from django.contrib import messages
from django.http import JsonResponse
import json
from datetime import datetime, timedelta
from pycalorie.models import (
    FoodEntry, DailyLog, Food, Meal, CaloriePrediction
)
from accounts.models import UserProfile


@login_required
def dashboard(request):
    """Main dashboard view showing user's calorie tracking overview."""
    today = timezone.now().date()
    user = request.user
    
    # Get or create user profile
    profile, _ = UserProfile.objects.get_or_create(user=user)
    
    # Get today's food entries
    today_entries = FoodEntry.objects.filter(user=user, date=today)
    
    # Calculate today's totals
    today_totals = today_entries.aggregate(
        total_calories=Sum('food__calories_per_100g') * Sum('quantity') / 100,
        total_protein=Sum('food__protein_per_100g') * Sum('quantity') / 100,
        total_carbs=Sum('food__carbs_per_100g') * Sum('quantity') / 100,
        total_fat=Sum('food__fat_per_100g') * Sum('quantity') / 100,
    )
    
    # Calculate totals manually for accuracy
    total_calories = sum(entry.total_calories for entry in today_entries)
    total_protein = sum(entry.total_protein for entry in today_entries)
    total_carbs = sum(entry.total_carbs for entry in today_entries)
    total_fat = sum(entry.total_fat for entry in today_entries)
    
    # Get or create today's daily log
    daily_log, _ = DailyLog.objects.get_or_create(
        user=user,
        date=today,
        defaults={
            'total_calories': total_calories,
            'total_protein': total_protein,
            'total_carbs': total_carbs,
            'total_fat': total_fat,
            'calorie_goal': profile.daily_calorie_goal,
        }
    )
    
    # Update daily log with current totals
    daily_log.total_calories = total_calories
    daily_log.total_protein = total_protein
    daily_log.total_carbs = total_carbs
    daily_log.total_fat = total_fat
    daily_log.calorie_goal = profile.daily_calorie_goal
    daily_log.save()
    
    # Get recent entries (last 7 days)
    week_ago = today - timedelta(days=7)
    recent_entries = FoodEntry.objects.filter(
        user=user,
        date__gte=week_ago
    ).order_by('-date', '-time')[:10]
    
    # Get weekly calorie data for chart
    weekly_data = []
    for i in range(7):
        date = today - timedelta(days=i)
        entries = FoodEntry.objects.filter(user=user, date=date)
        day_calories = sum(entry.total_calories for entry in entries)
        weekly_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'calories': round(day_calories, 1),
            'goal': profile.daily_calorie_goal or 0,
        })
    weekly_data.reverse()
    weekly_data_json = json.dumps(weekly_data)
    
    # Get meals for today grouped by meal type
    meals_today = {}
    for meal in Meal.objects.all():
        meal_entries = today_entries.filter(meal=meal)
        if meal_entries.exists():
            meals_today[meal.name] = {
                'entries': meal_entries,
                'total_calories': sum(e.total_calories for e in meal_entries),
            }
    
    context = {
        'user': user,
        'profile': profile,
        'daily_log': daily_log,
        'today_entries': today_entries,
        'recent_entries': recent_entries,
        'weekly_data': weekly_data_json,
        'meals_today': meals_today,
        'total_calories': total_calories,
        'total_protein': total_protein,
        'total_carbs': total_carbs,
        'total_fat': total_fat,
        'calorie_goal': profile.daily_calorie_goal or 2000,
        'calorie_remaining': (profile.daily_calorie_goal or 2000) - total_calories,
        'calorie_percentage': min(100, (total_calories / (profile.daily_calorie_goal or 2000)) * 100),
    }
    
    return render(request, 'dashboard/index.html', context)


@login_required
def food_log(request):
    """View for logging food entries - supports direct entry without Food FK."""
    meals = Meal.objects.all()
    # Get verified foods for suggestions (optional)
    foods = Food.objects.filter(is_verified=True).order_by('name')[:100]
    
    if request.method == 'POST':
        try:
            # Get form data
            food_name = request.POST.get('food_name')
            meal_id = request.POST.get('meal_id')
            quantity = request.POST.get('quantity')
            date = request.POST.get('date')
            time = request.POST.get('time')
            notes = request.POST.get('notes', '')
            
            # Optional nutritional data
            calories = float(request.POST.get('calories', 0))
            protein = float(request.POST.get('protein', 0))
            carbs = float(request.POST.get('carbs', 0))
            fat = float(request.POST.get('fat', 0))
            
            # Get meal if provided
            meal = Meal.objects.get(id=meal_id) if meal_id else None
            
            # Check if user selected from database (optional)
            food_id = request.POST.get('food_id')
            food = None
            if food_id:
                food = Food.objects.get(id=food_id)
            
            # Create food entry (direct entry mode)
            FoodEntry.objects.create(
                user=request.user,
                food=food,  # Optional FK
                food_name=food_name or (food.name if food else 'Unknown'),
                meal=meal,
                quantity=float(quantity),
                calories=calories,
                protein=protein,
                carbs=carbs,
                fat=fat,
                date=datetime.strptime(date, '%Y-%m-%d').date() if date else timezone.now().date(),
                time=datetime.strptime(time, '%H:%M').time() if time else timezone.now().time(),
                notes=notes,
                is_ai_generated=False,
            )
            
            messages.success(request, f'Successfully logged {food_name or food.name}!')
            return redirect('dashboard:food_log')
        except Exception as e:
            messages.error(request, f'Error logging food: {str(e)}')
    
    # Get today's entries
    today = timezone.now().date()
    now_time = timezone.now()
    today_entries = FoodEntry.objects.filter(user=request.user, date=today).order_by('-time')
    
    context = {
        'meals': meals,
        'foods': foods,
        'today_entries': today_entries,
        'today': today,
        'now': now_time,
    }
    
    return render(request, 'dashboard/food_log.html', context)


@login_required
def calorie_predict(request):
    """View for AI-powered calorie prediction."""
    if request.method == 'POST':
        food_description = request.POST.get('food_description', '').strip()
        
        if not food_description:
            messages.error(request, 'Please provide a food description.')
            return redirect('dashboard:calorie_predict')
        
        # Import the AI service
        from pycalorie.services.ai_service import predict_calories
        
        try:
            prediction = predict_calories(request.user, food_description)
            
            if prediction:
                messages.success(request, f'Prediction generated for: {prediction.predicted_food_name}')
                return redirect('dashboard:calorie_predict_result', prediction_id=prediction.id)
            else:
                messages.error(request, 'Unable to generate prediction. Please try again.')
        except Exception as e:
            messages.error(request, f'Error generating prediction: {str(e)}')
    
    # Get recent predictions
    recent_predictions = CaloriePrediction.objects.filter(
        user=request.user
    ).order_by('-created_at')[:10]
    
    context = {
        'recent_predictions': recent_predictions,
    }
    
    return render(request, 'dashboard/calorie_predict.html', context)


@login_required
def calorie_predict_result(request, prediction_id):
    """View to display prediction result and allow saving as food entry."""
    try:
        prediction = CaloriePrediction.objects.get(id=prediction_id, user=request.user)
    except CaloriePrediction.DoesNotExist:
        messages.error(request, 'Prediction not found.')
        return redirect('dashboard:calorie_predict')
    
    meals = Meal.objects.all()
    
    if request.method == 'POST':
        meal_id = request.POST.get('meal_id')
        quantity = request.POST.get('quantity', prediction.predicted_quantity)
        date = request.POST.get('date')
        time = request.POST.get('time')
        
        try:
            # Create food entry from prediction (direct entry mode)
            meal = Meal.objects.get(id=meal_id) if meal_id else None
            
            # Calculate nutrition based on quantity
            quantity_float = float(quantity)
            quantity_ratio = quantity_float / prediction.predicted_quantity if prediction.predicted_quantity > 0 else 1
            
            FoodEntry.objects.create(
                user=request.user,
                food_name=prediction.predicted_food_name,
                meal=meal,
                quantity=quantity_float,
                calories=prediction.predicted_calories * quantity_ratio,
                protein=prediction.predicted_protein * quantity_ratio,
                carbs=prediction.predicted_carbs * quantity_ratio,
                fat=prediction.predicted_fat * quantity_ratio,
                date=datetime.strptime(date, '%Y-%m-%d').date() if date else timezone.now().date(),
                time=datetime.strptime(time, '%H:%M').time() if time else timezone.now().time(),
                notes=f'AI Prediction: {prediction.food_description}',
                is_ai_generated=True,
            )
            
            # Mark prediction as saved
            prediction.was_saved_to_log = True
            prediction.save()
            
            messages.success(request, f'Successfully added {prediction.predicted_food_name} to your food log!')
            return redirect('dashboard:index')
        except Exception as e:
            messages.error(request, f'Error saving food entry: {str(e)}')
    
    today = timezone.now().date()
    now_time = timezone.now()
    
    context = {
        'prediction': prediction,
        'meals': meals,
        'today': today,
        'now': now_time,
    }
    
    return render(request, 'dashboard/calorie_predict_result.html', context)


@login_required
def reports(request):
    """View for nutrition reports and analytics."""
    user = request.user
    
    # Get date range (default: last 30 days)
    days = int(request.GET.get('days', 30))
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=days)
    
    # Get daily logs in range
    daily_logs = DailyLog.objects.filter(
        user=user,
        date__gte=start_date,
        date__lte=end_date
    ).order_by('date')
    
    # Calculate averages
    if daily_logs.exists():
        avg_calories = sum(log.total_calories for log in daily_logs) / len(daily_logs)
        avg_protein = sum(log.total_protein for log in daily_logs) / len(daily_logs)
        avg_carbs = sum(log.total_carbs for log in daily_logs) / len(daily_logs)
        avg_fat = sum(log.total_fat for log in daily_logs) / len(daily_logs)
    else:
        avg_calories = avg_protein = avg_carbs = avg_fat = 0
    
    context = {
        'daily_logs': daily_logs,
        'start_date': start_date,
        'end_date': end_date,
        'days': days,
        'avg_calories': avg_calories,
        'avg_protein': avg_protein,
        'avg_carbs': avg_carbs,
        'avg_fat': avg_fat,
    }
    
    return render(request, 'dashboard/reports.html', context)


@login_required
def profile(request):
    """User profile view within dashboard."""
    user = request.user
    
    # Get or create user profile
    profile, _ = UserProfile.objects.get_or_create(user=user)
    
    # Get some statistics
    total_entries = FoodEntry.objects.filter(user=user).count()
    today = timezone.now().date()
    today_entries = FoodEntry.objects.filter(user=user, date=today).count()
    
    # Get recent activity (last 7 days)
    week_ago = today - timedelta(days=7)
    recent_entries_count = FoodEntry.objects.filter(
        user=user,
        date__gte=week_ago
    ).count()
    
    context = {
        'user': user,
        'profile': profile,
        'total_entries': total_entries,
        'today_entries': today_entries,
        'recent_entries_count': recent_entries_count,
    }
    
    return render(request, 'dashboard/profile.html', context)
