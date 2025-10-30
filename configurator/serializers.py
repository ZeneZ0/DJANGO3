# configurator/serializers.py
from rest_framework import serializers
from .models import ComponentType, Manufacturer, Component, PCConfiguration, BuildRequest

class ComponentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComponentType
        fields = ['id', 'name', 'description']

class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ['id', 'name', 'country', 'website']

class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = ['id', 'name', 'component_type', 'manufacturer', 'price', 'description', 'specifications', 'in_stock', 'created_at']

class PCConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PCConfiguration
        fields = ['id', 'name', 'description', 'cpu', 'gpu', 'motherboard', 'ram', 'storage', 'power_supply', 'case', 'total_price', 'created_at']

class BuildRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildRequest
        fields = ['id', 'user', 'configuration', 'status', 'budget', 'notes', 'created_at', 'updated_at']