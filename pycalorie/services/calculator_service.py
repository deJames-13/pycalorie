"""
Calorie and nutrition calculation services.
Implements TDEE (Total Daily Energy Expenditure) calculations using Mifflin-St Jeor equation.
"""
from typing import Dict, Optional


def calculate_bmr(weight_kg: float, height_cm: float, age: int, gender: str) -> float:
    """
    Calculate Basal Metabolic Rate (BMR) using Mifflin-St Jeor Equation.
    
    Args:
        weight_kg: Weight in kilograms
        height_cm: Height in centimeters
        age: Age in years
        gender: 'male', 'female', 'M', or 'F'
    
    Returns:
        BMR in calories per day
    
    Formula:
        Male: BMR = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
        Female: BMR = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
    """
    gender_normalized = gender.lower()
    
    if gender_normalized in ['male', 'm']:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    elif gender_normalized in ['female', 'f']:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
    else:
        # Default to average of both
        male_bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
        female_bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
        bmr = (male_bmr + female_bmr) / 2
    
    return bmr


def calculate_tdee(weight_kg: float, height_cm: float, age: int, gender: str, activity_level: str) -> int:
    """
    Calculate Total Daily Energy Expenditure (TDEE) - daily calorie target.
    
    Args:
        weight_kg: Weight in kilograms
        height_cm: Height in centimeters
        age: Age in years
        gender: 'male' or 'female'
        activity_level: One of 'sedentary', 'light', 'moderate', 'active', 'very_active'
    
    Returns:
        TDEE in calories per day (rounded to nearest integer)
    
    Activity Level Multipliers:
        - sedentary: Little or no exercise (1.2)
        - light: Light exercise 1-3 days/week (1.375)
        - moderate: Moderate exercise 3-5 days/week (1.55)
        - active: Hard exercise 6-7 days/week (1.725)
        - very_active: Very hard exercise & physical job or 2x training (1.9)
    """
    # Calculate BMR first
    bmr = calculate_bmr(weight_kg, height_cm, age, gender)
    
    # Activity multipliers based on standard TDEE calculations
    activity_multipliers = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very_active': 1.9,
    }
    
    # Get multiplier, default to moderate if not found
    multiplier = activity_multipliers.get(activity_level.lower(), 1.55)
    
    # Calculate TDEE
    tdee = bmr * multiplier
    
    return int(tdee)


def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    """
    Calculate Body Mass Index (BMI).
    
    Args:
        weight_kg: Weight in kilograms
        height_cm: Height in centimeters
    
    Returns:
        BMI value (rounded to 1 decimal place)
    
    Formula:
        BMI = weight_kg / (height_m)^2
    """
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 1)


def get_bmi_category(bmi: float) -> str:
    """
    Get BMI category based on WHO standards.
    
    Args:
        bmi: BMI value
    
    Returns:
        Category string
    """
    if bmi < 18.5:
        return 'Underweight'
    elif 18.5 <= bmi < 25:
        return 'Normal weight'
    elif 25 <= bmi < 30:
        return 'Overweight'
    else:
        return 'Obese'


def calculate_calorie_goal_for_goal(tdee: int, health_goal: str) -> int:
    """
    Calculate daily calorie goal based on health goal.
    
    Args:
        tdee: Total Daily Energy Expenditure
        health_goal: One of 'weight_loss', 'weight_gain', 'maintain', 'muscle_gain'
    
    Returns:
        Daily calorie goal
    
    Adjustments:
        - weight_loss: TDEE - 500 (lose ~0.5kg per week)
        - weight_gain: TDEE + 300 (gain slowly)
        - muscle_gain: TDEE + 500 (build muscle)
        - maintain: TDEE (maintain current weight)
    """
    goal_adjustments = {
        'weight_loss': -500,
        'weight_gain': 300,
        'muscle_gain': 500,
        'maintain': 0,
        'general_health': 0,
    }
    
    adjustment = goal_adjustments.get(health_goal, 0)
    calorie_goal = tdee + adjustment
    
    # Ensure minimum 1200 calories for safety
    return max(1200, calorie_goal)


def calculate_macros(calorie_goal: int, macro_ratio: Optional[Dict[str, float]] = None) -> Dict[str, float]:
    """
    Calculate macro distribution (protein, carbs, fat) based on calorie goal.
    
    Args:
        calorie_goal: Daily calorie goal
        macro_ratio: Optional dict with 'protein', 'carbs', 'fat' percentages (should sum to 1.0)
                     Default: {'protein': 0.3, 'carbs': 0.4, 'fat': 0.3}
    
    Returns:
        Dictionary with protein_g, carbs_g, fat_g values
    
    Calorie per gram:
        - Protein: 4 calories/gram
        - Carbs: 4 calories/gram
        - Fat: 9 calories/gram
    """
    if macro_ratio is None:
        # Default balanced ratio: 30% protein, 40% carbs, 30% fat
        macro_ratio = {
            'protein': 0.3,
            'carbs': 0.4,
            'fat': 0.3,
        }
    
    # Calculate calories for each macro
    protein_calories = calorie_goal * macro_ratio['protein']
    carbs_calories = calorie_goal * macro_ratio['carbs']
    fat_calories = calorie_goal * macro_ratio['fat']
    
    # Convert to grams
    protein_g = protein_calories / 4  # 4 cal/g
    carbs_g = carbs_calories / 4      # 4 cal/g
    fat_g = fat_calories / 9          # 9 cal/g
    
    return {
        'protein_g': round(protein_g, 1),
        'carbs_g': round(carbs_g, 1),
        'fat_g': round(fat_g, 1),
    }


def calculate_water_goal(weight_kg: float) -> float:
    """
    Calculate daily water intake goal in liters.
    
    Args:
        weight_kg: Weight in kilograms
    
    Returns:
        Water goal in liters (rounded to 1 decimal)
    
    Formula:
        Water (liters) = weight_kg * 0.033
        (approximately 33ml per kg of body weight)
    """
    water_liters = weight_kg * 0.033
    return round(water_liters, 1)


def calculate_ideal_weight_range(height_cm: float, gender: str) -> Dict[str, float]:
    """
    Calculate ideal weight range based on height and gender.
    Uses BMI range of 18.5-24.9 (normal weight).
    
    Args:
        height_cm: Height in centimeters
        gender: 'male' or 'female'
    
    Returns:
        Dictionary with 'min_weight' and 'max_weight' in kg
    """
    height_m = height_cm / 100
    
    # Calculate weight for BMI boundaries
    min_weight = 18.5 * (height_m ** 2)
    max_weight = 24.9 * (height_m ** 2)
    
    return {
        'min_weight': round(min_weight, 1),
        'max_weight': round(max_weight, 1),
    }


def calculate_nutrition_percentage(consumed: float, goal: float) -> float:
    """
    Calculate percentage of nutrition goal consumed.
    
    Args:
        consumed: Amount consumed
        goal: Daily goal
    
    Returns:
        Percentage (0-100+)
    """
    if goal == 0:
        return 0.0
    
    percentage = (consumed / goal) * 100
    return round(percentage, 1)
