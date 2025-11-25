from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date


class UserProfile(models.Model):
    """
    Extended user profile with userprofihealth and biometric information.
    Stores data needed for TDEE calculation and daily calorie goals.
    """
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    ACTIVITY_LEVEL_CHOICES = [
        ('sedentary', 'Sedentary (Little/No Exercise)'),
        ('light', 'Light Activity (1-3 days/week)'),
        ('moderate', 'Moderate (3-5 days/week)'),
        ('active', 'Active (6-7 days/week)'),
        ('very_active', 'Very Active (2x/day)'),
    ]
    
    HEALTH_GOAL_CHOICES = [
        ('weight_loss', 'Lose Weight'),
        ('weight_gain', 'Gain Weight'),
        ('maintain', 'Maintain Weight'),
        ('muscle_gain', 'Build Muscle'),
        ('general_health', 'General Health'),
    ]
    
    # User relationship
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    
    # Biometric data
    weight_kg = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(20.0), MaxValueValidator(300.0)],
        help_text="Weight in kilograms"
    )
    
    height_cm = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(100.0), MaxValueValidator(250.0)],
        help_text="Height in centimeters"
    )
    
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        help_text="Date of birth for age calculation"
    )
    
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default='O',
        help_text="Gender for TDEE calculation"
    )
    
    # Activity and goals
    activity_level = models.CharField(
        max_length=20,
        choices=ACTIVITY_LEVEL_CHOICES,
        default='moderate',
        help_text="Physical activity level"
    )
    
    health_goal = models.CharField(
        max_length=20,
        choices=HEALTH_GOAL_CHOICES,
        default='maintain',
        help_text="Primary health goal"
    )
    
    # Calculated values
    daily_calorie_goal = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1200), MaxValueValidator(5000)],
        help_text="Daily calorie target (calculated from TDEE)"
    )
    
    bmi = models.FloatField(
        null=True,
        blank=True,
        help_text="Body Mass Index (calculated)"
    )
    
    # Preferences
    water_goal_liters = models.FloatField(
        default=2.0,
        validators=[MinValueValidator(0.5), MaxValueValidator(10.0)],
        help_text="Daily water intake goal in liters"
    )
    
    is_onboarding_complete = models.BooleanField(
        default=False,
        help_text="Whether user has completed onboarding wizard"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    @property
    def age(self):
        """Calculate age from date of birth."""
        if not self.date_of_birth:
            return None
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
    
    @property
    def gender_for_calculation(self):
        """Return gender string for TDEE calculation."""
        return 'male' if self.gender == 'M' else 'female'
    
    @property
    def calculated_bmi(self):
        """
        Calculate BMI on-the-fly from current weight and height.
        Returns None if weight or height are not set.
        """
        if not self.weight_kg or not self.height_cm:
            return None
        
        from pycalorie.services.calculator_service import calculate_bmi
        return calculate_bmi(self.weight_kg, self.height_cm)
    
    def calculate_and_save_goals(self):
        """
        Calculate BMI, TDEE, and daily calorie goal based on profile data.
        Uses the calculator_service for all calculations.
        """
        if not all([self.weight_kg, self.height_cm, self.date_of_birth, self.activity_level]):
            return False
        
        from pycalorie.services.calculator_service import (
            calculate_bmi, calculate_tdee, calculate_calorie_goal_for_goal, calculate_water_goal
        )
        
        # Calculate BMI
        self.bmi = calculate_bmi(self.weight_kg, self.height_cm)
        
        # Calculate TDEE
        age = self.age
        if age:
            tdee = calculate_tdee(
                weight_kg=self.weight_kg,
                height_cm=self.height_cm,
                age=age,
                gender=self.gender_for_calculation,
                activity_level=self.activity_level
            )
            
            # Adjust for health goal
            self.daily_calorie_goal = calculate_calorie_goal_for_goal(tdee, self.health_goal)
        
        # Calculate water goal
        self.water_goal_liters = calculate_water_goal(self.weight_kg)
        
        self.save()
        return True


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a UserProfile when a new User is created."""
    if created:
        UserProfile.objects.create(user=instance)
