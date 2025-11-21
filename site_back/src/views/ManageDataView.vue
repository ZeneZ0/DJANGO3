<!-- site_back/src/views/ManageDataView.vue -->
<template>
  <div class="manage-data-view">
    <div class="container mt-4">
      <h1 class="text-center mb-4">🛠️ Управление данными</h1>
      
      <div class="currency-note alert alert-info">
        💰 Все цены в долларах США ($)
      </div>

      <!-- Навигация по типам данных -->
      <ul class="nav nav-tabs mb-4">
        <li class="nav-item">
          <a class="nav-link" :class="{ active: activeTab === 'components' }" 
             @click="setActiveTab('components')">
            💻 Компоненты
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link" :class="{ active: activeTab === 'manufacturers' }" 
             @click="setActiveTab('manufacturers')">
            🏭 Производители
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link" :class="{ active: activeTab === 'types' }" 
             @click="setActiveTab('types')">
            🏷️ Типы компонентов
          </a>
        </li>
      </ul>

      <!-- Уведомления -->
      <div v-if="notification.message" 
           :class="['alert', `alert-${notification.type}`, 'alert-dismissible', 'fade', 'show']" 
           role="alert">
        {{ notification.message }}
        <button type="button" class="btn-close" @click="clearNotification"></button>
      </div>

      <!-- Форма добавления -->
      <div class="card mb-4">
        <div class="card-header">
          <h5 class="card-title mb-0">
            {{ isEditing ? '✏️ Редактирование' : '➕ Добавление новой записи' }}
          </h5>
        </div>
        <div class="card-body">
          <form @submit.prevent="isEditing ? updateItem() : createItem()">
            <!-- Форма для компонентов -->
            <div v-if="activeTab === 'components'" class="row g-3">
              <div class="col-md-4">
                <label class="form-label">Название</label>
                <input v-model="formData.name" type="text" class="form-control" required>
              </div>
              <div class="col-md-3">
                <label class="form-label">Тип компонента</label>
                <select v-model="formData.component_type" class="form-select" required>
                  <option value="">Выберите тип</option>
                  <option v-for="type in componentTypes" :key="type.id" :value="type.id">
                    {{ type.name }}
                  </option>
                </select>
              </div>
              <div class="col-md-3">
                <label class="form-label">Производитель</label>
                <select v-model="formData.manufacturer" class="form-select" required>
                  <option value="">Выберите производителя</option>
                  <option v-for="manufacturer in manufacturers" :key="manufacturer.id" :value="manufacturer.id">
                    {{ manufacturer.name }}
                  </option>
                </select>
              </div>
              <div class="col-md-2">
                <label class="form-label">Цена ($)</label>
                <input v-model.number="formData.price" type="number" step="0.01" class="form-control" required>
              </div>
              <div class="col-12">
                <label class="form-label">Описание</label>
                <textarea v-model="formData.description" class="form-control" rows="2"></textarea>
              </div>
              <div class="col-md-6">
                <label class="form-label">Характеристики (JSON)</label>
                <textarea v-model="formData.specifications" class="form-control" rows="3" 
                         placeholder='{"ядер": 6, "потоков": 12}'></textarea>
              </div>
              <div class="col-md-6">
                <div class="form-check mt-4">
                  <input v-model="formData.in_stock" class="form-check-input" type="checkbox">
                  <label class="form-check-label">В наличии</label>
                </div>
              </div>
            </div>

            <!-- Форма для производителей -->
            <div v-else-if="activeTab === 'manufacturers'" class="row g-3">
              <div class="col-md-6">
                <label class="form-label">Название производителя</label>
                <input v-model="formData.name" type="text" class="form-control" required>
              </div>
              <div class="col-md-4">
                <label class="form-label">Страна</label>
                <input v-model="formData.country" type="text" class="form-control" required>
              </div>
              <div class="col-md-6">
                <label class="form-label">Веб-сайт</label>
                <input v-model="formData.website" type="url" class="form-control">
              </div>
            </div>

            <!-- Форма для типов компонентов -->
            <div v-else-if="activeTab === 'types'" class="row g-3">
              <div class="col-md-8">
                <label class="form-label">Название типа</label>
                <input v-model="formData.name" type="text" class="form-control" required>
              </div>
              <div class="col-12">
                <label class="form-label">Описание</label>
                <textarea v-model="formData.description" class="form-control" rows="2"></textarea>
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

      <!-- Список записей -->
      <div class="card">
        <div class="card-header d-flex justify-content-between align-items-center">
          <h5 class="card-title mb-0">
            📋 Список записей ({{ items.length }})
          </h5>
          <button class="btn btn-outline-primary btn-sm" @click="loadData">
            🔄 Обновить
          </button>
        </div>
        <div class="card-body">
          <div v-if="loading" class="text-center">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Загрузка...</span>
            </div>
          </div>

          <div v-else-if="items.length === 0" class="text-center text-muted py-4">
            😔 Записи не найдены
          </div>

          <div v-else>
            <!-- Таблица компонентов -->
            <div v-if="activeTab === 'components'" class="table-responsive">
              <table class="table table-striped table-hover">
                <thead>
                  <tr>
                    <th>Название</th>
                    <th>Тип</th>
                    <th>Производитель</th>
                    <th>Цена</th>
                    <th>Наличие</th>
                    <th>Действия</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="item in items" :key="item.id">
                    <td>{{ item.name }}</td>
                    <td>{{ getComponentTypeName(item.component_type) }}</td>
                    <td>{{ getManufacturerName(item.manufacturer) }}</td>
                    <td class="fw-bold text-success">${{ item.price }}</td>
                    <td>
                      <span :class="['badge', item.in_stock ? 'bg-success' : 'bg-danger']">
                        {{ item.in_stock ? 'В наличии' : 'Нет в наличии' }}
                      </span>
                    </td>
                    <td>
                      <button class="btn btn-warning btn-sm me-1" @click="editItem(item)">
                        ✏️
                      </button>
                      <button class="btn btn-danger btn-sm" @click="deleteItem(item.id)">
                        🗑️
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Таблица производителей -->
            <div v-else-if="activeTab === 'manufacturers'" class="table-responsive">
              <table class="table table-striped table-hover">
                <thead>
                  <tr>
                    <th>Название</th>
                    <th>Страна</th>
                    <th>Веб-сайт</th>
                    <th>Действия</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="item in items" :key="item.id">
                    <td>{{ item.name }}</td>
                    <td>{{ item.country }}</td>
                    <td>
                      <a v-if="item.website" :href="item.website" target="_blank" class="text-decoration-none">
                        {{ item.website }}
                      </a>
                      <span v-else class="text-muted">—</span>
                    </td>
                    <td>
                      <button class="btn btn-warning btn-sm me-1" @click="editItem(item)">
                        ✏️
                      </button>
                      <button class="btn btn-danger btn-sm" @click="deleteItem(item.id)">
                        🗑️
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Таблица типов компонентов -->
            <div v-else-if="activeTab === 'types'" class="table-responsive">
              <table class="table table-striped table-hover">
                <thead>
                  <tr>
                    <th>Название</th>
                    <th>Описание</th>
                    <th>Действия</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="item in items" :key="item.id">
                    <td>{{ item.name }}</td>
                    <td>{{ item.description || '—' }}</td>
                    <td>
                      <button class="btn btn-warning btn-sm me-1" @click="editItem(item)">
                        ✏️
                      </button>
                      <button class="btn btn-danger btn-sm" @click="deleteItem(item.id)">
                        🗑️
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Cookies from 'js-cookie';

const API_BASE = '/api';

export default {
  name: 'ManageDataView',
  data() {
    return {
      activeTab: 'components',
      items: [],
      componentTypes: [],
      manufacturers: [],
      loading: false,
      isEditing: false,
      editingId: null,
      formData: this.getEmptyForm(),
      notification: {
        message: '',
        type: 'info'
      }
    }
  },
  computed: {
    currentEndpoint() {
      const endpoints = {
        components: 'components',
        manufacturers: 'manufacturers',
        types: 'component-types'
      };
      return endpoints[this.activeTab];
    }
  },
  methods: {
    // Получение пустой формы
    getEmptyForm() {
      return {
        name: '',
        component_type: '',
        manufacturer: '',
        price: 0,
        description: '',
        specifications: '{}',
        in_stock: true,
        country: '',
        website: ''
      };
    },

    // Установка активной вкладки
    setActiveTab(tab) {
      this.activeTab = tab;
      this.resetForm();
      this.loadData();
    },

    // Загрузка данных
    async loadData() {
      this.loading = true;
      try {
        // Загрузка основных данных
        const response = await axios.get(`${API_BASE}/${this.currentEndpoint}/`);
        this.items = response.data;

        // Загрузка справочников для компонентов
        if (this.activeTab === 'components') {
          const [typesResponse, manufacturersResponse] = await Promise.all([
            axios.get(`${API_BASE}/component-types/`),
            axios.get(`${API_BASE}/manufacturers/`)
          ]);
          this.componentTypes = typesResponse.data;
          this.manufacturers = manufacturersResponse.data;
        }

      } catch (error) {
        console.error('Ошибка загрузки данных:', error);
        this.showNotification('Ошибка загрузки данных', 'danger');
      } finally {
        this.loading = false;
      }
    },

    // Создание записи
    async createItem() {
      this.loading = true;
      try {
        let data = { ...this.formData };
        
        // Обработка спецификаций для компонентов
        if (this.activeTab === 'components' && data.specifications) {
          try {
            data.specifications = JSON.parse(data.specifications);
          } catch (e) {
            data.specifications = {};
          }
        }

        const response = await axios.post(`${API_BASE}/${this.currentEndpoint}/`, data);
        this.items.push(response.data);
        this.resetForm();
        this.showNotification('Запись успешно создана!', 'success');
        
        // Сохраняем в cookies для демонстрации
        Cookies.set('last_created_item', JSON.stringify(response.data), { expires: 7 });
        
      } catch (error) {
        console.error('Ошибка создания записи:', error);
        this.showNotification('Ошибка создания записи', 'danger');
      } finally {
        this.loading = false;
      }
    },

    // Редактирование записи
    editItem(item) {
      this.isEditing = true;
      this.editingId = item.id;
      this.formData = { ...this.getEmptyForm(), ...item };
      
      // Преобразование спецификаций в JSON строку
      if (this.activeTab === 'components' && item.specifications) {
        this.formData.specifications = JSON.stringify(item.specifications, null, 2);
      }
    },

    // Обновление записи
    async updateItem() {
      this.loading = true;
      try {
        let data = { ...this.formData };
        
        // Обработка спецификаций для компонентов
        if (this.activeTab === 'components' && data.specifications) {
          try {
            data.specifications = JSON.parse(data.specifications);
          } catch (e) {
            data.specifications = {};
          }
        }

        const response = await axios.put(`${API_BASE}/${this.currentEndpoint}/${this.editingId}/`, data);
        const index = this.items.findIndex(item => item.id === this.editingId);
        if (index !== -1) {
          this.items.splice(index, 1, response.data);
        }
        
        this.cancelEdit();
        this.showNotification('Запись успешно обновлена!', 'success');
        
      } catch (error) {
        console.error('Ошибка обновления записи:', error);
        this.showNotification('Ошибка обновления записи', 'danger');
      } finally {
        this.loading = false;
      }
    },

    // Удаление записи
    async deleteItem(id) {
      if (!confirm('Вы уверены, что хотите удалить эту запись?')) {
        return;
      }

      try {
        await axios.delete(`${API_BASE}/${this.currentEndpoint}/${id}/`);
        this.items = this.items.filter(item => item.id !== id);
        this.showNotification('Запись успешно удалена!', 'success');
      } catch (error) {
        console.error('Ошибка удаления записи:', error);
        this.showNotification('Ошибка удаления записи', 'danger');
      }
    },

    // Сброс формы
    resetForm() {
      this.isEditing = false;
      this.editingId = null;
      this.formData = this.getEmptyForm();
    },

    cancelEdit() {
      this.resetForm();
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
  }
}
</script>

<style scoped>
.manage-data-view {
  min-height: 100vh;
  background: #f8f9fa;
}

.currency-note {
  text-align: center;
  font-weight: bold;
}

.nav-tabs .nav-link {
  cursor: pointer;
  color: #495057;
}

.nav-tabs .nav-link.active {
  color: #0d6efd;
  font-weight: bold;
}

.table-responsive {
  border-radius: 0.375rem;
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}
</style>