<!-- site_back/src/views/PCConfigurationsView.vue -->
<template>
  <div class="configurations-view">
    <div class="container mt-4">
      <h1 class="text-center mb-4">🖥️ Управление конфигурациями ПК</h1>
      
      <div class="currency-note alert alert-info">
        💰 Все цены в долларах США ($)
      </div>

      <!-- Уведомления -->
      <div v-if="notification.message" 
           :class="['alert', `alert-${notification.type}`, 'alert-dismissible', 'fade', 'show']" 
           role="alert">
        {{ notification.message }}
        <button type="button" class="btn-close" @click="clearNotification"></button>
      </div>

      <!-- Форма добавления/редактирования -->
      <div class="card mb-4">
        <div class="card-header">
          <h5 class="card-title mb-0">
            {{ isEditing ? '✏️ Редактирование конфигурации' : '➕ Добавить новую конфигурацию' }}
          </h5>
        </div>
        <div class="card-body">
          <form @submit.prevent="isEditing ? updateItem() : createItem()">
            <div class="row g-3">
              <div class="col-md-8">
                <label class="form-label">Название конфигурации *</label>
                <input v-model="formData.name" type="text" class="form-control" required>
              </div>
              <div class="col-12">
                <label class="form-label">Описание</label>
                <textarea v-model="formData.description" class="form-control" rows="2" 
                         placeholder="Описание конфигурации..."></textarea>
              </div>
              
              <!-- Выбор компонентов -->
              <div class="col-md-6" v-for="componentType in componentTypes" :key="componentType.id">
                <label class="form-label">{{ componentType.name }} *</label>
                <select v-model="formData[getComponentField(componentType.name)]" class="form-select" required>
                  <option value="">Выберите {{ componentType.name.toLowerCase() }}</option>
                  <option v-for="component in getComponentsByType(componentType.id)" 
                         :key="component.id" :value="component.id">
                    {{ component.name }} - ${{ component.price }}
                  </option>
                </select>
              </div>
            </div>
            
            <div class="mt-4 p-3 bg-light rounded">
              <h6>💰 Итоговая стоимость: <span class="text-success fw-bold">{{ calculateTotalPrice() }}</span></h6>
            </div>

            <div class="mt-3">
              <button type="submit" class="btn btn-success me-2" :disabled="loading || !isFormValid()">
                <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                {{ isEditing ? '💾 Сохранить' : '➕ Добавить' }}
              </button>
              <button v-if="isEditing" type="button" class="btn btn-secondary" @click="cancelEdit">
                ❌ Отмена
              </button>
            </div>
          </form>
        </div>
      </div>

      <!-- Список конфигураций -->
      <div class="card">
        <div class="card-header d-flex justify-content-between align-items-center">
          <h5 class="card-title mb-0">📋 Список конфигураций ({{ items.length }})</h5>
          <div>
            <button class="btn btn-outline-primary btn-sm me-2" @click="loadData">
              🔄 Обновить
            </button>
            <button class="btn btn-outline-info btn-sm" @click="loadReferenceData">
              📥 Загрузить компоненты
            </button>
          </div>
        </div>
        <div class="card-body">
          <div v-if="loading" class="text-center">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Загрузка...</span>
            </div>
          </div>

          <div v-else-if="items.length === 0" class="text-center text-muted py-4">
            😔 Конфигурации не найдены
          </div>

          <div v-else class="table-responsive">
            <table class="table table-striped table-hover">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Название</th>
                  <th>Описание</th>
                  <th>Общая стоимость</th>
                  <th>Дата создания</th>
                  <th>Действия</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in items" :key="item.id">
                  <td>{{ item.id }}</td>
                  <td class="fw-bold">{{ item.name }}</td>
                  <td>{{ item.description || '—' }}</td>
                  <td class="fw-bold text-success">${{ item.total_price }}</td>
                  <td>{{ formatDate(item.created_at) }}</td>
                  <td>
                    <button class="btn btn-warning btn-sm me-1" @click="editItem(item)" title="Редактировать">
                      ✏️
                    </button>
                    <button class="btn btn-info btn-sm me-1" @click="showDetails(item)" title="Подробности">
                      🔍
                    </button>
                    <button class="btn btn-danger btn-sm" @click="deleteItem(item.id)" title="Удалить">
                      🗑️
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Модальное окно с деталями -->
      <div v-if="selectedItem" class="modal fade show" style="display: block; background: rgba(0,0,0,0.5)">
        <div class="modal-dialog modal-lg">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">🔍 Детали конфигурации</h5>
              <button type="button" class="btn-close" @click="selectedItem = null"></button>
            </div>
            <div class="modal-body">
              <div v-if="selectedItem" class="row">
                <div class="col-md-6">
                  <p><strong>Название:</strong> {{ selectedItem.name }}</p>
                  <p><strong>Описание:</strong> {{ selectedItem.description || '—' }}</p>
                  <p><strong>Общая стоимость:</strong> 
                    <span class="text-success fw-bold">${{ selectedItem.total_price }}</span>
                  </p>
                  <p><strong>Дата создания:</strong> {{ formatDate(selectedItem.created_at) }}</p>
                </div>
                <div class="col-md-6">
                  <strong>Компоненты:</strong>
                  <ul class="mt-2">
                    <li v-for="componentType in componentTypes" :key="componentType.id">
                      <strong>{{ componentType.name }}:</strong> 
                      {{ getComponentName(selectedItem[getComponentField(componentType.name)]) }}
                    </li>
                  </ul>
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="selectedItem = null">Закрыть</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

const API_BASE = '/api';

export default {
  name: 'PCConfigurationsView',
  data() {
    return {
      items: [],
      components: [],
      componentTypes: [],
      loading: false,
      isEditing: false,
      editingId: null,
      selectedItem: null,
      formData: {
        name: '',
        description: '',
        cpu: '',
        gpu: '',
        motherboard: '',
        ram: '',
        storage: '',
        power_supply: '',
        case: ''
      },
      notification: {
        message: '',
        type: 'info'
      }
    }
  },
  methods: {
    // Загрузка данных
    async loadData() {
      this.loading = true;
      try {
        const response = await axios.get(`${API_BASE}/configurations/`);
        this.items = response.data;
      } catch (error) {
        console.error('Ошибка загрузки конфигураций:', error);
        this.showNotification('Ошибка загрузки данных', 'danger');
      } finally {
        this.loading = false;
      }
    },

    // Загрузка справочников
    async loadReferenceData() {
      try {
        const [componentsResponse, typesResponse] = await Promise.all([
          axios.get(`${API_BASE}/components/`),
          axios.get(`${API_BASE}/component-types/`)
        ]);
        this.components = componentsResponse.data;
        this.componentTypes = typesResponse.data;
        this.showNotification('Компоненты загружены!', 'success');
      } catch (error) {
        console.error('Ошибка загрузки справочников:', error);
        this.showNotification('Ошибка загрузки компонентов', 'danger');
      }
    },

    // Создание конфигурации
    async createItem() {
      this.loading = true;
      try {
        const response = await axios.post(`${API_BASE}/configurations/`, this.formData);
        this.items.push(response.data);
        this.resetForm();
        this.showNotification('Конфигурация успешно создана!', 'success');
      } catch (error) {
        console.error('Ошибка создания конфигурации:', error);
        this.showNotification('Ошибка создания конфигурации', 'danger');
      } finally {
        this.loading = false;
      }
    },

    // Редактирование конфигурации
    editItem(item) {
      this.isEditing = true;
      this.editingId = item.id;
      this.formData = { ...item };
    },

    // Обновление конфигурации
    async updateItem() {
      this.loading = true;
      try {
        const response = await axios.put(`${API_BASE}/configurations/${this.editingId}/`, this.formData);
        const index = this.items.findIndex(item => item.id === this.editingId);
        if (index !== -1) {
          this.items.splice(index, 1, response.data);
        }
        this.cancelEdit();
        this.showNotification('Конфигурация успешно обновлена!', 'success');
      } catch (error) {
        console.error('Ошибка обновления конфигурации:', error);
        this.showNotification('Ошибка обновления конфигурации', 'danger');
      } finally {
        this.loading = false;
      }
    },

    // Удаление конфигурации
    async deleteItem(id) {
      if (!confirm('Вы уверены, что хотите удалить эту конфигурацию?')) {
        return;
      }

      try {
        await axios.delete(`${API_BASE}/configurations/${id}/`);
        this.items = this.items.filter(item => item.id !== id);
        this.showNotification('Конфигурация успешно удалена!', 'success');
      } catch (error) {
        console.error('Ошибка удаления конфигурации:', error);
        this.showNotification('Ошибка удаления конфигурации', 'danger');
      }
    },

    // Показать детали
    showDetails(item) {
      this.selectedItem = item;
    },

    // Вспомогательные методы
    getComponentField(typeName) {
      const fields = {
        'Процессор': 'cpu',
        'Видеокарта': 'gpu',
        'Материнская плата': 'motherboard',
        'Оперативная память': 'ram',
        'Накопитель': 'storage',
        'Блок питания': 'power_supply',
        'Корпус': 'case'
      };
      return fields[typeName] || typeName.toLowerCase();
    },

    getComponentsByType(typeId) {
      return this.components.filter(component => component.component_type === typeId);
    },

    getComponentName(componentId) {
      const component = this.components.find(c => c.id === componentId);
      return component ? component.name : `Компонент #${componentId}`;
    },

    calculateTotalPrice() {
      let total = 0;
      for (const field in this.formData) {
        if (field !== 'name' && field !== 'description' && this.formData[field]) {
          const component = this.components.find(c => c.id === this.formData[field]);
          if (component) {
            total += parseFloat(component.price);
          }
        }
      }
      return `$${total}`;
    },

    isFormValid() {
      // Проверяем, что все компоненты выбраны
      const requiredFields = ['cpu', 'gpu', 'motherboard', 'ram', 'storage', 'power_supply', 'case'];
      return requiredFields.every(field => this.formData[field]) && this.formData.name;
    },

    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString('ru-RU');
    },

    // Сброс формы
    resetForm() {
      this.isEditing = false;
      this.editingId = null;
      this.formData = {
        name: '',
        description: '',
        cpu: '',
        gpu: '',
        motherboard: '',
        ram: '',
        storage: '',
        power_supply: '',
        case: ''
      };
    },

    cancelEdit() {
      this.resetForm();
    },

    // Уведомления
    showNotification(message, type = 'info') {
      this.notification = { message, type };
      setTimeout(() => {
        this.clearNotification();
      }, 5000);
    },

    clearNotification() {
      this.notification.message = '';
    }
  },
  mounted() {
    this.loadData();
    this.loadReferenceData();
  }
}
</script>

<style scoped>
.configurations-view {
  min-height: 100vh;
  background: #f8f9fa;
}

.currency-note {
  text-align: center;
  font-weight: bold;
}

.modal {
  background: rgba(0,0,0,0.5);
}
</style>