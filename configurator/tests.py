
import pytest
from django.contrib.auth.models import User
from .models import ComponentType, Manufacturer, Component, PCConfiguration, BuildRequest
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestComponentTypeCRUD:
    
    def test_create_component_type(self):
        """Тест на создание типа компонента"""
        client = APIClient()
        data = {'name': 'Процессор', 'description': 'Центральный процессор'}
        response = client.post('/component-types/', data)
        assert response.status_code == 201
        assert ComponentType.objects.count() == 1
        assert ComponentType.objects.get().name == 'Процессор'
    
    def test_read_component_type_list(self):
        """Тест на чтение списка типов компонентов"""
        ComponentType.objects.create(name='Процессор')
        ComponentType.objects.create(name='Видеокарта')
        
        client = APIClient()
        response = client.get('/component-types/')
        
        assert response.status_code == 200
        assert len(response.data) == 2
        assert response.data[0]['name'] == 'Процессор'
        assert response.data[1]['name'] == 'Видеокарта'
    
    def test_read_component_type_detail(self):
        """Тест на чтение деталей типа компонента"""
        component_type = ComponentType.objects.create(name='Процессор')
        
        client = APIClient()
        response = client.get(f'/component-types/{component_type.id}/')
        
        assert response.status_code == 200
        assert response.data['name'] == 'Процессор'
    
    def test_update_component_type(self):
        """Тест на обновление типа компонента"""
        component_type = ComponentType.objects.create(name='Процессор')
        
        client = APIClient()
        data = {'name': 'Центральный процессор', 'description': 'Основной процессор'}
        response = client.put(f'/component-types/{component_type.id}/', data)
        
        assert response.status_code == 200
        component_type.refresh_from_db()
        assert component_type.name == 'Центральный процессор'
    
    def test_delete_component_type(self):
        """Тест на удаление типа компонента"""
        component_type = ComponentType.objects.create(name='Процессор')
        
        client = APIClient()
        response = client.delete(f'/component-types/{component_type.id}/')
        
        assert response.status_code == 204
        assert ComponentType.objects.count() == 0


@pytest.mark.django_db
class TestManufacturerCRUD:
    
    def test_create_manufacturer(self):
        """Тест на создание производителя"""
        client = APIClient()
        data = {'name': 'Intel', 'country': 'USA', 'website': 'https://intel.com'}
        response = client.post('/manufacturers/', data)
        
        assert response.status_code == 201
        assert Manufacturer.objects.count() == 1
        assert Manufacturer.objects.get().name == 'Intel'
    
    def test_read_manufacturer_list(self):
        """Тест на чтение списка производителей"""
        Manufacturer.objects.create(name='Intel', country='USA')
        Manufacturer.objects.create(name='AMD', country='USA')
        
        client = APIClient()
        response = client.get('/manufacturers/')
        
        assert response.status_code == 200
        assert len(response.data) == 2
    
    def test_read_manufacturer_detail(self):
        """Тест на чтение деталей производителя"""
        manufacturer = Manufacturer.objects.create(name='Intel', country='USA')
        
        client = APIClient()
        response = client.get(f'/manufacturers/{manufacturer.id}/')
        
        assert response.status_code == 200
        assert response.data['name'] == 'Intel'
    
    def test_update_manufacturer(self):
        """Тест на обновление производителя"""
        manufacturer = Manufacturer.objects.create(name='Intel', country='USA')
        
        client = APIClient()
        data = {'name': 'Intel Corp', 'country': 'United States', 'website': 'https://intel.com'}
        response = client.put(f'/manufacturers/{manufacturer.id}/', data)
        
        assert response.status_code == 200
        manufacturer.refresh_from_db()
        assert manufacturer.name == 'Intel Corp'
    
    def test_delete_manufacturer(self):
        """Тест на удаление производителя"""
        manufacturer = Manufacturer.objects.create(name='Intel', country='USA')
        
        client = APIClient()
        response = client.delete(f'/manufacturers/{manufacturer.id}/')
        
        assert response.status_code == 204
        assert Manufacturer.objects.count() == 0


@pytest.mark.django_db
class TestComponentCRUD:
    
    def setup_method(self):
        self.component_type = ComponentType.objects.create(name='Процессор')
        self.manufacturer = Manufacturer.objects.create(name='AMD', country='USA')
    
    def test_create_component(self):
        """Тест на создание компонента"""
        client = APIClient()
        data = {
            'name': 'AMD Ryzen 5',
            'component_type': self.component_type.id,
            'manufacturer': self.manufacturer.id,
            'price': '200.00',
            'description': '6-ядерный процессор',
            'specifications': {'ядер': 6, 'потоков': 12}
        }
        response = client.post('/components/', data, format='json')
        
        assert response.status_code == 201
        assert Component.objects.count() == 1
        assert Component.objects.get().name == 'AMD Ryzen 5'
    
    def test_read_component_list(self):
        """Тест на чтение списка компонентов"""
        Component.objects.create(
            name='AMD Ryzen 5',
            component_type=self.component_type,
            manufacturer=self.manufacturer,
            price=200.00
        )
        
        client = APIClient()
        response = client.get('/components/')
        
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['name'] == 'AMD Ryzen 5'
    
    def test_read_component_detail(self):
        """Тест на чтение деталей компонента"""
        component = Component.objects.create(
            name='AMD Ryzen 5',
            component_type=self.component_type,
            manufacturer=self.manufacturer,
            price=200.00
        )
        
        client = APIClient()
        response = client.get(f'/components/{component.id}/')
        
        assert response.status_code == 200
        assert response.data['name'] == 'AMD Ryzen 5'
    
    def test_update_component(self):
        """Тест на обновление компонента"""
        component = Component.objects.create(
            name='AMD Ryzen 5',
            component_type=self.component_type,
            manufacturer=self.manufacturer,
            price=200.00
        )
        
        client = APIClient()
        data = {
            'name': 'AMD Ryzen 5 5600X',
            'component_type': self.component_type.id,
            'manufacturer': self.manufacturer.id,
            'price': '220.00',
            'description': 'Обновленный процессор',
            'specifications': {'ядер': 6, 'потоков': 12}
        }
        response = client.put(f'/components/{component.id}/', data, format='json')
        
        assert response.status_code == 200
        component.refresh_from_db()
        assert component.name == 'AMD Ryzen 5 5600X'
        assert component.price == 220.00
    
    def test_delete_component(self):
        """Тест на удаление компонента"""
        component = Component.objects.create(
            name='AMD Ryzen 5',
            component_type=self.component_type,
            manufacturer=self.manufacturer,
            price=200.00
        )
        
        client = APIClient()
        response = client.delete(f'/components/{component.id}/')
        
        assert response.status_code == 204
        assert Component.objects.count() == 0


@pytest.mark.django_db
class TestPCConfigurationCRUD:
    
    def setup_method(self):
        self.component_type = ComponentType.objects.create(name='Процессор')
        self.manufacturer = Manufacturer.objects.create(name='AMD', country='USA')
        self.component = Component.objects.create(
            name='AMD Ryzen 5',
            component_type=self.component_type,
            manufacturer=self.manufacturer,
            price=200.00
        )
    
    def test_create_configuration(self):
        """Тест на создание конфигурации"""
        client = APIClient()
        data = {
            'name': 'Игровой ПК',
            'description': 'Мощный игровой компьютер',
            'cpu': self.component.id,
            'gpu': self.component.id,
            'motherboard': self.component.id,
            'ram': self.component.id,
            'storage': self.component.id,
            'power_supply': self.component.id,
            'case': self.component.id
        }
        response = client.post('/configurations/', data, format='json')
        
        assert response.status_code == 201
        assert PCConfiguration.objects.count() == 1
        configuration = PCConfiguration.objects.get()
        assert configuration.name == 'Игровой ПК'
        assert configuration.total_price == 1400.00 
    
    def test_read_configuration_list(self):
        """Тест на чтение списка конфигураций"""
        PCConfiguration.objects.create(
            name='Игровой ПК',
            description='Мощный игровой компьютер',
            cpu=self.component,
            gpu=self.component,
            motherboard=self.component,
            ram=self.component,
            storage=self.component,
            power_supply=self.component,
            case=self.component
        )
        
        client = APIClient()
        response = client.get('/configurations/')
        
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['name'] == 'Игровой ПК'
        assert response.data[0]['total_price'] == '1400.00'
    
    def test_read_configuration_detail(self):
        """Тест на чтение деталей конфигурации"""
        config = PCConfiguration.objects.create(
            name='Игровой ПК',
            description='Мощный игровой компьютер',
            cpu=self.component,
            gpu=self.component,
            motherboard=self.component,
            ram=self.component,
            storage=self.component,
            power_supply=self.component,
            case=self.component
        )
        
        client = APIClient()
        response = client.get(f'/configurations/{config.id}/')
        
        assert response.status_code == 200
        assert response.data['name'] == 'Игровой ПК'
        assert response.data['total_price'] == '1400.00'
    
    def test_update_configuration(self):
        """Тест на обновление конфигурации"""
        config = PCConfiguration.objects.create(
            name='Игровой ПК',
            description='Мощный игровой компьютер',
            cpu=self.component,
            gpu=self.component,
            motherboard=self.component,
            ram=self.component,
            storage=self.component,
            power_supply=self.component,
            case=self.component
        )
        
        client = APIClient()
        data = {
            'name': 'Профессиональный ПК',
            'description': 'ПК для профессиональной работы',
            'cpu': self.component.id,
            'gpu': self.component.id,
            'motherboard': self.component.id,
            'ram': self.component.id,
            'storage': self.component.id,
            'power_supply': self.component.id,
            'case': self.component.id
        }
        response = client.put(f'/configurations/{config.id}/', data, format='json')
        
        assert response.status_code == 200
        config.refresh_from_db()
        assert config.name == 'Профессиональный ПК'
        assert config.description == 'ПК для профессиональной работы'
        assert config.total_price == 1400.00
    
    def test_delete_configuration(self):
        """Тест на удаление конфигурации"""
        config = PCConfiguration.objects.create(
            name='Игровой ПК',
            description='Мощный игровой компьютер',
            cpu=self.component,
            gpu=self.component,
            motherboard=self.component,
            ram=self.component,
            storage=self.component,
            power_supply=self.component,
            case=self.component
        )
        
        client = APIClient()
        response = client.delete(f'/configurations/{config.id}/')
        
        assert response.status_code == 204
        assert PCConfiguration.objects.count() == 0


@pytest.mark.django_db
@pytest.mark.django_db
class TestBuildRequestCRUD:
    
    def setup_method(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.component_type = ComponentType.objects.create(name='Процессор')
        self.manufacturer = Manufacturer.objects.create(name='AMD', country='USA')
        self.component = Component.objects.create(
            name='AMD Ryzen 5',
            component_type=self.component_type,
            manufacturer=self.manufacturer,
            price=200.00
        )
        self.configuration = PCConfiguration.objects.create(
            name='Игровой ПК',
            cpu=self.component,
            gpu=self.component,
            motherboard=self.component,
            ram=self.component,
            storage=self.component,
            power_supply=self.component,
            case=self.component
        )
    
    def test_create_build_request(self):
        """Тест на создание запроса на сборку"""
        client = APIClient()
        client.force_authenticate(user=self.user)
        
        data = {
            'user': self.user.id,
            'configuration': self.configuration.id,
            'budget': '1500.00',
            'notes': 'Тестовый запрос'
        }
        response = client.post('/build-requests/', data)
        
        assert response.status_code == 201
        assert BuildRequest.objects.count() == 1
        assert BuildRequest.objects.get().budget == 1500.00
    
    def test_read_build_request_list(self):
        """Тест на чтение списка запросов на сборку"""
        BuildRequest.objects.create(
            user=self.user,
            configuration=self.configuration,
            budget=1500.00
        )
        
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.get('/build-requests/')
        
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['budget'] == '1500.00'
    
    def test_read_build_request_detail(self):
        """Тест на чтение деталей запроса на сборку"""
        build_request = BuildRequest.objects.create(
            user=self.user,
            configuration=self.configuration,
            budget=1500.00
        )
        
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.get(f'/build-requests/{build_request.id}/')
        
        assert response.status_code == 200
        assert response.data['budget'] == '1500.00'
    
    def test_update_build_request(self):
        """Тест на обновление запроса на сборку"""
        build_request = BuildRequest.objects.create(
            user=self.user,
            configuration=self.configuration,
            budget=1500.00
        )
        
        client = APIClient()
        client.force_authenticate(user=self.user)
        data = {
            'user': self.user.id,
            'configuration': self.configuration.id,
            'budget': '2000.00',
            'status': 'in_progress',
            'notes': 'Обновленный запрос'
        }
        response = client.put(f'/build-requests/{build_request.id}/', data)
        
        assert response.status_code == 200
        build_request.refresh_from_db()
        assert build_request.budget == 2000.00
        assert build_request.status == 'in_progress'
    
    def test_delete_build_request(self):
        """Тест на удаление запроса на сборку"""
        build_request = BuildRequest.objects.create(
            user=self.user,
            configuration=self.configuration,
            budget=1500.00
        )
        
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.delete(f'/build-requests/{build_request.id}/')
        
        assert response.status_code == 204
        assert BuildRequest.objects.count() == 0