# PyCalorie Tracker 🔥

**PyCalorie** is a modern, AI-powered calorie tracking application built with Django 4.2. It combines traditional manual food logging with cutting-edge Google Gemini AI to analyze food photos and predict nutritional information, making calorie tracking effortless and accurate.

[![Django](https://img.shields.io/badge/Django-4.2.9-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple.svg)](https://getbootstrap.com/)
[![Google GenAI](https://img.shields.io/badge/Google-GenAI-orange.svg)](https://ai.google.dev/)

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage Guide](#-usage-guide)
- [API Documentation](#-api-documentation)
- [Development](#-development)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### 🎯 Core Features
- **User Authentication & Authorization** - Secure login/register system with Django auth
- **Onboarding Wizard** - Guided setup to calculate BMI, TDEE, and daily calorie goals
- **Dashboard** - Real-time progress tracking with circular progress bars
- **Manual Food Logging** - Search and log food from a comprehensive database
- **AI Image Analysis** - Upload food photos for instant calorie prediction using Google Gemini
- **Water Tracking** - Monitor daily water intake with visual indicators
- **Food Gallery** - Instagram-style gallery of your food photos
- **Analytics & Insights** - Visualize progress with Chart.js graphs

### 🤖 AI-Powered Features
- **Text-to-Nutrition** - Describe food in natural language, get instant nutrition facts
- **Image-to-Nutrition** - Upload food photos for automatic calorie detection
- **Meal Type Detection** - AI automatically categorizes meals (Breakfast/Lunch/Dinner/Snack)
- **Multi-Item Detection** - Recognizes multiple food items in a single photo
- **Confidence Scoring** - AI provides confidence levels for predictions

### 📊 Health Tracking
- **BMI Calculator** - Automatic Body Mass Index calculation
- **TDEE Calculation** - Total Daily Energy Expenditure using Mifflin-St Jeor equation
- **Goal Setting** - Weight loss, gain, maintenance, or muscle building goals
- **Macro Tracking** - Monitor protein, carbs, and fats
- **Water Goals** - Personalized daily water intake recommendations

### 📱 User Experience
- **Mobile-Responsive Design** - Bootstrap 5 ensures perfect mobile experience
- **Dark Mode Ready** - Built-in theme switching capability
- **Quick Actions** - Thumb-friendly buttons for rapid logging
- **Real-time Updates** - Instant feedback on daily progress
- **Search & Autocomplete** - Fast food database search

---

## 🛠 Tech Stack

### Backend
- **Django 4.2.9** - High-level Python web framework
- **SQLite/PostgreSQL/MySQL** - Flexible database options
- **Pillow 12.0.0** - Image processing and compression
- **Google GenAI 1.52.0** - AI-powered calorie prediction
- **Gunicorn 21.2.0** - Production WSGI server
- **WhiteNoise 6.6.0** - Static file serving

### Frontend
- **Bootstrap 5** - Responsive UI framework
- **Chart.js** - Interactive data visualizations
- **Pixel Lite Theme** - Modern, elegant design system
- **Vanilla JavaScript** - Clean, dependency-free interactions

### AI/ML
- **Google Gemini 2.5 Pro** - Advanced vision and language model
- **Google Gemini 2.5 Flash** - Fast, efficient model for quick predictions

---

## 📁 Project Structure

```
pycalorie/
├── manage.py                      # Django management script
├── requirements.txt               # Python dependencies
├── db.sqlite3                     # SQLite database (development)
├── env.sample                     # Environment variables template
├── docker-compose.yml             # Docker configuration
├── Dockerfile                     # Docker image definition
├── build.sh                       # Deployment build script
├── gunicorn-cfg.py               # Gunicorn configuration
│
├── core/                          # Project settings
│   ├── settings.py               # Main configuration file
│   ├── urls.py                   # Root URL routing
│   ├── wsgi.py                   # WSGI application
│   └── asgi.py                   # ASGI application
│
├── accounts/                      # User authentication & profiles
│   ├── models.py                 # UserProfile, biometrics
│   ├── views.py                  # Login, register, profile views
│   ├── forms.py                  # User forms
│   ├── urls.py                   # Auth routes
│   └── templates/                # Auth templates
│
├── pycalorie/                     # Main tracking app
│   ├── models.py                 # Food, DailyLog, FoodEntry, etc.
│   ├── urls.py                   # Tracker routes
│   ├── admin.py                  # Admin interface customization
│   │
│   ├── views/                    # View modules
│   │   ├── dashboard.py          # Dashboard & home
│   │   ├── food_logging.py       # Manual food logging
│   │   ├── ai_prediction.py      # AI calorie prediction
│   │   └── analytics.py          # Charts & statistics
│   │
│   ├── services/                 # Business logic (DRY principle)
│   │   ├── calculator_service.py # TDEE, BMI, macro calculations
│   │   └── ai_service.py         # Google GenAI integration
│   │
│   ├── templatetags/             # Custom template filters
│   │   └── pycalorie_filters.py  # Formatting filters
│   │
│   └── management/commands/      # Custom Django commands
│
├── dashboard/                     # Legacy dashboard app
│   └── (basic dashboard views)
│
├── home/                          # Landing pages
│   ├── views.py                  # Home, about, contact
│   └── urls.py
│
├── templates/                     # HTML templates
│   ├── layouts/                  # Base templates
│   ├── includes/                 # Reusable components
│   ├── pages/                    # Static pages
│   ├── accounts/                 # Auth templates
│   └── dashboard/                # Dashboard templates
│
├── static/                        # Static assets
│   ├── css/                      # Stylesheets
│   │   └── pixel.css             # Main theme CSS
│   ├── scss/                     # SASS source files
│   ├── assets/                   # Images, fonts
│   └── vendor/                   # Third-party libraries
│
├── media/                         # User uploads
│   ├── food_images/              # Original food photos
│   ├── food_thumbnails/          # Compressed thumbnails
│   └── prediction_images/        # AI prediction images
│
├── staticfiles/                   # Collected static files (production)
│
└── nginx/                         # Nginx configuration (production)
```

---

## 🚀 Installation

### Prerequisites

- **Python 3.10+** ([Download](https://www.python.org/downloads/))
- **pip** (Python package manager)
- **Git** ([Download](https://git-scm.com/downloads))
- **Google Cloud Account** (for GenAI API key - [Get Free Key](https://ai.google.dev/))
- **Virtual Environment** (recommended)

### 🪟 Windows Quick Setup (Automated)

**For Windows users, we provide automated setup scripts:**

1. **Clone or download the repository**
2. **Run the setup script:**
   ```cmd
   setup.bat
   ```
   
The script will automatically:
- ✅ Check Python installation
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Create .env configuration file
- ✅ Setup database with migrations
- ✅ Collect static files
- ✅ Guide you through superuser creation
- ✅ Optionally start the server

3. **Quick start scripts (after setup):**
   ```cmd
   # Start the development server
   start.bat
   
   # Create admin account
   create_superuser.bat
   ```

---

### 🐧 Manual Installation (All Platforms)

### Step 1: Clone the Repository

```bash
git clone https://github.com/deJames-13/pycalorie.git
cd pycalorie
```

### Step 2: Create Virtual Environment

#### Linux/Mac
```bash
python3 -m venv env
source env/bin/activate
```

#### Windows
```cmd
python -m venv env
env\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Environment Configuration

1. Copy the sample environment file:

**Linux/Mac:**
```bash
cp env.sample .env
```

**Windows:**
```cmd
copy env.sample .env
```

2. Edit `.env` and configure:
```bash
# Development mode
DEBUG=True

# Generate a strong secret key
SECRET_KEY=your-super-secret-key-here

# Google GenAI API Key (REQUIRED for AI features)
GOOGLE_API_KEY=your-google-api-key-here

# Database (Optional - defaults to SQLite)
# DB_ENGINE=postgresql
# DB_HOST=localhost
# DB_NAME=pycalorie_db
# DB_USERNAME=pycalorie_user
# DB_PASS=secure_password
# DB_PORT=5432
```

### Step 5: Database Setup

```bash
# Create database tables
python manage.py makemigrations
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser
# Follow prompts to set username, email, and password
```

### Step 6: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### Step 7: Run Development Server

```bash
python manage.py runserver
```

✅ **Success!** Open your browser and navigate to:
- **Application:** http://127.0.0.1:8000
- **Admin Panel:** http://127.0.0.1:8000/admin

---

## 🔧 Configuration

### Getting Google GenAI API Key

1. Visit [Google AI Studio](https://ai.google.dev/)
2. Sign in with your Google account
3. Click **Get API Key**
4. Create a new API key
5. Copy the key and add to `.env`:
   ```bash
   GOOGLE_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXX
   ```

### Database Configuration

#### SQLite (Default - Development)
```python
# No configuration needed - works out of the box
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

#### PostgreSQL (Recommended - Production)
```bash
# .env file
DB_ENGINE=postgresql
DB_HOST=localhost
DB_NAME=pycalorie_db
DB_USERNAME=pycalorie_user
DB_PASS=secure_password
DB_PORT=5432
```

#### MySQL
```bash
# .env file
DB_ENGINE=mysql
DB_HOST=localhost
DB_NAME=pycalorie_db
DB_USERNAME=pycalorie_user
DB_PASS=secure_password
DB_PORT=3306
```

### Static & Media Files

```python
# settings.py
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### Security Settings (Production)

```python
# .env for production
DEBUG=False
SECRET_KEY=<use-strong-64-char-random-key>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

---

## 📖 Usage Guide

### 1. User Registration & Onboarding

#### Step 1: Register Account
1. Navigate to http://127.0.0.1:8000/accounts/register/
2. Fill in username, email, and password
3. Click **Register**

#### Step 2: Complete Profile Setup
1. Go to **Profile** or **Settings**
2. Enter biometric data:
   - **Weight (kg):** Your current weight
   - **Height (cm):** Your height
   - **Date of Birth:** For age calculation
   - **Gender:** Male, Female, or Other
   - **Activity Level:** Select from sedentary to very active
   - **Health Goal:** Weight loss, gain, maintain, or muscle building

3. Click **Save Profile**
4. System automatically calculates:
   - BMI (Body Mass Index)
   - TDEE (Total Daily Energy Expenditure)
   - Daily Calorie Goal
   - Water Intake Goal

### 2. Dashboard Overview

The dashboard shows:
- **Circular Progress Bar:** Calories consumed vs. goal
- **Macro Summary Cards:** Protein, Carbs, Fat totals
- **Water Tracker:** Visual water intake indicator
- **Today's Meals:** Quick view of logged foods
- **Quick Actions:** Large buttons for "Log Meal" and "Upload Photo"

### 3. Manual Food Logging

#### Option A: Search Food Database
1. Click **Log Meal** or navigate to `/tracker/log/`
2. Select meal type (Breakfast, Lunch, Dinner, Snack)
3. Start typing food name in search box
4. Select from dropdown suggestions
5. Enter quantity in grams
6. Click **Add to Log**

#### Option B: Manual Entry (Custom Food)
1. Click **Create Custom Food**
2. Enter:
   - Food name
   - Quantity (grams)
   - Calories
   - Protein, Carbs, Fat (optional)
3. Click **Save**

### 4. AI-Powered Calorie Prediction

#### Method 1: Text-to-Nutrition
1. Click **AI Predict** or navigate to `/tracker/predict/text/`
2. Describe your food naturally:
   - "a medium apple"
   - "grilled chicken breast with rice"
   - "two slices of pepperoni pizza"
3. Click **Predict**
4. AI returns:
   - Detected food name
   - Estimated calories
   - Macro breakdown (protein, carbs, fat)
   - Confidence score
5. Review and click **Save to Log** or **Edit** then save

#### Method 2: Image-to-Nutrition (Most Accurate!)
1. Click **Upload Photo** or navigate to `/tracker/predict/image/`
2. Take or upload a food photo
3. AI analyzes:
   - All visible food items
   - Portion sizes (in grams)
   - Total calories
   - Macro breakdown
   - Suggested meal type (based on time)
4. Review detected items
5. Click **Save to Log** - automatically creates food entry with image

**AI Features:**
- Detects multiple items in one photo
- Estimates portion sizes
- Auto-categorizes meal type
- Provides confidence scores
- Saves image to gallery

### 5. Water Tracking

1. On dashboard, find **Water Tracker** widget
2. Click **+** button to add 250ml (1 glass)
3. Visual indicator fills up as you approach your goal
4. Daily water goal based on your weight (33ml per kg)

### 6. Food Gallery

1. Navigate to **Gallery** or `/tracker/gallery/`
2. View all your food photos in Instagram-style grid
3. Click any photo to see:
   - Full-size image
   - Detected food items
   - Nutritional breakdown
   - Date and meal type
4. Share or delete entries

### 7. Analytics & Insights

Navigate to **Analytics** or `/tracker/analytics/`

#### Available Charts:
- **Weight Progress Line Chart** - 30-day weight tracking
- **Calorie Consistency Bar Chart** - Goal vs. Actual (weekly)
- **Macro Distribution Pie Chart** - Protein/Carbs/Fat ratio
- **Weekly Summary** - Total calories, average macros
- **Monthly Trends** - Long-term progress visualization

#### Export Data:
- Download CSV reports
- Share progress screenshots
- Track long-term trends

### 8. Profile Management

#### Update Biometrics
1. Go to **Profile** or `/accounts/profile/`
2. Update any biometric data
3. Click **Recalculate Goals**
4. System updates TDEE and calorie targets

#### Change Goals
1. Select new health goal (e.g., from weight loss to maintenance)
2. Adjust activity level if needed
3. Save changes
4. Daily calorie goal updates automatically

---

## 🔌 API Documentation

### Internal Service APIs

#### Calculator Service
Located in `pycalorie/services/calculator_service.py`

##### `calculate_bmr(weight_kg, height_cm, age, gender)`
Calculate Basal Metabolic Rate using Mifflin-St Jeor equation.

**Parameters:**
- `weight_kg` (float): Weight in kilograms
- `height_cm` (float): Height in centimeters
- `age` (int): Age in years
- `gender` (str): 'male', 'female', 'M', or 'F'

**Returns:** `float` - BMR in calories/day

**Example:**
```python
from pycalorie.services.calculator_service import calculate_bmr

bmr = calculate_bmr(weight_kg=70, height_cm=175, age=30, gender='male')
# Returns: 1673.75
```

##### `calculate_tdee(weight_kg, height_cm, age, gender, activity_level)`
Calculate Total Daily Energy Expenditure.

**Parameters:**
- Same as BMR, plus:
- `activity_level` (str): 'sedentary', 'light', 'moderate', 'active', 'very_active'

**Returns:** `int` - TDEE in calories/day

**Example:**
```python
from pycalorie.services.calculator_service import calculate_tdee

tdee = calculate_tdee(
    weight_kg=70, 
    height_cm=175, 
    age=30, 
    gender='male',
    activity_level='moderate'
)
# Returns: 2594 (BMR * 1.55 activity multiplier)
```

##### `calculate_bmi(weight_kg, height_cm)`
Calculate Body Mass Index.

**Returns:** `float` - BMI value

**Example:**
```python
from pycalorie.services.calculator_service import calculate_bmi

bmi = calculate_bmi(weight_kg=70, height_cm=175)
# Returns: 22.9 (Normal weight)
```

#### AI Service
Located in `pycalorie/services/ai_service.py`

##### `predict_calories(user, food_description)`
Predict nutritional info from text description using Google Gemini.

**Parameters:**
- `user` (User): Django User object
- `food_description` (str): Natural language food description

**Returns:** `CaloriePrediction` object or `None`

**Example:**
```python
from pycalorie.services.ai_service import predict_calories

prediction = predict_calories(
    user=request.user,
    food_description="two slices of pepperoni pizza"
)

print(f"Food: {prediction.predicted_food_name}")
print(f"Calories: {prediction.predicted_calories}")
print(f"Confidence: {prediction.confidence_score}")
```

##### `analyze_food_image(image_file, user)`
Analyze food photo and create food entry automatically.

**Parameters:**
- `image_file` (UploadedFile): Django UploadedFile from request.FILES
- `user` (User): Django User object

**Returns:** `dict` with 'food_entry', 'food_image', 'prediction' or `None`

**Example:**
```python
from pycalorie.services.ai_service import analyze_food_image

result = analyze_food_image(
    image_file=request.FILES['food_image'],
    user=request.user
)

if result:
    food_entry = result['food_entry']
    food_image = result['food_image']
    prediction = result['prediction']
    
    print(f"Created entry: {food_entry.food_name}")
    print(f"Calories: {food_entry.calories}")
    print(f"Image URL: {food_image.image.url}")
```

### URL Endpoints

#### Authentication
- `GET /accounts/register/` - Registration page
- `POST /accounts/register/` - Register new user
- `GET /accounts/login/` - Login page
- `POST /accounts/login/` - Authenticate user
- `GET /accounts/logout/` - Logout user
- `GET /accounts/profile/` - User profile & settings

#### Dashboard
- `GET /tracker/` - Main dashboard
- `GET /dashboard/` - Legacy dashboard (redirects to /tracker/)

#### Food Logging
- `GET /tracker/log/` - Food logging page
- `POST /tracker/log/` - Create food entry
- `GET /tracker/log/edit/<id>/` - Edit food entry
- `POST /tracker/log/edit/<id>/` - Update food entry
- `POST /tracker/log/delete/<id>/` - Delete food entry
- `GET /tracker/log/history/` - Food log history

#### Food Search (AJAX)
- `GET /tracker/food/search/?q=<query>` - Search food database
- `POST /tracker/food/create/` - Create custom food

#### Water Tracking
- `POST /tracker/water/add/` - Add water (250ml increment)

#### AI Predictions
- `GET /tracker/predict/text/` - Text prediction page
- `POST /tracker/predict/text/` - Create text prediction
- `GET /tracker/predict/image/` - Image upload page
- `POST /tracker/predict/image/` - Analyze food image
- `GET /tracker/predict/result/<id>/` - View prediction result
- `POST /tracker/predict/save/<id>/` - Save prediction to log

#### Gallery
- `GET /tracker/gallery/` - Food photo gallery
- `GET /tracker/gallery/<id>/` - Image detail view

#### Analytics
- `GET /tracker/analytics/` - Analytics dashboard
- `GET /tracker/analytics/weekly/` - Weekly data (JSON)
- `GET /tracker/analytics/monthly/` - Monthly data (JSON)

---

## 👨‍💻 Development

### Project Architecture

#### Design Principles
- **DRY (Don't Repeat Yourself):** Business logic in `services/` modules
- **KISS (Keep It Simple, Stupid):** Simple, readable code structure
- **Separation of Concerns:** Views handle requests, services handle logic
- **Mobile-First:** Responsive design prioritizing mobile experience

#### Key Design Patterns

**1. Service Layer Pattern**
```python
# views/food_logging.py (thin view)
from ..services.calculator_service import calculate_nutrition_percentage

def dashboard(request):
    log = get_daily_log(request.user)
    percentage = calculate_nutrition_percentage(log.total_calories, log.calorie_goal)
    return render(request, 'dashboard.html', {'percentage': percentage})
```

**2. Model Property Pattern**
```python
# models.py
class DailyLog(models.Model):
    total_calories = models.FloatField()
    calorie_goal = models.IntegerField()
    
    @property
    def calorie_percentage(self):
        if self.calorie_goal and self.calorie_goal > 0:
            return min(100, (self.total_calories / self.calorie_goal) * 100)
        return None
```

**3. Signal Pattern (Auto Profile Creation)**
```python
# accounts/models.py
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
```

### Adding New Features

#### 1. Create a New Model
```bash
# Edit pycalorie/models.py
python manage.py makemigrations
python manage.py migrate
```

#### 2. Register in Admin
```python
# pycalorie/admin.py
from .models import YourNewModel

@admin.register(YourNewModel)
class YourNewModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
```

#### 3. Create Service Functions
```python
# pycalorie/services/your_service.py
def your_business_logic(param1, param2):
    """
    Document what this does.
    """
    # Logic here
    return result
```

#### 4. Create Views
```python
# pycalorie/views/your_views.py
from django.shortcuts import render
from ..services.your_service import your_business_logic

def your_view(request):
    result = your_business_logic(param1, param2)
    return render(request, 'your_template.html', {'result': result})
```

#### 5. Add URL Routes
```python
# pycalorie/urls.py
from .views import your_views

urlpatterns = [
    path('your-route/', your_views.your_view, name='your_view'),
]
```

### Custom Management Commands

Create commands in `pycalorie/management/commands/`:

```python
# pycalorie/management/commands/seed_foods.py
from django.core.management.base import BaseCommand
from pycalorie.models import Food

class Command(BaseCommand):
    help = 'Seed food database with common foods'
    
    def handle(self, *args, **options):
        foods = [
            {'name': 'Apple', 'calories_per_100g': 52, ...},
            {'name': 'Banana', 'calories_per_100g': 89, ...},
        ]
        
        for food_data in foods:
            Food.objects.get_or_create(**food_data)
        
        self.stdout.write(self.style.SUCCESS('✓ Foods seeded successfully'))
```

Run with:
```bash
python manage.py seed_foods
```

### Testing

#### Run All Tests
```bash
python manage.py test
```

#### Test Specific App
```bash
python manage.py test pycalorie
python manage.py test accounts
```

#### Test Coverage
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Opens in browser
```

### Code Style

Follow PEP 8 guidelines:
```bash
pip install flake8 black

# Check code style
flake8 .

# Auto-format code
black .
```

---

## 🚢 Deployment

### Docker Deployment

#### Build Image
```bash
docker build -t pycalorie:latest .
```

#### Run with Docker Compose
```bash
# Edit docker-compose.yml with your settings
docker-compose up -d
```

#### Access Application
```
http://localhost:8000
```

### Heroku Deployment

```bash
# Install Heroku CLI
heroku login
heroku create your-app-name

# Set environment variables
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key
heroku config:set GOOGLE_API_KEY=your-google-api-key

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Render.com Deployment

1. Create account at [Render.com](https://render.com/)
2. Create **New Web Service**
3. Connect GitHub repository
4. Configure:
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn core.wsgi:application`
5. Add environment variables in dashboard
6. Deploy!

### VPS Deployment (Ubuntu/Nginx)

#### 1. Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3 python3-pip python3-venv nginx postgresql

# Create user
sudo adduser pycalorie
sudo usermod -aG sudo pycalorie
```

#### 2. Clone & Setup
```bash
su - pycalorie
git clone https://github.com/deJames-13/pycalorie.git
cd pycalorie

# Virtual environment
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

# Environment
cp env.sample .env
nano .env  # Edit with production settings
```

#### 3. Database Setup (PostgreSQL)
```bash
sudo -u postgres psql

CREATE DATABASE pycalorie_db;
CREATE USER pycalorie_user WITH PASSWORD 'secure_password';
ALTER ROLE pycalorie_user SET client_encoding TO 'utf8';
ALTER ROLE pycalorie_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE pycalorie_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE pycalorie_db TO pycalorie_user;
\q
```

#### 4. Django Setup
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

#### 5. Gunicorn Service
```bash
sudo nano /etc/systemd/system/pycalorie.service
```

```ini
[Unit]
Description=PyCalorie Gunicorn Daemon
After=network.target

[Service]
User=pycalorie
Group=www-data
WorkingDirectory=/home/pycalorie/pycalorie
ExecStart=/home/pycalorie/pycalorie/env/bin/gunicorn \
          --workers 3 \
          --bind unix:/home/pycalorie/pycalorie/pycalorie.sock \
          core.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl start pycalorie
sudo systemctl enable pycalorie
```

#### 6. Nginx Configuration
```bash
sudo nano /etc/nginx/sites-available/pycalorie
```

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /home/pycalorie/pycalorie;
    }
    
    location /media/ {
        root /home/pycalorie/pycalorie;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/pycalorie/pycalorie/pycalorie.sock;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/pycalorie /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

#### 7. SSL with Let's Encrypt
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## 📚 Additional Resources

### Documentation
- [Django Documentation](https://docs.djangoproject.com/)
- [Google GenAI Documentation](https://ai.google.dev/docs)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/)
- [Chart.js Documentation](https://www.chartjs.org/docs/)

### UI Theme
The UI is built with [Pixel Lite Template](https://app-generator.dev/docs/products/django/pixel/index.html), featuring:
- Modern Bootstrap 5 Design
- Fully Responsive Layout
- 100+ UI Components
- Dark Mode Ready
- [Theme Documentation](https://app-generator.dev/docs/products/django-libs/theme-pixel.html)

### Nutritional Data Resources
- [USDA FoodData Central](https://fdc.nal.usda.gov/)
- [Nutritionix API](https://www.nutritionix.com/business/api)
- [Open Food Facts](https://world.openfoodfacts.org/)

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork the repository**
2. **Create a feature branch:** `git checkout -b feature/amazing-feature`
3. **Commit changes:** `git commit -m 'Add amazing feature'`
4. **Push to branch:** `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Contribution Guidelines
- Follow PEP 8 style guide
- Add tests for new features
- Update documentation
- Keep commits atomic and descriptive
- Ensure all tests pass before submitting PR

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

---

## 👥 Authors

- **deJames** - *Initial work* - [GitHub](https://github.com/deJames-13)

---

## 🙏 Acknowledgments

- **AppSeed** for the Pixel Lite theme
- **Google** for the Gemini AI API
- **Django** community for excellent documentation
- **Bootstrap** team for responsive framework
- All contributors and testers

---

## 📞 Support

For issues, questions, or suggestions:

- **GitHub Issues:** [Report a bug](https://github.com/deJames-13/pycalorie/issues)
- **Email:** support@pycalorie.com
- **Documentation:** [Full Docs](https://github.com/deJames-13/pycalorie/wiki)

---

**Made with ❤️ and 🔥 by the PyCalorie Team**
