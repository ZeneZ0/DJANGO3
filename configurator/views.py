# configurator/views.py
from django.shortcuts import render
from .models import PCConfiguration, Component

def home_page(request):
    recent_configs = PCConfiguration.objects.all().order_by('-created_at')[:5]
    components_count = Component.objects.count()
    
    context = {
        'title': 'Удобный конфигуратор ПК',
        'recent_configs': recent_configs,
        'components_count': components_count,
    }
    return render(request, 'configurator/home.html', context)

def about_page(request):
    return render(request, 'configurator/about.html', {'title': 'О проекте'})