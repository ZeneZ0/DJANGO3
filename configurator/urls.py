# configurator/urls.py
from django.urls import path
from . import views
from .api import (
    ComponentTypeList, ManufacturerList, ComponentList, PCConfigurationList,
    BuildRequestList, BuildRequestDetail, UserList,
    ComponentTypeCreate, ManufacturerCreate, ComponentCreate, PCConfigurationCreate
)

urlpatterns = [
    # HTML pages
    path('', views.home_page, name='home'),
    path('about/', views.about_page, name='about'),
    
    # Публичные API (чтение)
    path('component-types/', ComponentTypeList.as_view(), name='componenttype-list'),
    path('manufacturers/', ManufacturerList.as_view(), name='manufacturer-list'),
    path('components/', ComponentList.as_view(), name='component-list'),
    path('configurations/', PCConfigurationList.as_view(), name='pcconfiguration-list'),
    
    # API для заявок (требуют аутентификации)
    path('build-requests/', BuildRequestList.as_view(), name='buildrequest-list'),
    path('build-requests/<int:pk>/', BuildRequestDetail.as_view(), name='buildrequest-detail'),
    
    # Админские API (создание)
    path('admin/component-types/', ComponentTypeCreate.as_view(), name='componenttype-create'),
    path('admin/manufacturers/', ManufacturerCreate.as_view(), name='manufacturer-create'),
    path('admin/components/', ComponentCreate.as_view(), name='component-create'),
    path('admin/configurations/', PCConfigurationCreate.as_view(), name='pcconfiguration-create'),
    
    # Пользователи (только для админа)
    path('admin/users/', UserList.as_view(), name='user-list'),
]