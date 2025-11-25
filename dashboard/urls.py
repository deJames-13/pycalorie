from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='index'),
    path('food-log/', views.food_log, name='food_log'),
    path('calorie-predict/', views.calorie_predict, name='calorie_predict'),
    path('calorie-predict/<int:prediction_id>/', views.calorie_predict_result, name='calorie_predict_result'),
    path('reports/', views.reports, name='reports'),
    path('profile/', views.profile, name='profile'),
]

