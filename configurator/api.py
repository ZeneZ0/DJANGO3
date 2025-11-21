# configurator/api.py
from rest_framework import generics
from .models import ComponentType, Manufacturer, Component, PCConfiguration, BuildRequest
from .serializers import ComponentTypeSerializer, ManufacturerSerializer, ComponentSerializer, PCConfigurationSerializer, BuildRequestSerializer
from django.contrib.auth.models import User
from .serializers import UserSerializer

class ComponentTypeList(generics.ListCreateAPIView):
    queryset = ComponentType.objects.all()
    serializer_class = ComponentTypeSerializer

class ComponentTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ComponentType.objects.all()
    serializer_class = ComponentTypeSerializer

class ManufacturerList(generics.ListCreateAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer

class ManufacturerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer

class ComponentList(generics.ListCreateAPIView):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer

class ComponentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer

class PCConfigurationList(generics.ListCreateAPIView):
    queryset = PCConfiguration.objects.all()
    serializer_class = PCConfigurationSerializer

class PCConfigurationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PCConfiguration.objects.all()
    serializer_class = PCConfigurationSerializer

class BuildRequestList(generics.ListCreateAPIView):
    queryset = BuildRequest.objects.all()
    serializer_class = BuildRequestSerializer

class BuildRequestDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BuildRequest.objects.all()
    serializer_class = BuildRequestSerializer

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer