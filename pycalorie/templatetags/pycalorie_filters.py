"""Custom template filters for PyCalorie."""
from django import template

register = template.Library()

@register.filter(name='percentage')
def percentage(value, decimal_places=0):
    """
    Convert a decimal confidence value (0.0-1.0) to percentage.
    
    Usage: {{ 0.85|percentage }} -> "85"
           {{ 0.85|percentage:1 }} -> "85.0"
    """
    try:
        return f"{float(value) * 100:.{decimal_places}f}"
    except (ValueError, TypeError):
        return "0"

@register.filter(name='multiply')
def multiply(value, arg):
    """
    Multiply the value by the argument.
    
    Usage: {{ value|multiply:100 }}
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0
