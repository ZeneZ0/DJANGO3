# configurator/api.py
from rest_framework import generics
from django.contrib.auth.models import User
from .models import ComponentType, Manufacturer, Component, PCConfiguration, BuildRequest
from .serializers import (
    ComponentTypeSerializer, ManufacturerSerializer, ComponentSerializer,
    PCConfigurationSerializer, BuildRequestSerializer, UserSerializer
)

# ComponentType API (без привязки к пользователю)
class ComponentTypeList(generics.ListCreateAPIView):
    queryset = ComponentType.objects.all()
    serializer_class = ComponentTypeSerializer

class ComponentTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ComponentType.objects.all()
    serializer_class = ComponentTypeSerializer

# Manufacturer API с фильтрацией по пользователю
class ManufacturerList(generics.ListCreateAPIView):
    serializer_class = ManufacturerSerializer
    
    def get_queryset(self):
        qs = Manufacturer.objects.all()
        
        # Фильтруем по текущему пользователю согласно методичке
        if not self.request.user.is_superuser:
            qs = qs.filter(user=self.request.user)
        
        # Фильтр по пользователю для суперюзера
        user_id = self.request.query_params.get('user_id')
        if self.request.user.is_superuser and user_id:
            qs = qs.filter(user_id=user_id)
            
        return qs

class ManufacturerDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ManufacturerSerializer
    
    def get_queryset(self):
        qs = Manufacturer.objects.all()
        
        # Фильтруем по текущему пользователю согласно методичке
        if not self.request.user.is_superuser:
            qs = qs.filter(user=self.request.user)
            
        return qs

# Component API с фильтрацией по пользователю
class ComponentList(generics.ListCreateAPIView):
    serializer_class = ComponentSerializer
    
    def get_queryset(self):
        qs = Component.objects.all()
        
        # Фильтруем по текущему пользователю согласно методичке
        if not self.request.user.is_superuser:
            qs = qs.filter(user=self.request.user)
        
        # Фильтр по пользователю для суперюзера
        user_id = self.request.query_params.get('user_id')
        if self.request.user.is_superuser and user_id:
            qs = qs.filter(user_id=user_id)
            
        return qs

class ComponentDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ComponentSerializer
    
    def get_queryset(self):
        qs = Component.objects.all()
        
        # Фильтруем по текущему пользователю согласно методичке
        if not self.request.user.is_superuser:
            qs = qs.filter(user=self.request.user)
            
        return qs

# PCConfiguration API с фильтрацией по пользователю
class PCConfigurationList(generics.ListCreateAPIView):
    serializer_class = PCConfigurationSerializer
    
    def get_queryset(self):
        qs = PCConfiguration.objects.all()
        
        # Фильтруем по текущему пользователю согласно методичке
        if not self.request.user.is_superuser:
            qs = qs.filter(user=self.request.user)
        
        # Фильтр по пользователю для суперюзера
        user_id = self.request.query_params.get('user_id')
        if self.request.user.is_superuser and user_id:
            qs = qs.filter(user_id=user_id)
            
        return qs

class PCConfigurationDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PCConfigurationSerializer
    
    def get_queryset(self):
        qs = PCConfiguration.objects.all()
        
        # Фильтруем по текущему пользователю согласно методичке
        if not self.request.user.is_superuser:
            qs = qs.filter(user=self.request.user)
            
        return qs

# BuildRequest API (уже привязан к пользователю)
class BuildRequestList(generics.ListCreateAPIView):
    serializer_class = BuildRequestSerializer
    
    def get_queryset(self):
        qs = BuildRequest.objects.all()
        
        # Фильтруем по текущему пользователю согласно методичке
        if not self.request.user.is_superuser:
            qs = qs.filter(user=self.request.user)
        
        # Фильтр по пользователю для суперюзера
        user_id = self.request.query_params.get('user_id')
        if self.request.user.is_superuser and user_id:
            qs = qs.filter(user_id=user_id)
            
        return qs

class BuildRequestDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BuildRequestSerializer
    
    def get_queryset(self):
        qs = BuildRequest.objects.all()
        
        # Фильтруем по текущему пользователю согласно методичке
        if not self.request.user.is_superuser:
            qs = qs.filter(user=self.request.user)
            
        return qs

# User API
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer