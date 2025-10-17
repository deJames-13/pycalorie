from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):

    # Page from the theme 
    return render(request, 'pages/index.html')

def theme_docs(request):
    """Render the Django Pixel theme documentation page."""
    return render(request, 'docs/theme.html')
