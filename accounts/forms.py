from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
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