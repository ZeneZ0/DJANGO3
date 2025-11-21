<!-- site_back/src/views/ManufacturersView.vue -->
<template>
  <div class="manufacturers-view">
    <div class="container mt-4">
      <h1 class="text-center mb-4">🏭 Управление производителями</h1>
      
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
            {{ isEditing ? '✏️ Редактирование производителя' : '➕ Добавить нового производителя' }}
          </h5>
        </div>
        <div class="card-body">
          <form @submit.prevent="isEditing ? updateItem() : createItem()">
            <div class="row g-3">
              <div class="col-md-6">
                <label class="form-label">Название производителя *</label>
                <input v-model="formData.name" type="text" class="form-control" required>
              </div>
              <div class="col-md-4">
                <label class="form-label">Страна *</label>
                <input v-model="formData.country" type="text" class="form-control" required>
              </div>
              <div class="col-md-6">
                <label class="form-label">Веб-сайт</label>
                <input v-model="formData.website" type="url" class="form-control" placeholder="https://example.com">
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

      <!-- Список производителей -->
      <div class="card">
        <div class="card-header d-flex justify-content-between align-items-center">
          <h5 class="card-title mb-0">📋 Список производителей ({{ items.length }})</h5>
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
            😔 Производители не найдены
          </div>

          <div v-else class="table-responsive">
            <table class="table table-striped table-hover">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Название</th>
                  <th>Страна</th>
                  <th>Веб-сайт</th>
                  <th>Действия</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in items" :key="item.id">
                  <td>{{ item.id }}</td>
                  <td class="fw-bold">{{ item.name }}</td>
                  <td>
                    <span class="badge bg-info">{{ item.country }}</span>
                  </td>
                  <td>
                    <a v-if="item.website" :href="item.website" target="_blank" class="text-decoration-none">
                      🔗 Сайт
                    </a>
                    <span v-else class="text-muted">—</span>
                  </td>
                  <td>
                    <button class="btn btn-warning btn-sm me-1" @click="editItem(item)" title="Редактировать">
                      ✏️
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
    </div>
  </div>
</template>

<script>
import axios from 'axios';

const API_BASE = '/api';

export default {
  name: 'ManufacturersView',
  data() {
    return {
      items: [],
      loading: false,
      isEditing: false,
      editingId: null,
      formData: {
        name: '',
        country: '',
        website: ''
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
        const response = await axios.get(`${API_BASE}/manufacturers/`);
        this.items = response.data;
      } catch (error) {
        console.error('Ошибка загрузки производителей:', error);
        this.showNotification('Ошибка загрузки данных', 'danger');
      } finally {
        this.loading = false;
      }
    },

    // Создание производителя
    async createItem() {
      this.loading = true;
      try {
        const response = await axios.post(`${API_BASE}/manufacturers/`, this.formData);
        this.items.push(response.data);
        this.resetForm();
        this.showNotification('Производитель успешно создан!', 'success');
      } catch (error) {
        console.error('Ошибка создания производителя:', error);
        this.showNotification('Ошибка создания производителя', 'danger');
      } finally {
        this.loading = false;
      }
    },

    // Редактирование производителя
    editItem(item) {
      this.isEditing = true;
      this.editingId = item.id;
      this.formData = { ...item };
    },

    // Обновление производителя
    async updateItem() {
      this.loading = true;
      try {
        const response = await axios.put(`${API_BASE}/manufacturers/${this.editingId}/`, this.formData);
        const index = this.items.findIndex(item => item.id === this.editingId);
        if (index !== -1) {
          this.items.splice(index, 1, response.data);
        }
        this.cancelEdit();
        this.showNotification('Производитель успешно обновлен!', 'success');
      } catch (error) {
        console.error('Ошибка обновления производителя:', error);
        this.showNotification('Ошибка обновления производителя', 'danger');
      } finally {
        this.loading = false;
      }
    },

    // Удаление производителя
    async deleteItem(id) {
      if (!confirm('Вы уверены, что хотите удалить этого производителя?')) {
        return;
      }

      try {
        await axios.delete(`${API_BASE}/manufacturers/${id}/`);
        this.items = this.items.filter(item => item.id !== id);
        this.showNotification('Производитель успешно удален!', 'success');
      } catch (error) {
        console.error('Ошибка удаления производителя:', error);
        this.showNotification('Ошибка удаления производителя', 'danger');
      }
    },

    // Сброс формы
    resetForm() {
      this.isEditing = false;
      this.editingId = null;
      this.formData = {
        name: '',
        country: '',
        website: ''
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
  }
}
</script>

<style scoped>
.manufacturers-view {
  min-height: 100vh;
  background: #f8f9fa;
}
</style>