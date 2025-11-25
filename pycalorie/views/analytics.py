"""
Analytics views - Reports, statistics, and data visualization.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from datetime import timedelta
import json

from ..models import DailyLog, FoodEntry


@login_required
def analytics(request):
    """Analytics and reports page with charts and statistics."""
    days = int(request.GET.get('days', 30))
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=days)
    
    daily_logs = DailyLog.objects.filter(
        user=request.user,
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
    
    # Prepare chart data
    chart_data = [{
        'date': log.date.strftime('%Y-%m-%d'),
        'calories': round(log.total_calories, 1),
        'protein': round(log.total_protein, 1),
        'carbs': round(log.total_carbs, 1),
        'fat': round(log.total_fat, 1),
        'goal': log.calorie_goal or 2000,
    } for log in daily_logs]
    
    context = {
        'daily_logs': daily_logs,
        'start_date': start_date,
        'end_date': end_date,
        'days': days,
        'avg_calories': round(avg_calories, 1),
        'avg_protein': round(avg_protein, 1),
        'avg_carbs': round(avg_carbs, 1),
        'avg_fat': round(avg_fat, 1),
        'chart_data': json.dumps(chart_data),
    }
    
    return render(request, 'dashboard/reports.html', context)


@login_required
def weekly_analytics(request):
    """Weekly analytics data (AJAX)."""
    today = timezone.now().date()
    start_date = today - timedelta(days=7)
    
    logs = DailyLog.objects.filter(
        user=request.user,
        date__gte=start_date,
        date__lte=today
    ).order_by('date')
    
    data = [{
        'date': log.date.strftime('%a'),
        'calories': log.total_calories,
        'protein': log.total_protein,
        'carbs': log.total_carbs,
        'fat': log.total_fat,
    } for log in logs]
    
    return JsonResponse({'data': data})


@login_required
def monthly_analytics(request):
    """Monthly analytics data (AJAX)."""
    today = timezone.now().date()
    start_date = today - timedelta(days=30)
    
    logs = DailyLog.objects.filter(
        user=request.user,
        date__gte=start_date,
        date__lte=today
    ).order_by('date')
    
    data = [{
        'date': log.date.strftime('%m/%d'),
        'calories': log.total_calories,
        'protein': log.total_protein,
        'carbs': log.total_carbs,
        'fat': log.total_fat,
    } for log in logs]
    
    return JsonResponse({'data': data})
