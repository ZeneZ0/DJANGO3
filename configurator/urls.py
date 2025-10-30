# configurator/urls.py
from django.urls import path
from . import views
from .api import *

urlpatterns = [
    # HTML pages
    path('', views.home_page, name='home'),
    path('about/', views.about_page, name='about'),
    
    # API URLs
    path('component-types/', ComponentTypeList.as_view()),
    path('component-types/<int:pk>/', ComponentTypeDetail.as_view()),
    
    path('manufacturers/', ManufacturerList.as_view()),
    path('manufacturers/<int:pk>/', ManufacturerDetail.as_view()),
    
    path('components/', ComponentList.as_view()),
    path('components/<int:pk>/', ComponentDetail.as_view()),
    
    path('configurations/', PCConfigurationList.as_view()),
    path('configurations/<int:pk>/', PCConfigurationDetail.as_view()),
    
    path('build-requests/', BuildRequestList.as_view()),
    path('build-requests/<int:pk>/', BuildRequestDetail.as_view()),
]