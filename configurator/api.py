# configurator/api.py
from rest_framework import generics
from django.contrib.auth.models import User
from .models import ComponentType, Manufacturer, Component, PCConfiguration, BuildRequest
from .serializers import (
    ComponentTypeSerializer, ManufacturerSerializer, ComponentSerializer,
    PCConfigurationSerializer, BuildRequestSerializer, UserSerializer
)

# ComponentType API
class ComponentTypeList(generics.ListCreateAPIView):
    queryset = ComponentType.objects.all()
    serializer_class = ComponentTypeSerializer

class ComponentTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ComponentType.objects.all()
    serializer_class = ComponentTypeSerializer

# Manufacturer API
class ManufacturerList(generics.ListCreateAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer

class ManufacturerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer

# Component API
class ComponentList(generics.ListCreateAPIView):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer

class ComponentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer

# PCConfiguration API
class PCConfigurationList(generics.ListCreateAPIView):
    queryset = PCConfiguration.objects.all()
    serializer_class = PCConfigurationSerializer

class PCConfigurationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PCConfiguration.objects.all()
    serializer_class = PCConfigurationSerializer

# BuildRequest API
class BuildRequestList(generics.ListCreateAPIView):
    queryset = BuildRequest.objects.all()
    serializer_class = BuildRequestSerializer

class BuildRequestDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BuildRequest.objects.all()
    serializer_class = BuildRequestSerializer

# User API
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer