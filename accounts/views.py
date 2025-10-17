from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from .forms import CustomUserCreationForm, CustomAuthenticationForm


class CustomLoginView(LoginView):
    """Enhanced login view with custom form and template."""
    
    form_class = CustomAuthenticationForm
    template_name = 'accounts/sign-in.html'
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        """Handle successful login."""
        remember_me = form.cleaned_data.get('remember_me')
        if remember_me:
            # Set session to expire in 30 days
            self.request.session.set_expiry(30 * 24 * 60 * 60)
        else:
            # Set session to expire when browser closes
            self.request.session.set_expiry(0)
        
        messages.success(self.request, f'Welcome back, {form.get_user().first_name or form.get_user().username}!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Handle invalid login attempts."""
        messages.error(self.request, 'Invalid username or password. Please try again.')
        return super().form_invalid(form)
    
    def get_success_url(self):
        """Redirect to next page or home after login."""
        next_page = self.request.GET.get('next')
        if next_page:
            return next_page
        return reverse_lazy('index')  # Redirect to home page


class CustomLogoutView(LogoutView):
    """Enhanced logout view."""
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, 'You have been successfully logged out. See you next time!')
        return super().dispatch(request, *args, **kwargs)
    
    def get_next_page(self):
        """Redirect to home page after logout."""
        return reverse_lazy('index')


class SignUpView(CreateView):
    """Enhanced user registration view."""
    
    model = User
    form_class = CustomUserCreationForm
    template_name = 'accounts/sign-up.html'
    success_url = reverse_lazy('accounts:login')
    
    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Redirect authenticated users
        if request.user.is_authenticated:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        """Handle successful registration."""
        response = super().form_valid(form)
        
        # Get the created user
        user = form.instance
        
        # Log the user in automatically after registration
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        
        if user:
            login(self.request, user)
            messages.success(
                self.request, 
                f'Welcome to PyCalorie, {user.first_name}! Your account has been created successfully. '
                'Let\'s start your health journey!'
            )
            return redirect('index')  # Redirect to home page after signup
        
        return response
    
    def form_invalid(self, form):
        """Handle registration errors."""
        messages.error(
            self.request, 
            'There were some errors with your registration. Please check the form and try again.'
        )
        return super().form_invalid(form)


def password_reset_view(request):
    """Simple password reset view (placeholder)."""
    if request.method == 'POST':
        email = request.POST.get('email')
        if email and User.objects.filter(email=email).exists():
            messages.success(
                request, 
                f'Password reset instructions have been sent to {email}. '
                'Please check your email inbox and spam folder.'
            )
        else:
            messages.error(request, 'No account found with this email address.')
        return redirect('accounts:login')
    
    return render(request, 'accounts/password_reset.html')


@login_required
def profile_view(request):
    """User profile view (placeholder for future development)."""
    return render(request, 'accounts/profile.html', {
        'user': request.user
    })


# Function-based views as alternatives

def login_view(request):
    """Function-based login view (alternative)."""
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                remember_me = form.cleaned_data.get('remember_me')
                if remember_me:
                    request.session.set_expiry(30 * 24 * 60 * 60)  # 30 days
                else:
                    request.session.set_expiry(0)  # Browser close
                
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                return redirect(request.GET.get('next', 'index'))
            else:
                messages.error(request, 'Invalid credentials.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'accounts/sign-in.html', {'form': form})


def signup_view(request):
    """Function-based signup view (alternative)."""
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            
            if user:
                login(request, user)
                messages.success(
                    request, 
                    f'Welcome to PyCalorie, {user.first_name}! Your account has been created successfully.'
                )
                return redirect('index')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/sign-up.html', {'form': form})


def logout_view(request):
    """Function-based logout view (alternative)."""
    if request.user.is_authenticated:
        messages.success(request, 'You have been successfully logged out. See you next time!')
        logout(request)
    return redirect('index')
