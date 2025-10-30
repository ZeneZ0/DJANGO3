# configurator/admin.py
from django.contrib import admin
from .models import ComponentType, Manufacturer, Component, PCConfiguration, BuildRequest

@admin.register(ComponentType)
class ComponentTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'website')
    list_filter = ('country',)
    search_fields = ('name', 'country')
    ordering = ('name',)

@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'component_type', 'manufacturer', 'price', 'in_stock')
    list_filter = ('component_type', 'manufacturer', 'in_stock')
    search_fields = ('name', 'description')
    list_editable = ('price', 'in_stock')
    ordering = ('name',)
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'component_type', 'manufacturer', 'price')
        }),
        ('Дополнительная информация', {
            'fields': ('description', 'specifications', 'in_stock'),
            'classes': ('collapse',)
        }),
    )

@admin.register(PCConfiguration)
class PCConfigurationAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_price', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')
    ordering = ('-created_at',)
    
    # Поля только для чтения в форме редактирования
    readonly_fields = ('total_price', 'created_at')
    
    # Группировка полей в форме
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'total_price')
        }),
        ('Компоненты', {
            'fields': (
                'cpu', 'gpu', 'motherboard', 
                'ram', 'storage', 'power_supply', 'case'
            )
        }),
    )

@admin.register(BuildRequest)
class BuildRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'configuration', 'status', 'budget', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'configuration__name', 'notes')
    list_editable = ('status',)
    ordering = ('-created_at',)
    
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'configuration', 'status', 'budget')
        }),
        ('Дополнительно', {
            'fields': ('notes', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )