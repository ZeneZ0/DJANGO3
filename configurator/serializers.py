# configurator/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ComponentType, Manufacturer, Component, PCConfiguration, BuildRequest

class ComponentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComponentType
        fields = ['id', 'name', 'description']

class ManufacturerSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Manufacturer
        fields = ['id', 'name', 'country', 'website', 'logo', 'logo_url', 'user', 'user_name']
    
    def get_logo_url(self, obj):
        if obj.logo:
            return obj.logo.url
        return None
    
    def create(self, validated_data):
        # Автоматически заполняем пользователя из запроса согласно методичке
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class ComponentSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    component_type_name = serializers.CharField(source='component_type.name', read_only=True)
    manufacturer_name = serializers.CharField(source='manufacturer.name', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Component
        fields = [
            'id', 'name', 'component_type', 'component_type_name', 
            'manufacturer', 'manufacturer_name', 'price', 'description',
            'specifications', 'in_stock', 'image', 'image_url', 'user', 'user_name', 'created_at'
        ]
    
    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None
    
    def create(self, validated_data):
        # Автоматически заполняем пользователя из запроса согласно методичке
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class PCConfigurationSerializer(serializers.ModelSerializer):
    cpu_name = serializers.CharField(source='cpu.name', read_only=True)
    gpu_name = serializers.CharField(source='gpu.name', read_only=True)
    motherboard_name = serializers.CharField(source='motherboard.name', read_only=True)
    ram_name = serializers.CharField(source='ram.name', read_only=True)
    storage_name = serializers.CharField(source='storage.name', read_only=True)
    power_supply_name = serializers.CharField(source='power_supply.name', read_only=True)
    case_name = serializers.CharField(source='case.name', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = PCConfiguration
        fields = [
            'id', 'name', 'description', 'cpu', 'cpu_name', 'gpu', 'gpu_name',
            'motherboard', 'motherboard_name', 'ram', 'ram_name', 'storage', 'storage_name',
            'power_supply', 'power_supply_name', 'case', 'case_name', 'total_price', 
            'user', 'user_name', 'created_at'
        ]
        read_only_fields = ['total_price']
    
    def create(self, validated_data):
        # Автоматически заполняем пользователя из запроса согласно методичке
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class BuildRequestSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    configuration_name = serializers.CharField(source='configuration.name', read_only=True)
    
    class Meta:
        model = BuildRequest
        fields = [
            'id', 'user', 'user_name', 'configuration', 'configuration_name',
            'status', 'budget', 'notes', 'created_at', 'updated_at'
        ]
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']