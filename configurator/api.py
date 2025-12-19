from rest_framework import generics, permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import ComponentType, Manufacturer, Component, PCConfiguration, BuildRequest
from .serializers import (
    ComponentTypeSerializer, ManufacturerSerializer, ComponentSerializer,
    PCConfigurationSerializer, BuildRequestSerializer, UserSerializer
)
from django.http import HttpResponse, JsonResponse
import pandas as pd
from io import BytesIO
from django.db.models import Q
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
import json
from django.contrib.auth import authenticate, login, logout
import os
from django.conf import settings

# ================ CUSTOM PERMISSIONS ================
class IsAdminOrReadOnly(permissions.BasePermission):
    """Разрешает полный доступ админам, только чтение всем"""
    def has_permission(self, request, view):
        # Разрешаем GET, HEAD, OPTIONS всем
        if request.method in permissions.SAFE_METHODS:
            return True
        # POST, PUT, PATCH, DELETE только админам
        return request.user and (request.user.is_staff or request.user.is_superuser)

class IsOwnerOrAdmin(permissions.BasePermission):
    """Разрешает доступ владельцу или админу"""
    def has_object_permission(self, request, view, obj):
        # Админы могут всё
        if request.user and (request.user.is_staff or request.user.is_superuser):
            return True
        # Проверяем, является ли пользователь владельцем
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return False

# ================ VIEWSETS ================
class ComponentTypeViewSet(viewsets.ModelViewSet):
    queryset = ComponentType.objects.all()
    serializer_class = ComponentTypeSerializer
    permission_classes = [IsAdminOrReadOnly]

class ManufacturerViewSet(viewsets.ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    permission_classes = [IsAdminOrReadOnly]

class ComponentViewSet(viewsets.ModelViewSet):
    queryset = Component.objects.all().order_by('-created_at')
    serializer_class = ComponentSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def get_queryset(self):
        """Показываем все компоненты всем пользователям"""
        queryset = Component.objects.all().select_related('component_type', 'manufacturer')
        
        # Фильтры для экспорта
        if self.action == 'export_excel':
            filters = Q()
            
            name_filter = self.request.query_params.get('name', '')
            if name_filter:
                filters &= Q(name__icontains=name_filter)
            
            component_type_filter = self.request.query_params.get('component_type', '')
            if component_type_filter:
                filters &= Q(component_type_id=component_type_filter)
            
            manufacturer_filter = self.request.query_params.get('manufacturer', '')
            if manufacturer_filter:
                filters &= Q(manufacturer_id=manufacturer_filter)
            
            price_min = self.request.query_params.get('price_min', '')
            if price_min:
                try:
                    filters &= Q(price__gte=float(price_min))
                except:
                    pass
            
            price_max = self.request.query_params.get('price_max', '')
            if price_max:
                try:
                    filters &= Q(price__lte=float(price_max))
                except:
                    pass
            
            in_stock_filter = self.request.query_params.get('in_stock', '')
            if in_stock_filter:
                if in_stock_filter.lower() == 'true':
                    filters &= Q(in_stock=True)
                elif in_stock_filter.lower() == 'false':
                    filters &= Q(in_stock=False)
            
            queryset = queryset.filter(filters)
        
        return queryset
    
    def perform_create(self, serializer):
        """Автоматически сохраняем создателя компонента"""
        serializer.save()
    
    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        """Экспорт компонентов в Excel"""
        try:
            components = self.get_queryset()
            
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
    serializer_class = PCConfigurationSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def get_queryset(self):
        """Показываем все конфигурации всем пользователям"""
        queryset = PCConfiguration.objects.all().select_related(
            'cpu', 'gpu', 'motherboard', 'ram', 'storage', 'power_supply', 'case'
        ).order_by('-created_at')
        
        # Фильтры для экспорта
        if self.action == 'export_excel':
            filters = Q()
            
            name_filter = self.request.query_params.get('name', '')
            if name_filter:
                filters &= Q(name__icontains=name_filter)
            
            price_min = self.request.query_params.get('price_min', '')
            if price_min:
                try:
                    filters &= Q(total_price__gte=float(price_min))
                except:
                    pass
            
            price_max = self.request.query_params.get('price_max', '')
            if price_max:
                try:
                    filters &= Q(total_price__lte=float(price_max))
                except:
                    pass
            
            date_from = self.request.query_params.get('date_from', '')
            if date_from:
                filters &= Q(created_at__gte=date_from)
            
            date_to = self.request.query_params.get('date_to', '')
            if date_to:
                filters &= Q(created_at__lte=date_to)
            
            queryset = queryset.filter(filters)
        
        return queryset
    
    def perform_create(self, serializer):
        """Вычисляем общую стоимость при создании"""
        config = serializer.save()
        config.calculate_total_price()
    
    def perform_update(self, serializer):
        """Вычисляем общую стоимость при обновлении"""
        config = serializer.save()
        config.calculate_total_price()
    
    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        """Экспорт конфигураций в Excel"""
        try:
            configs = self.get_queryset()
            
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
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    
    def get_queryset(self):
        """
        Админы видят все заявки, обычные пользователи - только свои
        """
        user = self.request.user
        
        if user.is_staff or user.is_superuser:
            # Админы видят все
            queryset = BuildRequest.objects.all().select_related('user', 'configuration')
            
            # Фильтр по пользователю для админов
            user_id = self.request.query_params.get('user_id', '')
            if user_id:
                queryset = queryset.filter(user_id=user_id)
        else:
            # Обычные пользователи видят только свои
            queryset = BuildRequest.objects.filter(user=user).select_related('user', 'configuration')
        
        # Дополнительные фильтры для экспорта
        if self.action == 'export_excel':
            filters = Q()
            
            id_filter = self.request.query_params.get('id', '')
            if id_filter:
                filters &= Q(id__icontains=id_filter)
            
            user_name_filter = self.request.query_params.get('user_name', '')
            if user_name_filter:
                filters &= Q(user__username__icontains=user_name_filter)
            
            configuration_name_filter = self.request.query_params.get('configuration_name', '')
            if configuration_name_filter:
                filters &= Q(configuration__name__icontains=configuration_name_filter)
            
            budget_min = self.request.query_params.get('budget_min', '')
            if budget_min:
                try:
                    filters &= Q(budget__gte=float(budget_min))
                except:
                    pass
            
            budget_max = self.request.query_params.get('budget_max', '')
            if budget_max:
                try:
                    filters &= Q(budget__lte=float(budget_max))
                except:
                    pass
            
            status_filter = self.request.query_params.get('status', '')
            if status_filter:
                filters &= Q(status=status_filter)
            
            queryset = queryset.filter(filters)
        
        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):
        """Автоматически привязываем пользователя при создании"""
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        """Экспорт заявок в Excel"""
        try:
            requests = self.get_queryset()
            
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
            return JsonResponse({
                'status': 'ok', 
                'user': {
                    'id': user.id,
                    'username': user.username, 
                    'is_staff': user.is_staff,
                    'is_superuser': user.is_superuser,
                }
            })
        return JsonResponse({'status': 'error', 'message': 'Неверные учетные данные'}, status=401)
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
            'id': request.user.id,
            'username': request.user.username,
            'is_staff': request.user.is_staff,
            'is_superuser': request.user.is_superuser,
        })
    return JsonResponse({'is_authenticated': False})

@ensure_csrf_cookie
@require_http_methods(["GET"])
def dashboard_stats_view(request):
    from django.db.models import Count, Avg, Sum
    
    try:
        requests_qs = BuildRequest.objects.all()
        components_qs = Component.objects.all()
        
        if request.user.is_authenticated:
            if not (request.user.is_staff or request.user.is_superuser):
                requests_qs = requests_qs.filter(user=request.user)
        else:
            requests_qs = BuildRequest.objects.none()
        
        stats = {
            'users_count': User.objects.count() if (request.user.is_staff or request.user.is_superuser) else 0,
            'requests_count': requests_qs.count(),
            'components_count': components_qs.count(),
            'configs_count': PCConfiguration.objects.count(),
            'avg_request_budget': requests_qs.aggregate(Avg('budget'))['budget__avg'] or 0,
            'total_request_budget': requests_qs.aggregate(Sum('budget'))['budget__sum'] or 0,
            'avg_component_price': components_qs.aggregate(Avg('price'))['price__avg'] or 0,
        }
        return JsonResponse(stats)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

class UserList(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer

@ensure_csrf_cookie
@require_http_methods(["GET"])
def check_permissions_view(request):
    """Проверка прав пользователя"""
    if not request.user.is_authenticated:
        return JsonResponse({'is_authenticated': False})
    
    is_admin = request.user.is_staff or request.user.is_superuser
    
    return JsonResponse({
        'is_authenticated': True,
        'is_staff': request.user.is_staff,
        'is_superuser': request.user.is_superuser,
        'is_admin': is_admin,
        'can_manage_components': is_admin,
        'can_manage_configurations': is_admin,
        'can_manage_all_requests': is_admin,
        'can_view_users': is_admin
    })