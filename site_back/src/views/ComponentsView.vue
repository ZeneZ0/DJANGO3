<!-- site_back/src/views/ComponentsView.vue -->
<template>
  <div class="components-view">
    <div class="container mt-4">
      <h1 class="text-center mb-4">💻 Управление компонентами</h1>
      
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
            {{ isEditing ? '✏️ Редактирование компонента' : '➕ Добавить новый компонент' }}
          </h5>
        </div>
        <div class="card-body">
          <form @submit.prevent="isEditing ? updateItem() : createItem()">
            <div class="row g-3">
              <div class="col-md-6">
                <label class="form-label">Название компонента *</label>
                <input v-model="formData.name" type="text" class="form-control" required>
              </div>
              <div class="col-md-3">
                <label class="form-label">Тип компонента *</label>
                <select v-model="formData.component_type" class="form-select" required>
                  <option value="">Выберите тип</option>
                  <option v-for="type in componentTypes" :key="type.id" :value="type.id">
                    {{ type.name }}
                  </option>
                </select>
              </div>
              <div class="col-md-3">
                <label class="form-label">Производитель *</label>
                <select v-model="formData.manufacturer" class="form-select" required>
                  <option value="">Выберите производителя</option>
                  <option v-for="manufacturer in manufacturers" :key="manufacturer.id" :value="manufacturer.id">
                    {{ manufacturer.name }}
                  </option>
                </select>
              </div>
              <div class="col-md-4">
                <label class="form-label">Цена ($) *</label>
                <input v-model.number="formData.price" type="number" step="0.01" min="0" class="form-control" required>
              </div>
              <div class="col-md-8">
                <label class="form-label">Описание</label>
                <textarea v-model="formData.description" class="form-control" rows="2" 
                         placeholder="Описание компонента..."></textarea>
              </div>
              <div class="col-md-6">
                <label class="form-label">Характеристики (JSON)</label>
                <textarea v-model="formData.specifications" class="form-control" rows="3" 
                         placeholder='{"ядер": 6, "потоков": 12, "частота": "3.5GHz"}'></textarea>
                <div class="form-text">Введите характеристики в формате JSON</div>
              </div>
              <div class="col-md-6">
                <div class="form-check mt-4">
                  <input v-model="formData.in_stock" class="form-check-input" type="checkbox">
                  <label class="form-check-label">В наличии</label>
                </div>
              </div>
            </div>
            <div class="mt-3">
              <button type="submit" class="btn btn-success me-2" :disabled="loading">
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

      <!-- Список компонентов -->
      <div class="card">
        <div class="card-header d-flex justify-content-between align-items-center">
          <h5 class="card-title mb-0">📋 Список компонентов ({{ items.length }})</h5>
          <div>
            <button class="btn btn-outline-primary btn-sm me-2" @click="loadData">
              🔄 Обновить
            </button>
            <button class="btn btn-outline-info btn-sm" @click="loadReferenceData">
              📥 Загрузить справочники
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
            😔 Компоненты не найдены
          </div>

          <div v-else class="table-responsive">
            <table class="table table-striped table-hover">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Название</th>
                  <th>Тип</th>
                  <th>Производитель</th>
                  <th>Цена</th>
                  <th>Наличие</th>
                  <th>Действия</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in items" :key="item.id" :class="{ 'table-warning': !item.in_stock }">
                  <td>{{ item.id }}</td>
                  <td class="fw-bold">{{ item.name }}</td>
                  <td>
                    <span class="badge bg-primary">{{ getComponentTypeName(item.component_type) }}</span>
                  </td>
                  <td>
                    <span class="badge bg-info">{{ getManufacturerName(item.manufacturer) }}</span>
                  </td>
                  <td class="fw-bold text-success">${{ item.price }}</td>
                  <td>
                    <span :class="['badge', item.in_stock ? 'bg-success' : 'bg-danger']">
                      {{ item.in_stock ? 'В наличии' : 'Нет в наличии' }}
                    </span>
                  </td>
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
              <h5 class="modal-title">🔍 Детали компонента</h5>
              <button type="button" class="btn-close" @click="selectedItem = null"></button>
            </div>
            <div class="modal-body">
              <div v-if="selectedItem" class="row">
                <div class="col-md-6">
                  <p><strong>Название:</strong> {{ selectedItem.name }}</p>
                  <p><strong>Тип:</strong> {{ getComponentTypeName(selectedItem.component_type) }}</p>
                  <p><strong>Производитель:</strong> {{ getManufacturerName(selectedItem.manufacturer) }}</p>
                  <p><strong>Цена:</strong> <span class="text-success fw-bold">${{ selectedItem.price }}</span></p>
                  <p><strong>Наличие:</strong> 
                    <span :class="['badge', selectedItem.in_stock ? 'bg-success' : 'bg-danger']">
                      {{ selectedItem.in_stock ? 'В наличии' : 'Нет в наличии' }}
                    </span>
                  </p>
                </div>
                <div class="col-md-6">
                  <p><strong>Описание:</strong> {{ selectedItem.description || '—' }}</p>
                  <div v-if="selectedItem.specifications && Object.keys(selectedItem.specifications).length > 0">
                    <strong>Характеристики:</strong>
                    <ul class="mt-2">
                      <li v-for="(value, key) in selectedItem.specifications" :key="key">
                        <strong>{{ key }}:</strong> {{ value }}
                      </li>
                    </ul>
                  </div>
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
  name: 'ComponentsView',
  data() {
    return {
      items: [],
      componentTypes: [],
      manufacturers: [],
      loading: false,
      isEditing: false,
      editingId: null,
      selectedItem: null,
      formData: {
        name: '',
        component_type: '',
        manufacturer: '',
        price: 0,
        description: '',
        specifications: '{}',
        in_stock: true
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
        const response = await axios.get(`${API_BASE}/components/`);
        this.items = response.data;
      } catch (error) {
        console.error('Ошибка загрузки компонентов:', error);
        this.showNotification('Ошибка загрузки данных', 'danger');
      } finally {
        this.loading = false;
      }
    },

    // Загрузка справочников
    async loadReferenceData() {
      try {
        const [typesResponse, manufacturersResponse] = await Promise.all([
          axios.get(`${API_BASE}/component-types/`),
          axios.get(`${API_BASE}/manufacturers/`)
        ]);
        this.componentTypes = typesResponse.data;
        this.manufacturers = manufacturersResponse.data;
        this.showNotification('Справочники загружены!', 'success');
      } catch (error) {
        console.error('Ошибка загрузки справочников:', error);
        this.showNotification('Ошибка загрузки справочников', 'danger');
      }
    },

    // Создание компонента
    async createItem() {
      this.loading = true;
      try {
        let data = { ...this.formData };
        
        // Обработка спецификаций
        if (data.specifications) {
          try {
            data.specifications = JSON.parse(data.specifications);
          } catch (e) {
            data.specifications = {};
          }
        }

        const response = await axios.post(`${API_BASE}/components/`, data);
        this.items.push(response.data);
        this.resetForm();
        this.showNotification('Компонент успешно создан!', 'success');
      } catch (error) {
        console.error('Ошибка создания компонента:', error);
        this.showNotification('Ошибка создания компонента', 'danger');
      } finally {
        this.loading = false;
      }
    },

    // Редактирование компонента
    editItem(item) {
      this.isEditing = true;
      this.editingId = item.id;
      this.formData = { ...item };
      
      // Преобразование спецификаций в JSON строку
      if (item.specifications) {
        this.formData.specifications = JSON.stringify(item.specifications, null, 2);
      }
    },

    // Обновление компонента
    async updateItem() {
      this.loading = true;
      try {
        let data = { ...this.formData };
        
        // Обработка спецификаций
        if (data.specifications) {
          try {
            data.specifications = JSON.parse(data.specifications);
          } catch (e) {
            data.specifications = {};
          }
        }

        const response = await axios.put(`${API_BASE}/components/${this.editingId}/`, data);
        const index = this.items.findIndex(item => item.id === this.editingId);
        if (index !== -1) {
          this.items.splice(index, 1, response.data);
        }
        this.cancelEdit();
        this.showNotification('Компонент успешно обновлен!', 'success');
      } catch (error) {
        console.error('Ошибка обновления компонента:', error);
        this.showNotification('Ошибка обновления компонента', 'danger');
      } finally {
        this.loading = false;
      }
    },

    // Удаление компонента
    async deleteItem(id) {
      if (!confirm('Вы уверены, что хотите удалить этот компонент?')) {
        return;
      }

      try {
        await axios.delete(`${API_BASE}/components/${id}/`);
        this.items = this.items.filter(item => item.id !== id);
        this.showNotification('Компонент успешно удален!', 'success');
      } catch (error) {
        console.error('Ошибка удаления компонента:', error);
        this.showNotification('Ошибка удаления компонента', 'danger');
      }
    },

    // Показать детали
    showDetails(item) {
      this.selectedItem = item;
    },

    // Вспомогательные методы
    getComponentTypeName(typeId) {
      const type = this.componentTypes.find(t => t.id === typeId);
      return type ? type.name : `Тип #${typeId}`;
    },

    getManufacturerName(manufacturerId) {
      const manufacturer = this.manufacturers.find(m => m.id === manufacturerId);
      return manufacturer ? manufacturer.name : `Произв. #${manufacturerId}`;
    },

    // Сброс формы
    resetForm() {
      this.isEditing = false;
      this.editingId = null;
      this.formData = {
        name: '',
        component_type: '',
        manufacturer: '',
        price: 0,
        description: '',
        specifications: '{}',
        in_stock: true
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
.components-view {
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