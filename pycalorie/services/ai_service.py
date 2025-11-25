"""
Google GENAI service for calorie prediction and food analysis.
Uses the new google-genai package (replaces google-generativeai).
"""
import os
import json
import re
from typing import Optional, Dict
from django.conf import settings
from django.utils import timezone
from ..models import CaloriePrediction, User

try:
    from google import genai
    from google.genai import types
    GOOGLE_AI_AVAILABLE = True
except ImportError:
    GOOGLE_AI_AVAILABLE = False
    genai = None
    types = None

PRO_MODEL = "gemini-2.5-pro"
FLASH_MODEL = "gemini-2.5-flash"
MODEL = PRO_MODEL

def get_google_api_key():
    """Get Google API key from environment variables."""
    return os.environ.get('GOOGLE_API_KEY') or os.environ.get('GEMINI_API_KEY') or getattr(settings, 'GOOGLE_API_KEY', None)


def get_genai_client():
    """
    Create and return a Google GenAI client.
    Uses environment variables or settings for API key.
    """
    if not GOOGLE_AI_AVAILABLE:
        raise ImportError(
            "google-genai package is not installed. "
            "Install it with: pip install google-genai"
        )
    
    api_key = get_google_api_key()
    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY or GEMINI_API_KEY not found in environment variables or settings. "
            "Set export GOOGLE_API_KEY='your-api-key' or export GEMINI_API_KEY='your-api-key'"
        )
    
    # Create client with API key
    client = genai.Client(api_key=api_key)
    return client


def predict_calories(user: User, food_description: str) -> Optional[CaloriePrediction]:
    """
    Predict calories and nutritional information for a food description using Google GENAI.
    
    Args:
        user: The user making the prediction request
        food_description: Natural language description of the food (e.g., "a medium apple", "grilled chicken breast")
    
    Returns:
        CaloriePrediction object or None if prediction fails
    """
    if not GOOGLE_AI_AVAILABLE:
        raise ImportError("google-genai package is not installed.")
    
    print("--- Starting Text Calorie Prediction ---")
    
    try:
        # Get client
        client = get_genai_client()
        
        # Create prompt for calorie prediction
        prompt = f"""You are a nutrition expert. Analyze the following food description and provide accurate nutritional information.

Food Description: "{food_description}"

Please provide the nutritional information in the following JSON format (no markdown formatting):
{{
    "food_name": "Standard name of the food",
    "quantity_grams": 100,
    "calories_per_100g": 0.0,
    "protein_per_100g": 0.0,
    "carbs_per_100g": 0.0,
    "fat_per_100g": 0.0,
    "confidence": 0.0
}}

Guidelines:
- If the description includes a quantity (e.g., "medium apple", "1 cup rice"), estimate the weight in grams
- Provide calories per 100g (standard unit)
- Provide macronutrients (protein, carbs, fat) in grams per 100g
- Set confidence between 0.0 and 1.0 based on how specific the description is
- Be as accurate as possible based on standard nutritional databases
- If the food description is unclear, make your best estimate

Return ONLY valid JSON, no additional text or markdown code blocks."""

        print(f"--- Sending text prediction request for: {food_description} ---")
        
        # Generate prediction using new API
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
        )
        
        # Extract JSON from response
        response_text = response.text.strip()
        print(f"--- Raw Response (first 200 chars): {response_text[:200]}... ---")
        
        # Clean JSON response (remove markdown formatting if present)
        if response_text.startswith('```json'):
            print("--- Removing ```json markdown wrapper ---")
            response_text = response_text[7:]
        if response_text.startswith('```'):
            print("--- Removing ``` markdown wrapper ---")
            response_text = response_text[3:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        
        response_text = response_text.strip()
        
        # Try to extract JSON object if AI added extra text
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            response_text = json_match.group(0)
        
        # Parse JSON response
        print("--- Parsing JSON response ---")
        prediction_data = json.loads(response_text)
        
        # Extract values with defaults
        food_name = prediction_data.get('food_name', food_description.title())
        quantity_grams = float(prediction_data.get('quantity_grams', 100))
        calories_per_100g = float(prediction_data.get('calories_per_100g', 0))
        protein_per_100g = float(prediction_data.get('protein_per_100g', 0))
        carbs_per_100g = float(prediction_data.get('carbs_per_100g', 0))
        fat_per_100g = float(prediction_data.get('fat_per_100g', 0))
        confidence = float(prediction_data.get('confidence', 0.5))
        
        # Calculate calories for the predicted quantity
        predicted_calories = (calories_per_100g * quantity_grams) / 100
        predicted_protein = (protein_per_100g * quantity_grams) / 100
        predicted_carbs = (carbs_per_100g * quantity_grams) / 100
        predicted_fat = (fat_per_100g * quantity_grams) / 100
        
        print(f"--- Predicted: {food_name} ({quantity_grams}g, {predicted_calories} cal) ---")
        
        # Create prediction record
        prediction = CaloriePrediction.objects.create(
            user=user,
            food_description=food_description,
            predicted_food_name=food_name,
            predicted_calories=predicted_calories,
            predicted_protein=predicted_protein,
            predicted_carbs=predicted_carbs,
            predicted_fat=predicted_fat,
            predicted_quantity=quantity_grams,
            confidence_score=confidence,
            ai_model_used=MODEL,
        )
        
        print("--- ✓ Text Prediction Complete ---")
        return prediction
        
    except json.JSONDecodeError as e:
        print(f"!!! JSON Parse Error: {e}")
        print(f"!!! Response text: {response_text}")
        return None
    except Exception as e:
        print(f"!!! Error generating prediction: {e}")
        import traceback
        traceback.print_exc()
        return None


def analyze_food_image(image_file, user: User) -> Optional[Dict]:
    """
    Analyze food from an image using Google GENAI vision capabilities.
    Automatically creates FoodEntry and FoodImage, detects meal type.
    Includes image compression using Pillow.
    
    Args:
        image_file: Django UploadedFile object (from request.FILES)
        user: The user making the request
    
    Returns:
        Dict with 'food_entry', 'food_image', and 'prediction' or None if analysis fails
    """
    if not GOOGLE_AI_AVAILABLE:
        raise ImportError("google-generativeai package is not installed.")
    
    print("--- Starting AI Food Image Analysis ---")
    
    try:
        # Import dependencies
        from PIL import Image
        import io
        from django.core.files.base import ContentFile
        from datetime import datetime
        from ..models import CaloriePrediction, FoodEntry, FoodImage, Meal
        
        # Get client
        client = get_genai_client()
        
        # Load and process image
        print(f"--- Loading image: {image_file.name} ---")
        img = Image.open(image_file)
        
        # Convert RGBA/P to RGB (fixes transparency issues)
        if img.mode in ('RGBA', 'P'):
            print(f"--- Converting {img.mode} to RGB ---")
            img = img.convert('RGB')
        
        # Resize if too large (max 1024x1024 for API efficiency)
        max_size = 1024
        if img.width > max_size or img.height > max_size:
            print(f"--- Resizing from {img.width}x{img.height} to fit {max_size}x{max_size} ---")
            img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        
        # Determine meal type based on current time
        current_hour = datetime.now().hour
        if 5 <= current_hour < 11:
            suggested_meal_type = "Breakfast"
        elif 11 <= current_hour < 16:
            suggested_meal_type = "Lunch"
        elif 16 <= current_hour < 21:
            suggested_meal_type = "Dinner"
        else:
            suggested_meal_type = "Snack"
        
        print(f"--- Suggested meal type based on time ({current_hour}:00): {suggested_meal_type} ---")
        
        # Create prompt for food analysis
        prompt = f"""Analyze this food image and provide detailed nutritional information.

Current time suggests this is: {suggested_meal_type}

Please identify:
1. All visible food items
2. Estimated portion sizes (in grams for each item)
3. Total calories and macronutrients for the entire meal
4. Meal type classification (Breakfast, Lunch, Dinner, or Snack)

Return the information in the following JSON format (no markdown formatting):
{{
    "food_name": "Description of the meal (e.g., 'Grilled Chicken Salad with Brown Rice')",
    "meal_type": "Lunch",
    "quantity_grams": 450,
    "total_calories": 520.0,
    "total_protein": 45.0,
    "total_carbs": 55.0,
    "total_fat": 12.0,
    "confidence": 0.85,
    "items": [
        {{
            "item": "Grilled chicken breast",
            "grams": 150,
            "calories": 248
        }},
        {{
            "item": "Mixed salad",
            "grams": 200,
            "calories": 30
        }}
    ]
}}

Important:
- total_calories, total_protein, total_carbs, total_fat should be for the ENTIRE quantity
- quantity_grams is the total weight of all items
- meal_type must be one of: Breakfast, Lunch, Dinner, Snack
- Be as accurate as possible. If uncertain, provide your best estimate and lower the confidence score.
- Return ONLY valid JSON, no additional text or markdown code blocks."""

        print("--- Sending request to Google Gemini API ---")
        
        # Save image to bytes for upload
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG', quality=85, optimize=True)
        img_byte_arr.seek(0)
        img_bytes = img_byte_arr.read()
        
        # Create Part from image bytes
        image_part = types.Part.from_bytes(
            data=img_bytes,
            mime_type='image/jpeg'
        )
        
        # Generate analysis using new API with vision model
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=[prompt, image_part],
            )
            print(f"--- Using {MODEL} model ---")
        except Exception as e:
            print(f"--- {MODEL} failed: {e}, trying {MODEL} ---")
            try:
                response = client.models.generate_content(
                    model=MODEL,
                    contents=[prompt, image_part],
                )
                print(f"--- Using {MODEL} model ---")
            except Exception as e2:
                print(f"!!! Both vision models failed: {e2}")
                import traceback
                traceback.print_exc()
                return None
        
        # Get response text
        response_text = response.text.strip()
        print(f"--- Raw API Response (first 200 chars): {response_text[:200]}... ---")
        
        # Clean JSON response (remove markdown formatting if present)
        if response_text.startswith('```json'):
            print("--- Removing ```json markdown wrapper ---")
            response_text = response_text[7:]
        if response_text.startswith('```'):
            print("--- Removing ``` markdown wrapper ---")
            response_text = response_text[3:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        
        response_text = response_text.strip()
        
        # Try to extract JSON object if AI added extra text
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            response_text = json_match.group(0)
        
        # Parse JSON response
        print("--- Parsing JSON response ---")
        prediction_data = json.loads(response_text)
        
        # Extract values with defaults
        food_name = prediction_data.get('food_name', 'Unknown Food')
        meal_type_name = prediction_data.get('meal_type', suggested_meal_type)
        quantity_grams = float(prediction_data.get('quantity_grams', 100))
        total_calories = float(prediction_data.get('total_calories', 0))
        total_protein = float(prediction_data.get('total_protein', 0))
        total_carbs = float(prediction_data.get('total_carbs', 0))
        total_fat = float(prediction_data.get('total_fat', 0))
        confidence = float(prediction_data.get('confidence', 0.5))
        items = prediction_data.get('items', [])
        
        print(f"--- AI Detected: {food_name} ({quantity_grams}g, {total_calories} cal) ---")
        
        # Get or create meal type
        meal, created = Meal.objects.get_or_create(name=meal_type_name)
        if created:
            print(f"--- Created new meal type: {meal_type_name} ---")
        
        # Create description from items
        if items:
            food_description = f"AI Image Analysis: {food_name}. Items detected: " + ", ".join(
                f"{item.get('item', 'unknown')} ({item.get('grams', 0)}g)" 
                for item in items
            )
        else:
            food_description = f"AI Image Analysis: {food_name}"
        
        # Use the already compressed image bytes
        image_filename = f'food_{user.id}_{timezone.now().timestamp()}.jpg'
        image_content = ContentFile(img_bytes, name=image_filename)
        
        print(f"--- Saving image as: {image_filename} ---")
        
        # Create prediction record (for history)
        prediction = CaloriePrediction.objects.create(
            user=user,
            food_description=food_description,
            predicted_food_name=food_name,
            predicted_calories=total_calories,
            predicted_protein=total_protein,
            predicted_carbs=total_carbs,
            predicted_fat=total_fat,
            predicted_quantity=quantity_grams,
            confidence_score=confidence,
            ai_model_used=MODEL,
            image_path=image_content,
            was_saved_to_log=True,
        )
        print(f"--- Created CaloriePrediction ID: {prediction.id} ---")
        
        # Create FoodEntry directly
        food_entry = FoodEntry.objects.create(
            user=user,
            food_name=food_name,
            quantity=quantity_grams,
            calories=total_calories,
            protein=total_protein,
            carbs=total_carbs,
            fat=total_fat,
            meal=meal,
            is_ai_generated=True,
            notes=food_description,
            date=timezone.now().date(),
            time=timezone.now().time(),
        )
        print(f"--- Created FoodEntry ID: {food_entry.id} ---")
        
        # Create FoodImage linked to entry
        food_image = FoodImage.objects.create(
            food_entry=food_entry,
            image=image_content,
            ai_confidence=confidence,
            ai_detected_items=items,
        )
        print(f"--- Created FoodImage ID: {food_image.id} ---")
        
        print("--- ✓ AI Analysis Complete ---")
        
        return {
            'food_entry': food_entry,
            'food_image': food_image,
            'prediction': prediction,
        }
        
    except json.JSONDecodeError as e:
        print(f"!!! JSON Parse Error: {e}")
        print(f"!!! Response text: {response_text}")
        return None
    except Exception as e:
        print(f"!!! Error analyzing image: {e}")
        import traceback
        traceback.print_exc()
        return None

