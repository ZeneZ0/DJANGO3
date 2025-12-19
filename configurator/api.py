# configurator/api.py
from rest_framework import generics, permissions, viewsets
from django.contrib.auth.models import User
from .models import ComponentType, Manufacturer, Component, PCConfiguration, BuildRequest
from .serializers import (
    ComponentTypeSerializer, ManufacturerSerializer, ComponentSerializer,
    PCConfigurationSerializer, BuildRequestSerializer, UserSerializer
)
from rest_framework.decorators import action
from django.http import HttpResponse, JsonResponse
import pandas as pd
from io import BytesIO
from django.db.models import Q
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
import json
from django.contrib.auth import authenticate, login, logout

# ================ VIEWSETS ================
class ComponentTypeViewSet(viewsets.ModelViewSet):
    queryset = ComponentType.objects.all()
    serializer_class = ComponentTypeSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

class ManufacturerViewSet(viewsets.ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

class ComponentViewSet(viewsets.ModelViewSet):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
    
    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        """Экспорт компонентов в Excel с фильтрацией"""
        try:
            # Применяем фильтры
            filters = Q()
            
            name_filter = request.query_params.get('name')
            if name_filter:
                filters &= Q(name__icontains=name_filter)
            
            component_type_filter = request.query_params.get('component_type')
            if component_type_filter:
                filters &= Q(component_type_id=component_type_filter)
            
            manufacturer_filter = request.query_params.get('manufacturer')
            if manufacturer_filter:
                filters &= Q(manufacturer_id=manufacturer_filter)
            
            price_min = request.query_params.get('price_min')
            if price_min:
                filters &= Q(price__gte=float(price_min))
            
            price_max = request.query_params.get('price_max')
            if price_max:
                filters &= Q(price__lte=float(price_max))
            
            in_stock_filter = request.query_params.get('in_stock')
            if in_stock_filter:
                filters &= Q(in_stock=(in_stock_filter.lower() == 'true'))
            
            # Получаем данные с фильтрами
            components = Component.objects.filter(filters).select_related('component_type', 'manufacturer')
            
            # Подготавливаем данные для Excel
            data = []
            for comp in components:
                data.append({
                    'ID': comp.id,
                    'Название': comp.name,
                    'Тип': comp.component_type.name if comp.component_type else '',
                    'Производитель': comp.manufacturer.name if comp.manufacturer else '',
                    'Цена ($)': float(comp.price) if comp.price else 0,
                    'В наличии': 'Да' if comp.in_stock else 'Нет',
                    'Описание': comp.description or '',
                    'Дата создания': comp.created_at.strftime('%Y-%m-%d %H:%M') if comp.created_at else ''
                })
            
            # Создаем DataFrame
            df = pd.DataFrame(data)
            
            # Создаем Excel файл в памяти
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Компоненты')
                worksheet = writer.sheets['Компоненты']
                
                # Настраиваем ширину колонок
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
            
            # Формируем ответ
            output.seek(0)
            response = HttpResponse(
                output.read(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = f'attachment; filename="components_{timezone.now().date()}.xlsx"'
            return response
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class PCConfigurationViewSet(viewsets.ModelViewSet):
    queryset = PCConfiguration.objects.all()
    serializer_class = PCConfigurationSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
    
    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        """Экспорт конфигураций в Excel с фильтрацией"""
        try:
            # Применяем фильтры
            filters = Q()
            
            name_filter = request.query_params.get('name')
            if name_filter:
                filters &= Q(name__icontains=name_filter)
            
            price_min = request.query_params.get('price_min')
            if price_min:
                filters &= Q(total_price__gte=float(price_min))
            
            price_max = request.query_params.get('price_max')
            if price_max:
                filters &= Q(total_price__lte=float(price_max))
            
            date_from = request.query_params.get('date_from')
            if date_from:
                filters &= Q(created_at__gte=date_from)
            
            date_to = request.query_params.get('date_to')
            if date_to:
                filters &= Q(created_at__lte=date_to)
            
            # Получаем данные с фильтрами
            configs = PCConfiguration.objects.filter(filters).select_related(
                'cpu', 'gpu', 'motherboard', 'ram', 'storage', 'power_supply', 'case'
            )
            
            # Подготавливаем данные для Excel
            data = []
            for config in configs:
                data.append({
                    'ID': config.id,
                    'Название': config.name,
                    'Процессор': config.cpu.name if config.cpu else '',
                    'Видеокарта': config.gpu.name if config.gpu else '',
                    'Материнская плата': config.motherboard.name if config.motherboard else '',
                    'Оперативная память': config.ram.name if config.ram else '',
                    'Накопитель': config.storage.name if config.storage else '',
                    'Блок питания': config.power_supply.name if config.power_supply else '',
                    'Корпус': config.case.name if config.case else '',
                    'Общая стоимость ($)': float(config.total_price) if config.total_price else 0,
                    'Описание': config.description or '',
                    'Дата создания': config.created_at.strftime('%Y-%m-%d %H:%M') if config.created_at else ''
                })
            
            # Создаем DataFrame
            df = pd.DataFrame(data)
            
            # Создаем Excel файл в памяти
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Конфигурации')
                worksheet = writer.sheets['Конфигурации']
                
                # Настраиваем ширину колонок
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
            
            # Формируем ответ
            output.seek(0)
            response = HttpResponse(
                output.read(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = f'attachment; filename="configurations_{timezone.now().date()}.xlsx"'
            return response
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class BuildRequestViewSet(viewsets.ModelViewSet):
    serializer_class = BuildRequestSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        qs = BuildRequest.objects.all()
        
        if self.request.user.is_superuser:
            user_id = self.request.query_params.get('user_id')
            if user_id:
                qs = qs.filter(user_id=user_id)
        else:
            qs = qs.filter(user=self.request.user)
            
        return qs
    
    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        """Экспорт заявок в Excel с фильтрацией"""
        try:
            # Базовые фильтры из get_queryset
            filters = Q()
            
            if not request.user.is_superuser:
                filters &= Q(user=request.user)
            else:
                user_id = request.query_params.get('user_id')
                if user_id:
                    filters &= Q(user_id=user_id)
            
            # Дополнительные фильтры
            id_filter = request.query_params.get('id')
            if id_filter:
                filters &= Q(id__icontains=id_filter)
            
            user_name_filter = request.query_params.get('user_name')
            if user_name_filter:
                filters &= Q(user__username__icontains=user_name_filter)
            
            configuration_name_filter = request.query_params.get('configuration_name')
            if configuration_name_filter:
                filters &= Q(configuration__name__icontains=configuration_name_filter)
            
            budget_min = request.query_params.get('budget_min')
            if budget_min:
                filters &= Q(budget__gte=float(budget_min))
            
            budget_max = request.query_params.get('budget_max')
            if budget_max:
                filters &= Q(budget__lte=float(budget_max))
            
            status_filter = request.query_params.get('status')
            if status_filter:
                filters &= Q(status=status_filter)
            
            # Получаем данные с фильтрами
            requests = BuildRequest.objects.filter(filters).select_related('user', 'configuration')
            
            # Подготавливаем данные для Excel
            data = []
            for req in requests:
                data.append({
                    'ID': req.id,
                    'Пользователь': req.user.username if req.user else '',
                    'Конфигурация': req.configuration.name if req.configuration else '',
                    'Бюджет ($)': float(req.budget) if req.budget else 0,
                    'Статус': req.get_status_display() if req.status else '',
                    'Пожелания': req.notes or '',
                    'Дата создания': req.created_at.strftime('%Y-%m-%d %H:%M') if req.created_at else '',
                    'Дата обновления': req.updated_at.strftime('%Y-%m-%d %H:%M') if req.updated_at else ''
                })
            
            # Создаем DataFrame
            df = pd.DataFrame(data)
            
            # Создаем Excel файл в памяти
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Заявки')
                worksheet = writer.sheets['Заявки']
                
                # Настраиваем ширину колонок
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
            
            # Формируем ответ
            output.seek(0)
            response = HttpResponse(
                output.read(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = f'attachment; filename="requests_{timezone.now().date()}.xlsx"'
            return response
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

# ================ AUTH VIEWS ================
@ensure_csrf_cookie
@require_http_methods(["POST"])
def login_view(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 'ok', 'user': {
                'username': user.username, 
                'is_superuser': user.is_superuser,
                'id': user.id
            }})
        return JsonResponse({'status': 'error', 'message': 'Invalid credentials'}, status=401)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["POST"])
def logout_view(request):
    logout(request)
    return JsonResponse({'status': 'ok'})

@ensure_csrf_cookie
@require_http_methods(["GET"])
def user_info_view(request):
    if request.user.is_authenticated:
        return JsonResponse({
            'is_authenticated': True,
            'username': request.user.username,
            'is_superuser': request.user.is_superuser,
            'id': request.user.id
        })
    return JsonResponse({'is_authenticated': False})

@ensure_csrf_cookie
@require_http_methods(["GET"])
def dashboard_stats_view(request):
    from django.db.models import Count, Avg
    
    try:
        requests_qs = BuildRequest.objects.all()
        components_qs = Component.objects.all()
        
        if request.user.is_authenticated:
            if not request.user.is_superuser:
                requests_qs = requests_qs.filter(user=request.user)
        else:
            requests_qs = BuildRequest.objects.none()
        
        stats = {
            'users_count': User.objects.count() if request.user.is_superuser else 0,
            'requests_count': requests_qs.count(),
            'components_count': components_qs.count(),
            'configs_count': PCConfiguration.objects.count(),
            'avg_request_budget': requests_qs.aggregate(Avg('budget'))['budget__avg'] or 0,
            'avg_component_price': components_qs.aggregate(Avg('price'))['price__avg'] or 0,
        }
        return JsonResponse(stats)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

class UserList(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer