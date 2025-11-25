from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Food(models.Model):
    """
    Food database - stores nutritional information for food items.
    Corresponds to FoodDatabase in ERD.
    """
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    
    # Nutritional values per 100g (standard serving)
    calories_per_100g = models.FloatField(
        validators=[MinValueValidator(0.0)],
        help_text="Calories per 100 grams"
    )
    protein_per_100g = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0)],
        help_text="Protein per 100 grams in grams"
    )
    carbs_per_100g = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0)],
        help_text="Carbohydrates per 100 grams in grams"
    )
    fat_per_100g = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0)],
        help_text="Fat per 100 grams in grams"
    )
    fiber_per_100g = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0)],
        help_text="Fiber per 100 grams in grams"
    )
    
    # Standard serving information
    serving_size = models.CharField(
        max_length=100,
        default="100g",
        help_text="Standard serving size description"
    )
    
    # Verification and tracking
    is_verified = models.BooleanField(
        default=False,
        help_text="Whether this food item has been verified by admin"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_foods'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Food"
        verbose_name_plural = "Foods"
        indexes = [
            models.Index(fields=['name', 'is_verified']),
        ]

    def __str__(self):
        return f"{self.name} ({self.serving_size})"


class Meal(models.Model):
    """Meal types: Breakfast, Lunch, Dinner, Snack."""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0, help_text="Display order")

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Meal Type"
        verbose_name_plural = "Meal Types"

    def __str__(self):
        return self.name


class DailyLog(models.Model):
    """
    Daily summary log for users - tracks total nutrition per day.
    One record per user per day.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_logs')
    date = models.DateField(default=timezone.now, db_index=True)
    
    # Daily totals (calculated from FoodEntries)
    total_calories = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    total_protein = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    total_carbs = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    total_fat = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    total_fiber = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    
    # Water tracking (in liters)
    total_water_liters = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0)],
        help_text="Water intake in liters"
    )
    
    # Goals (snapshot of user's goal at this date)
    calorie_goal = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        unique_together = ['user', 'date']
        verbose_name = "Daily Log"
        verbose_name_plural = "Daily Logs"
        indexes = [
            models.Index(fields=['user', '-date']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.date}"

    @property
    def calorie_remaining(self):
        """Calculate remaining calories for the day."""
        if self.calorie_goal:
            return max(0, self.calorie_goal - self.total_calories)
        return None

    @property
    def calorie_percentage(self):
        """Calculate percentage of calorie goal achieved."""
        if self.calorie_goal and self.calorie_goal > 0:
            return min(100, (self.total_calories / self.calorie_goal) * 100)
        return None
    
    def update_totals(self):
        """Recalculate totals from all food entries for this day."""
        entries = self.food_entries.all()
        
        self.total_calories = sum(entry.total_calories for entry in entries)
        self.total_protein = sum(entry.total_protein for entry in entries)
        self.total_carbs = sum(entry.total_carbs for entry in entries)
        self.total_fat = sum(entry.total_fat for entry in entries)
        self.total_fiber = sum(entry.total_fiber for entry in entries)
        
        # Update calorie goal from user profile
        if hasattr(self.user, 'profile') and self.user.profile.daily_calorie_goal:
            self.calorie_goal = self.user.profile.daily_calorie_goal
        
        self.save()


class FoodEntry(models.Model):
    """
    Individual food entries logged by users.
    Can be created directly without Food FK (direct entry mode).
    Links to DailyLog for aggregation.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='food_entries')
    daily_log = models.ForeignKey(
        DailyLog,
        on_delete=models.CASCADE,
        related_name='food_entries',
        null=True,
        blank=True
    )
    
    # Optional Food FK (for database lookups)
    food = models.ForeignKey(
        Food, 
        on_delete=models.CASCADE, 
        related_name='entries',
        null=True,
        blank=True,
        help_text="Link to Food database (optional)"
    )
    
    # Direct entry fields (allows manual entry without Food FK)
    food_name = models.CharField(
        max_length=200,
        help_text="Name of the food (required for direct entry)"
    )
    calories = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0)],
        help_text="Total calories for this entry"
    )
    protein = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0)],
        help_text="Protein in grams"
    )
    carbs = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0)],
        help_text="Carbs in grams"
    )
    fat = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0)],
        help_text="Fat in grams"
    )
    fiber = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0)],
        help_text="Fiber in grams"
    )
    
    meal = models.ForeignKey(
        Meal,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='entries'
    )
    
    quantity = models.FloatField(
        validators=[MinValueValidator(0.0)],
        help_text="Quantity in grams"
    )
    
    date = models.DateField(default=timezone.now, db_index=True)
    time = models.TimeField(default=timezone.now)
    
    # AI tracking
    is_ai_generated = models.BooleanField(
        default=False,
        help_text="Whether this entry was created from AI prediction"
    )
    image_url = models.ImageField(
        upload_to='food_images/%Y/%m/%d/',
        null=True,
        blank=True,
        help_text="Optional food image"
    )
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-time']
        verbose_name = "Food Entry"
        verbose_name_plural = "Food Entries"
        indexes = [
            models.Index(fields=['user', '-date']),
            models.Index(fields=['daily_log']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.food_name} ({self.quantity}g) on {self.date}"

    @property
    def total_calories(self):
        """Calculate total calories for this entry."""
        if self.food:
            # Use Food FK if available
            return (self.food.calories_per_100g * self.quantity) / 100
        # Use direct entry values
        return self.calories

    @property
    def total_protein(self):
        """Calculate total protein for this entry."""
        if self.food:
            return (self.food.protein_per_100g * self.quantity) / 100
        return self.protein

    @property
    def total_carbs(self):
        """Calculate total carbohydrates for this entry."""
        if self.food:
            return (self.food.carbs_per_100g * self.quantity) / 100
        return self.carbs

    @property
    def total_fat(self):
        """Calculate total fat for this entry."""
        if self.food:
            return (self.food.fat_per_100g * self.quantity) / 100
        return self.fat
    
    @property
    def total_fiber(self):
        """Calculate total fiber for this entry."""
        if self.food:
            return (self.food.fiber_per_100g * self.quantity) / 100
        return self.fiber
    
    def save(self, *args, **kwargs):
        """Override save to populate food_name and update DailyLog totals."""
        # If Food FK exists, use it to populate food_name
        if self.food and not self.food_name:
            self.food_name = self.food.name
        
        super().save(*args, **kwargs)
        
        # Get or create daily log for this date
        daily_log, created = DailyLog.objects.get_or_create(
            user=self.user,
            date=self.date
        )
        
        # Link to daily log if not already linked
        if not self.daily_log:
            self.daily_log = daily_log
            super().save(update_fields=['daily_log'])
        
        # Update daily log totals
        daily_log.update_totals()


class FoodImage(models.Model):
    """
    Food images for Instagram-style gallery view.
    Linked to FoodEntry for nutritional context.
    """
    food_entry = models.OneToOneField(
        FoodEntry,
        on_delete=models.CASCADE,
        related_name='food_image',
        help_text="Associated food entry"
    )
    image = models.ImageField(
        upload_to='food_images/%Y/%m/%d/',
        help_text="Food image uploaded by user or AI"
    )
    thumbnail = models.ImageField(
        upload_to='food_thumbnails/%Y/%m/%d/',
        null=True,
        blank=True,
        help_text="Thumbnail for gallery view"
    )
    
    # AI analysis metadata
    ai_confidence = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="AI confidence score (0-1)"
    )
    ai_detected_items = models.JSONField(
        null=True,
        blank=True,
        help_text="List of detected food items from AI"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Food Image"
        verbose_name_plural = "Food Images"
    
    def __str__(self):
        return f"Image for {self.food_entry.food_name} on {self.food_entry.date}"
    
    def save(self, *args, **kwargs):
        """Override save to create thumbnail."""
        super().save(*args, **kwargs)
        
        # Create thumbnail if image exists and thumbnail doesn't
        if self.image and not self.thumbnail:
            from PIL import Image
            import os
            from django.core.files.base import ContentFile
            from io import BytesIO
            
            # Open image
            img = Image.open(self.image.path)
            
            # Create thumbnail (300x300)
            img.thumbnail((300, 300), Image.Resampling.LANCZOS)
            
            # Save thumbnail
            thumb_io = BytesIO()
            img.save(thumb_io, format='JPEG', quality=85)
            
            # Generate thumbnail filename
            thumb_name = f"thumb_{os.path.basename(self.image.name)}"
            
            self.thumbnail.save(
                thumb_name,
                ContentFile(thumb_io.getvalue()),
                save=False
            )
            super().save(update_fields=['thumbnail'])


class CaloriePrediction(models.Model):
    """Store AI-generated calorie predictions from text or images."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='predictions')
    
    # Input
    food_description = models.TextField(help_text="User's food description or image analysis")
    image_path = models.ImageField(
        upload_to='prediction_images/%Y/%m/%d/',
        null=True,
        blank=True,
        help_text="Optional uploaded image"
    )
    
    # Prediction results
    predicted_food_name = models.CharField(max_length=200)
    predicted_calories = models.FloatField(validators=[MinValueValidator(0.0)])
    predicted_protein = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    predicted_carbs = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    predicted_fat = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    predicted_quantity = models.FloatField(
        default=100.0,
        validators=[MinValueValidator(0.0)],
        help_text="Predicted quantity in grams"
    )
    
    # AI metadata
    confidence_score = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="AI confidence score (0-1)"
    )
    ai_model_used = models.CharField(max_length=50, default='google-genai')
    
    # Was it used?
    was_saved_to_log = models.BooleanField(
        default=False,
        help_text="Whether user saved this prediction to their food log"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Calorie Prediction"
        verbose_name_plural = "Calorie Predictions"
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.predicted_food_name} ({self.predicted_calories} kcal)"
