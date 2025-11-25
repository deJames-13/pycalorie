from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserProfile
import re


class CustomUserCreationForm(UserCreationForm):
    """Enhanced user creation form with additional fields and validation."""
    
    first_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter your first name'
        })
    )
    
    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter your last name'
        })
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter your email address'
        })
    )
    
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Choose a username'
        })
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Create a strong password'
        })
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Confirm your password'
        })
    )
    
    # Optional health goal fields
    HEALTH_GOAL_CHOICES = [
        ('', 'Select your main goal'),
        ('weight_loss', 'Lose Weight'),
        ('weight_gain', 'Gain Weight'),
        ('maintain', 'Maintain Weight'),
        ('muscle_gain', 'Build Muscle'),
        ('general_health', 'General Health'),
    ]
    
    ACTIVITY_LEVEL_CHOICES = [
        ('', 'Select activity level'),
        ('sedentary', 'Sedentary (Little/No Exercise)'),
        ('light', 'Light Activity (1-3 days/week)'),
        ('moderate', 'Moderate (3-5 days/week)'),
        ('active', 'Active (6-7 days/week)'),
        ('very_active', 'Very Active (2x/day)'),
    ]
    
    health_goal = forms.ChoiceField(
        choices=HEALTH_GOAL_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    activity_level = forms.ChoiceField(
        choices=ACTIVITY_LEVEL_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    terms = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        error_messages={
            'required': 'You must accept the terms and conditions.'
        }
    )
    
    newsletter = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_email(self):
        """Validate email uniqueness."""
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email

    def clean_username(self):
        """Validate username format and uniqueness."""
        username = self.cleaned_data.get('username')
        
        # Check length
        if len(username) < 3:
            raise ValidationError("Username must be at least 3 characters long.")
        
        # Check for valid characters (alphanumeric and underscore only)
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValidationError("Username can only contain letters, numbers, and underscores.")
        
        # Check uniqueness
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        
        return username

    def clean_password1(self):
        """Enhanced password validation."""
        password1 = self.cleaned_data.get('password1')
        
        if len(password1) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        
        # Check for at least one letter and one number
        if not re.search(r'[A-Za-z]', password1) or not re.search(r'\d', password1):
            raise ValidationError("Password must contain at least one letter and one number.")
        
        return password1

    def save(self, commit=True):
        """Save the user with additional profile information."""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Here you can save additional profile information to a separate UserProfile model
            # if you create one in the future for health goals, activity level, etc.
        
        return user


class CustomAuthenticationForm(AuthenticationForm):
    """Enhanced login form with better styling."""
    
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter your username',
            'autofocus': True
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter your password'
        })
    )
    
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to error messages
        for field in self.fields.values():
            field.error_messages = {
                'required': f'This field is required.',
                'invalid': f'Please enter a valid value.'
            }


class PasswordResetForm(forms.Form):
    """Custom password reset form."""
    
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter your email address',
            'autofocus': True
        })
    )

    def clean_email(self):
        """Validate that the email exists in the system."""
        email = self.cleaned_data.get('email')
        if email and not User.objects.filter(email=email).exists():
            raise ValidationError("No account found with this email address.")
        return email


class UserProfileEditForm(forms.ModelForm):
    """Form for editing user profile information."""
    
    first_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        })
    )
    
    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address'
        })
    )
    
    class Meta:
        model = UserProfile
        fields = [
            'weight_kg', 'height_cm', 'date_of_birth', 'gender',
            'activity_level', 'health_goal', 'daily_calorie_goal',
            'water_goal_liters'
        ]
        widgets = {
            'weight_kg': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Weight in kg',
                'step': '0.1',
                'min': '20',
                'max': '300'
            }),
            'height_cm': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Height in cm',
                'step': '0.1',
                'min': '100',
                'max': '250'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-select'
            }),
            'activity_level': forms.Select(attrs={
                'class': 'form-select'
            }),
            'health_goal': forms.Select(attrs={
                'class': 'form-select'
            }),
            'daily_calorie_goal': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Daily Calorie Goal',
                'min': '1200',
                'max': '5000'
            }),
            'water_goal_liters': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Water Goal (Liters)',
                'step': '0.1',
                'min': '0.5',
                'max': '10'
            }),
        }
        labels = {
            'weight_kg': 'Weight (kg)',
            'height_cm': 'Height (cm)',
            'date_of_birth': 'Date of Birth',
            'gender': 'Gender',
            'activity_level': 'Activity Level',
            'health_goal': 'Health Goal',
            'daily_calorie_goal': 'Daily Calorie Goal (optional - auto-calculated)',
            'water_goal_liters': 'Daily Water Goal (Liters)',
        }
        help_texts = {
            'daily_calorie_goal': 'Leave blank to auto-calculate based on your biometrics and goals',
            'water_goal_liters': 'Recommended: 2-3 liters per day',
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Pre-populate user fields
        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email
    
    def clean_email(self):
        """Validate email uniqueness (excluding current user)."""
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(pk=self.user.pk).exists():
            raise ValidationError("An account with this email already exists.")
        return email
    
    def save(self, commit=True):
        """Save both User and UserProfile."""
        profile = super().save(commit=False)
        
        # Update User model fields
        if self.user:
            self.user.first_name = self.cleaned_data['first_name']
            self.user.last_name = self.cleaned_data['last_name']
            self.user.email = self.cleaned_data['email']
            if commit:
                self.user.save()
        
        # Recalculate goals if biometrics changed
        if commit:
            profile.save()
            
            # Only auto-calculate if daily_calorie_goal is not manually set
            if not self.cleaned_data.get('daily_calorie_goal'):
                profile.calculate_and_save_goals()
        
        return profile
