"""
AI Prediction views - Text and Image-based calorie prediction.
Handles AI-powered food analysis and creates food entries automatically.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from ..models import Meal, FoodEntry, CaloriePrediction, FoodImage


@login_required
def predict_from_text(request):
    """AI calorie prediction from text description."""
    if request.method == 'POST':
        food_description = request.POST.get('food_description', '').strip()
        
        if not food_description:
            messages.error(request, 'Please provide a food description.')
            return redirect('pycalorie:predict_from_text')
        
        from ..services.ai_service import predict_calories
        
        try:
            prediction = predict_calories(request.user, food_description)
            
            if prediction:
                return redirect('pycalorie:prediction_result', prediction_id=prediction.id)
            else:
                messages.error(request, 'Unable to generate prediction. Please try again.')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    recent_predictions = CaloriePrediction.objects.filter(
        user=request.user
    ).order_by('-created_at')[:10]
    
    context = {'recent_predictions': recent_predictions}
    return render(request, 'dashboard/calorie_predict.html', context)


@login_required
def predict_from_image(request):
    """
    AI calorie prediction from food image.
    Analyzes image, detects food items, estimates portions, and meal type.
    """
    if request.method == 'POST' and request.FILES.get('food_image'):
        image = request.FILES['food_image']
        
        from ..services.ai_service import analyze_food_image
        
        try:
            # Analyze image and create prediction + food entry
            result = analyze_food_image(image, request.user)
            
            if result and result.get('food_entry'):
                messages.success(request, f"Successfully logged {result['food_entry'].food_name}!")
                return redirect('pycalorie:image_gallery')
            elif result and result.get('prediction'):
                return redirect('pycalorie:prediction_result', prediction_id=result['prediction'].id)
            else:
                messages.error(request, 'Unable to analyze image. Please try again.')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    return render(request, 'dashboard/predict_image.html')


@login_required
def prediction_result(request, prediction_id):
    """Display AI prediction result with option to save to log."""
    prediction = get_object_or_404(CaloriePrediction, id=prediction_id, user=request.user)
    
    meals = Meal.objects.all()
    context = {
        'prediction': prediction,
        'meals': meals,
        'today': timezone.now().date(),
        'now': timezone.now().time(),
    }
    
    return render(request, 'dashboard/calorie_predict_result.html', context)


@login_required
def save_prediction_to_log(request, prediction_id):
    """
    Save AI prediction as a food entry.
    User can adjust meal type and quantity before saving.
    """
    prediction = get_object_or_404(CaloriePrediction, id=prediction_id, user=request.user)
    
    if request.method == 'POST':
        try:
            meal_id = request.POST.get('meal_id')
            quantity = float(request.POST.get('quantity', prediction.predicted_quantity))
            
            # Calculate nutrition based on quantity adjustment
            quantity_ratio = quantity / prediction.predicted_quantity
            
            # Create food entry directly
            food_entry = FoodEntry.objects.create(
                user=request.user,
                food_name=prediction.predicted_food_name,
                quantity=quantity,
                calories=prediction.predicted_calories * quantity_ratio,
                protein=prediction.predicted_protein * quantity_ratio,
                carbs=prediction.predicted_carbs * quantity_ratio,
                fat=prediction.predicted_fat * quantity_ratio,
                meal_id=meal_id if meal_id else None,
                is_ai_generated=True,
                notes=f'AI Prediction: {prediction.food_description}',
            )
            
            # Link prediction to entry
            prediction.was_saved_to_log = True
            prediction.save()
            
            messages.success(request, f'Added {food_entry.food_name} to your log!')
            return redirect('dashboard:index')
            
        except Exception as e:
            messages.error(request, f'Error saving entry: {str(e)}')
    
    return redirect('pycalorie:prediction_result', prediction_id=prediction_id)


@login_required
def image_gallery(request):
    """
    Instagram-style grid view of all uploaded food images.
    Shows food images with date, meal type, and calories overlay.
    """
    # Get all food images for the user, ordered by date
    food_images = FoodImage.objects.filter(
        food_entry__user=request.user
    ).select_related('food_entry', 'food_entry__meal').order_by('-food_entry__date', '-food_entry__time')
    
    # Filter by date range if provided
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if start_date:
        from datetime import datetime
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        food_images = food_images.filter(food_entry__date__gte=start)
    
    if end_date:
        from datetime import datetime
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
        food_images = food_images.filter(food_entry__date__lte=end)
    
    # Filter by meal type if provided
    meal_type = request.GET.get('meal_type')
    if meal_type:
        food_images = food_images.filter(food_entry__meal__name=meal_type)
    
    meals = Meal.objects.all()
    
    context = {
        'food_images': food_images,
        'meals': meals,
        'selected_meal': meal_type,
    }
    
    return render(request, 'dashboard/image_gallery.html', context)


@login_required
def image_detail(request, image_id):
    """
    Detailed view of a single food image.
    Shows full image, nutrition breakdown, and edit options.
    """
    food_image = get_object_or_404(
        FoodImage, 
        id=image_id, 
        food_entry__user=request.user
    )
    
    context = {
        'food_image': food_image,
        'food_entry': food_image.food_entry,
    }
    
    return render(request, 'dashboard/image_detail.html', context)
