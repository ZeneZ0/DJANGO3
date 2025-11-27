# configurator/urls.py
from django.urls import path
from . import views  # для HTML views
from .api import (   # для API views
    ComponentTypeList, ComponentTypeDetail,
    ManufacturerList, ManufacturerDetail, 
    ComponentList, ComponentDetail,
    PCConfigurationList, PCConfigurationDetail,
    BuildRequestList, BuildRequestDetail,
    UserList
)

urlpatterns = [
    # HTML pages
    path('', views.home_page, name='home'),
    path('about/', views.about_page, name='about'),
    
    # API URLs
    path('component-types/', ComponentTypeList.as_view(), name='componenttype-list'),
    path('component-types/<int:pk>/', ComponentTypeDetail.as_view(), name='componenttype-detail'),
    
    path('manufacturers/', ManufacturerList.as_view(), name='manufacturer-list'),
    path('manufacturers/<int:pk>/', ManufacturerDetail.as_view(), name='manufacturer-detail'),
    
    path('components/', ComponentList.as_view(), name='component-list'),
    path('components/<int:pk>/', ComponentDetail.as_view(), name='component-detail'),
    
    path('configurations/', PCConfigurationList.as_view(), name='pcconfiguration-list'),
    path('configurations/<int:pk>/', PCConfigurationDetail.as_view(), name='pcconfiguration-detail'),
    
    path('build-requests/', BuildRequestList.as_view(), name='buildrequest-list'),
    path('build-requests/<int:pk>/', BuildRequestDetail.as_view(), name='buildrequest-detail'),
    
    # Endpoint для пользователей
    path('users/', UserList.as_view(), name='user-list'),
]