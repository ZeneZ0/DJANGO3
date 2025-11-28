# configurator/api.py
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .models import ComponentType, Manufacturer, Component, PCConfiguration, BuildRequest
from .serializers import (
    ComponentTypeSerializer, ManufacturerSerializer, ComponentSerializer,
    PCConfigurationSerializer, BuildRequestSerializer, UserSerializer
)

# Публичные API (доступны всем)
class ComponentTypeList(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = ComponentType.objects.all()
    serializer_class = ComponentTypeSerializer

class ManufacturerList(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer

class ComponentList(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer

class PCConfigurationList(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = PCConfiguration.objects.all()
    serializer_class = PCConfigurationSerializer

# API требующие аутентификации
class BuildRequestList(generics.ListCreateAPIView):
    serializer_class = BuildRequestSerializer
    
    def get_queryset(self):
        # Пользователи видят только свои заявки
        if not self.request.user.is_superuser:
            return BuildRequest.objects.filter(user=self.request.user)
        return BuildRequest.objects.all()

class BuildRequestDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BuildRequestSerializer
    
    def get_queryset(self):
        if not self.request.user.is_superuser:
            return BuildRequest.objects.filter(user=self.request.user)
        return BuildRequest.objects.all()

# Админские API (только для суперпользователей)
class ComponentTypeCreate(generics.CreateAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = ComponentType.objects.all()
    serializer_class = ComponentTypeSerializer

class ManufacturerCreate(generics.CreateAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer

class ComponentCreate(generics.CreateAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer

class PCConfigurationCreate(generics.CreateAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = PCConfiguration.objects.all()
    serializer_class = PCConfigurationSerializer

class UserList(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer