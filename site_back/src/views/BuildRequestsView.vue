<!-- site_back/src/views/BuildRequestsView.vue -->
<template>
  <div class="build-requests-view">
    <div class="container mt-4">
      <h1 class="text-center mb-4">📝 Управление запросами на сборку</h1>
      
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
            {{ isEditing ? '✏️ Редактирование запроса' : '➕ Создать новый запрос' }}
          </h5>
        </div>
        <div class="card-body">
          <form @submit.prevent="isEditing ? updateItem() : createItem()">
            <div class="row g-3">
              <div class="col-md-6">
                <label class="form-label">Пользователь *</label>
                <select v-model="formData.user" class="form-select" required>
                  <option value="">Выберите пользователя</option>
                  <option v-for="user in users" :key="user.id" :value="user.id">
                    {{ user.username }}
                  </option>
                </select>
              </div>
              <div class="col-md-6">
                <label class="form-label">Конфигурация *</label>
                <select v-model="formData.configuration" class="form-select" required @change="updateBudget">
                  <option value="">Выберите конфигурацию</option>
                  <option v-for="config in configurations" :key="config.id" :value="config.id">
                    {{ config.name }} - ${{ config.total_price }}
                  </option>
                </select>
              </div>
              <div class="col-md-4">
                <label class="form-label">Бюджет ($) *</label>
                <input v-model.number="formData.budget" type="number" step="0.01" min="0" class="form-control" required>
              </div>
              <div class="col-md-4">
                <label class="form-label">Статус *</label>
                <select v-model="formData.status" class="form-select" required>
                  <option value="pending">⏳ Ожидает</option>
                  <option value="in_progress">🔧 В работе</option>
                  <option value="completed">✅ Завершено</option>
                  <option value="cancelled">❌ Отменено</option>
                </select>
              </div>
              <div class="col-12">
                <label class="form-label">Дополнительные пожелания</label>
                <textarea v-model="formData.notes" class="form-control" rows="3" 
                         placeholder="Дополнительные требования или пожелания..."></textarea>
              </div>
            </div>

            <div class="mt-4 p-3 bg-light rounded" v-if="selectedConfiguration">
              <h6>📊 Информация о конфигурации:</h6>
              <p><strong>Название:</strong> {{ selectedConfiguration.name }}</p>
              <p><strong>Стоимость:</strong> <span class="text-success fw-bold">${{ selectedConfiguration.total_price }}</span></p>
              <p><strong>Разница с бюджетом:</strong> 
                <span :class="budgetDifference >= 0 ? 'text-success' : 'text-danger'">
                  ${{ Math.abs(budgetDifference) }} 
                  {{ budgetDifference >= 0 ? 'в пределах бюджета' : 'превышение бюджета' }}
                </span>
              </p>
            </div>

            <div class="mt-3">
              <button type="submit" class="btn btn-success me-2" :disabled="loading">
                <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                {{ isEditing ? '💾 Сохранить' : '➕ Создать запрос' }}
              </button>
              <button v-if="isEditing" type="button" class="btn btn-secondary" @click="cancelEdit">
                ❌ Отмена
              </button>
            </div>
          </form>
        </div>
      </div>

      <!-- Список запросов -->
      <div class="card">
        <div class="card-header d-flex justify-content-between align-items-center">
          <h5 class="card-title mb-0">📋 Список запросов ({{ items.length }})</h5>
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
          <div class="row mb-3">
            <div class="col-md-4">
              <select v-model="statusFilter" class="form-select" @change="applyFilters">
                <option value="">Все статусы</option>
                <option value="pending">⏳ Ожидает</option>
                <option value="in_progress">🔧 В работе</option>
                <option value="completed">✅ Завершено</option>
                <option value="cancelled">❌ Отменено</option>
              </select>
            </div>
            <div class="col-md-4">
              <input v-model="searchQuery" type="text" class="form-control" placeholder="Поиск по пользователю..." @input="applyFilters">
            </div>
          </div>

          <div v-if="loading" class="text-center">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Загрузка...</span>
            </div>
          </div>

          <div v-else-if="filteredItems.length === 0" class="text-center text-muted py-4">
            😔 Запросы не найдены
          </div>

          <div v-else class="table-responsive">
            <table class="table table-striped table-hover">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Пользователь</th>
                  <th>Конфигурация</th>
                  <th>Бюджет</th>
                  <th>Статус</th>
                  <th>Дата создания</th>
                  <th>Действия</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in filteredItems" :key="item.id" :class="getStatusClass(item.status)">
                  <td>{{ item.id }}</td>
                  <td class="fw-bold">{{ getUserName(item.user) }}</td>
                  <td>{{ getConfigurationName(item.configuration) }}</td>
                  <td class="fw-bold">${{ item.budget }}</td>
                  <td>
                    <span :class="['badge', getStatusBadgeClass(item.status)]">
                      {{ getStatusText(item.status) }}
                    </span>
                  </td>
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
              <h5 class="modal-title">🔍 Детали запроса на сборку</h5>
              <button type="button" class="btn-close" @click="selectedItem = null"></button>
            </div>
            <div class="modal-body">
              <div v-if="selectedItem" class="row">
                <div class="col-md-6">
                  <p><strong>ID запроса:</strong> {{ selectedItem.id }}</p>
                  <p><strong>Пользователь:</strong> {{ getUserName(selectedItem.user) }}</p>
                  <p><strong>Конфигурация:</strong> {{ getConfigurationName(selectedItem.configuration) }}</p>
                  <p><strong>Бюджет:</strong> <span class="text-success fw-bold">${{ selectedItem.budget }}</span></p>
                </div>
                <div class="col-md-6">
                  <p><strong>Статус:</strong> 
                    <span :class="['badge', getStatusBadgeClass(selectedItem.status)]">
                      {{ getStatusText(selectedItem.status) }}
                    </span>
                  </p>
                  <p><strong>Дата создания:</strong> {{ formatDate(selectedItem.created_at) }}</p>
                  <p><strong>Дата обновления:</strong> {{ formatDate(selectedItem.updated_at) }}</p>
                  <div v-if="selectedItem.notes">
                    <strong>Дополнительные пожелания:</strong>
                    <p class="mt-1">{{ selectedItem.notes }}</p>
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
  name: 'BuildRequestsView',
  data() {
    return {
      items: [],
      users: [],
      configurations: [],
      loading: false,
      isEditing: false,
      editingId: null,
      selectedItem: null,
      searchQuery: '',
      statusFilter: '',
      formData: {
        user: '',
        configuration: '',
        budget: 0,
        status: 'pending',
        notes: ''
      },
      notification: {
        message: '',
        type: 'info'
      }
    }
  },
  computed: {
    filteredItems() {
      let filtered = this.items;
      
      // Фильтрация по статусу
      if (this.statusFilter) {
        filtered = filtered.filter(item => item.status === this.statusFilter);
      }
      
      // Поиск по пользователю
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(item => {
          const userName = this.getUserName(item.user).toLowerCase();
          return userName.includes(query);
        });
      }
      
      return filtered;
    },
    
    selectedConfiguration() {
      if (!this.formData.configuration) return null;
      return this.configurations.find(config => config.id === this.formData.configuration);
    },
    
    budgetDifference() {
      if (!this.selectedConfiguration) return 0;
      return this.formData.budget - this.selectedConfiguration.total_price;
    }
  },
  methods: {
    // Загрузка данных
    async loadData() {
      this.loading = true;
      try {
        const response = await axios.get(`${API_BASE}/build-requests/`);
        this.items = response.data;
      } catch (error) {
        console.error('Ошибка загрузки запросов:', error);
        this.showNotification('Ошибка загрузки данных', 'danger');
      } finally {
        this.loading = false;
      }
    },

    // Загрузка справочников
    async loadReferenceData() {
      try {
        const [usersResponse, configsResponse] = await Promise.all([
          axios.get(`${API_BASE}/users/`), // Нужно создать endpoint для пользователей
          axios.get(`${API_BASE}/configurations/`)
        ]);
        this.users = usersResponse.data;
        this.configurations = configsResponse.data;
        this.showNotification('Справочники загружены!', 'success');
      } catch (error) {
        console.error('Ошибка загрузки справочников:', error);
        // Если endpoint для пользователей не существует, создаем тестовых пользователей
        if (error.response?.status === 404) {
          this.users = [
            { id: 1, username: 'test_user' },
            { id: 2, username: 'admin' },
            { id: 3, username: 'ivan' }
          ];
          this.showNotification('Используются тестовые пользователи', 'info');
        } else {
          this.showNotification('Ошибка загрузки справочников', 'danger');
        }
      }
    },

    // Создание запроса
    async createItem() {
      this.loading = true;
      try {
        const response = await axios.post(`${API_BASE}/build-requests/`, this.formData);
        this.items.push(response.data);
        this.resetForm();
        this.showNotification('Запрос на сборку успешно создан!', 'success');
      } catch (error) {
        console.error('Ошибка создания запроса:', error);
        this.showNotification('Ошибка создания запроса', 'danger');
      } finally {
        this.loading = false;
      }
    },

    // Редактирование запроса
    editItem(item) {
      this.isEditing = true;
      this.editingId = item.id;
      this.formData = { ...item };
    },

    // Обновление запроса
    async updateItem() {
      this.loading = true;
      try {
        const response = await axios.put(`${API_BASE}/build-requests/${this.editingId}/`, this.formData);
        const index = this.items.findIndex(item => item.id === this.editingId);
        if (index !== -1) {
          this.items.splice(index, 1, response.data);
        }
        this.cancelEdit();
        this.showNotification('Запрос на сборку успешно обновлен!', 'success');
      } catch (error) {
        console.error('Ошибка обновления запроса:', error);
        this.showNotification('Ошибка обновления запроса', 'danger');
      } finally {
        this.loading = false;
      }
    },

    // Удаление запроса
    async deleteItem(id) {
      if (!confirm('Вы уверены, что хотите удалить этот запрос?')) {
        return;
      }

      try {
        await axios.delete(`${API_BASE}/build-requests/${id}/`);
        this.items = this.items.filter(item => item.id !== id);
        this.showNotification('Запрос на сборку успешно удален!', 'success');
      } catch (error) {
        console.error('Ошибка удаления запроса:', error);
        this.showNotification('Ошибка удаления запроса', 'danger');
      }
    },

    // Показать детали
    showDetails(item) {
      this.selectedItem = item;
    },

    // Обновить бюджет при выборе конфигурации
    updateBudget() {
      if (this.selectedConfiguration && !this.isEditing) {
        this.formData.budget = this.selectedConfiguration.total_price;
      }
    },

    // Применить фильтры
    applyFilters() {
      // Фильтрация происходит через computed свойство
    },

    // Вспомогательные методы
    getUserName(userId) {
      const user = this.users.find(u => u.id === userId);
      return user ? user.username : `Пользователь #${userId}`;
    },

    getConfigurationName(configId) {
      const config = this.configurations.find(c => c.id === configId);
      return config ? config.name : `Конфигурация #${configId}`;
    },

    getStatusText(status) {
      const statuses = {
        pending: '⏳ Ожидает',
        in_progress: '🔧 В работе',
        completed: '✅ Завершено',
        cancelled: '❌ Отменено'
      };
      return statuses[status] || status;
    },

    getStatusBadgeClass(status) {
      const classes = {
        pending: 'bg-warning',
        in_progress: 'bg-info',
        completed: 'bg-success',
        cancelled: 'bg-danger'
      };
      return classes[status] || 'bg-secondary';
    },

    getStatusClass(status) {
      const classes = {
        completed: 'table-success',
        cancelled: 'table-danger',
        in_progress: 'table-info'
      };
      return classes[status] || '';
    },

    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString('ru-RU');
    },

    // Сброс формы
    resetForm() {
      this.isEditing = false;
      this.editingId = null;
      this.formData = {
        user: '',
        configuration: '',
        budget: 0,
        status: 'pending',
        notes: ''
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
.build-requests-view {
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