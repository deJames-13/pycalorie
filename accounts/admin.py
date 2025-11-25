from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin interface for UserProfile."""
    list_display = [
        'user', 'gender', 'age', 'weight_kg', 'height_cm', 
        'bmi', 'activity_level', 'health_goal', 'daily_calorie_goal',
        'is_onboarding_complete'
    ]
    list_filter = ['gender', 'activity_level', 'health_goal', 'is_onboarding_complete']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ['bmi', 'created_at', 'updated_at']
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Biometric Data', {
            'fields': ('weight_kg', 'height_cm', 'date_of_birth', 'gender', 'bmi')
        }),
        ('Activity & Goals', {
            'fields': ('activity_level', 'health_goal', 'daily_calorie_goal', 'water_goal_liters')
        }),
        ('Status', {
            'fields': ('is_onboarding_complete', 'created_at', 'updated_at')
        }),
    )
    
    def age(self, obj):
        """Display calculated age."""
        return obj.age if obj.age else 'N/A'
    age.short_description = 'Age'
