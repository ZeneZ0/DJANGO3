# configurator/models.py
from django.db import models
from django.contrib.auth.models import User

class ComponentType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Тип компонента")
    description = models.TextField(blank=True, verbose_name="Описание типа")
    
    def __str__(self):
        return self.name

class Manufacturer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название производителя")
    country = models.CharField(max_length=50, verbose_name="Страна")
    website = models.URLField(blank=True, verbose_name="Веб-сайт")
    logo = models.ImageField("Логотип", upload_to="manufacturers/", blank=True, null=True)
    
    def __str__(self):
        return self.name

class Component(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    component_type = models.ForeignKey(ComponentType, on_delete=models.CASCADE, verbose_name="Тип компонента")
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, verbose_name="Производитель")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    description = models.TextField(blank=True, verbose_name="Описание")
    specifications = models.JSONField(default=dict, blank=True, verbose_name="Характеристики")
    in_stock = models.BooleanField(default=True, verbose_name="В наличии")
    image = models.ImageField("Изображение", upload_to="components/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.manufacturer} {self.name} ({self.component_type})"

class PCConfiguration(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название конфигурации")
    description = models.TextField(blank=True, verbose_name="Описание конфигурации")
    cpu = models.ForeignKey(Component, on_delete=models.CASCADE, related_name="cpu_configs", verbose_name="Процессор")
    gpu = models.ForeignKey(Component, on_delete=models.CASCADE, related_name="gpu_configs", verbose_name="Видеокарта")
    motherboard = models.ForeignKey(Component, on_delete=models.CASCADE, related_name="motherboard_configs", verbose_name="Материнская плата")
    ram = models.ForeignKey(Component, on_delete=models.CASCADE, related_name="ram_configs", verbose_name="Оперативная память")
    storage = models.ForeignKey(Component, on_delete=models.CASCADE, related_name="storage_configs", verbose_name="Накопитель")
    power_supply = models.ForeignKey(Component, on_delete=models.CASCADE, related_name="psu_configs", verbose_name="Блок питания")
    case = models.ForeignKey(Component, on_delete=models.CASCADE, related_name="case_configs", verbose_name="Корпус")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая стоимость")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        components = [self.cpu, self.gpu, self.motherboard, self.ram, self.storage, self.power_supply, self.case]
        self.total_price = sum(comp.price for comp in components)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class BuildRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('in_progress', 'В работе'),
        ('completed', 'Завершено'),
        ('cancelled', 'Отменено'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    configuration = models.ForeignKey(PCConfiguration, on_delete=models.CASCADE, verbose_name="Конфигурация")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    budget = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Бюджет")
    notes = models.TextField(blank=True, verbose_name="Дополнительные пожелания")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Запрос #{self.id} от {self.user.username}"