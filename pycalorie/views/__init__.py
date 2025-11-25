"""
PyCalorie Views - Modular view structure.
Separation of concerns: dashboard, food logging, AI prediction, analytics.
Profile views are handled by the dashboard app.
"""

# Dashboard views
from .dashboard import dashboard

# Food logging views
from .food_logging import (
    food_log,
    search_food,
    edit_food_entry,
    delete_food_entry,
    food_log_history,
    add_water,
    create_food,
)

# AI prediction views
from .ai_prediction import (
    predict_from_text,
    predict_from_image,
    prediction_result,
    save_prediction_to_log,
    image_gallery,
    image_detail,
)

# Analytics views
from .analytics import (
    analytics,
    weekly_analytics,
    monthly_analytics,
)

__all__ = [
    # Dashboard
    'dashboard',
    
    # Food logging
    'food_log',
    'search_food',
    'edit_food_entry',
    'delete_food_entry',
    'food_log_history',
    'add_water',
    'create_food',
    
    # AI prediction
    'predict_from_text',
    'predict_from_image',
    'prediction_result',
    'save_prediction_to_log',
    'image_gallery',
    'image_detail',
    
    # Analytics
    'analytics',
    'weekly_analytics',
    'monthly_analytics',
]
