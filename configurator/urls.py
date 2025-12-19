# configurator/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .api import (
    ComponentViewSet, ManufacturerViewSet, ComponentTypeViewSet,
    PCConfigurationViewSet, BuildRequestViewSet,
    login_view, logout_view, user_info_view, dashboard_stats_view,
    UserList
)

router = DefaultRouter()
router.register(r'component-types', ComponentTypeViewSet, basename='component-type')
router.register(r'manufacturers', ManufacturerViewSet, basename='manufacturer')
router.register(r'components', ComponentViewSet, basename='component')
router.register(r'configurations', PCConfigurationViewSet, basename='configuration')
router.register(r'build-requests', BuildRequestViewSet, basename='build-request')

urlpatterns = [
    path('', views.home_page, name='home'),
    path('about/', views.about_page, name='about'),
    
    # Включаем все маршруты из роутера
    path('', include(router.urls)),
    
    # Пользователи (только для админа)
    path('management/users/', UserList.as_view(), name='user-list'),

    # Auth
    path('auth/login/', login_view, name='login'),
    path('auth/logout/', logout_view, name='logout'),
    path('auth/user/', user_info_view, name='user_info'),
    
    # Stats
    path('stats/', dashboard_stats_view, name='stats'),
]