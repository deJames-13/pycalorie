"""
URL configuration for pycalorie app.
Handles dashboard, food logging, AI predictions, and analytics.
"""
from django.urls import path
from . import views

app_name = 'pycalorie'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Food logging
    path('log/', views.food_log, name='food_log'),
    path('log/edit/<int:entry_id>/', views.edit_food_entry, name='edit_food_entry'),
    path('log/delete/<int:entry_id>/', views.delete_food_entry, name='delete_food_entry'),
    path('log/history/', views.food_log_history, name='food_log_history'),
    
    # Food search (AJAX)
    path('food/search/', views.search_food, name='search_food'),
    path('food/create/', views.create_food, name='create_food'),
    
    # Water tracking
    path('water/add/', views.add_water, name='add_water'),
    
    # AI Calorie Prediction
    path('predict/text/', views.predict_from_text, name='predict_from_text'),
    path('predict/image/', views.predict_from_image, name='predict_from_image'),
    path('predict/result/<int:prediction_id>/', views.prediction_result, name='prediction_result'),
    path('predict/save/<int:prediction_id>/', views.save_prediction_to_log, name='save_prediction_to_log'),
    
    # Image Gallery
    path('gallery/', views.image_gallery, name='image_gallery'),
    path('gallery/<int:image_id>/', views.image_detail, name='image_detail'),
    
    # Analytics
    path('analytics/', views.analytics, name='analytics'),
    path('analytics/weekly/', views.weekly_analytics, name='weekly_analytics'),
    path('analytics/monthly/', views.monthly_analytics, name='monthly_analytics'),
]
