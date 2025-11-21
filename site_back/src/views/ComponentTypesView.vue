<!-- site_back/src/views/ComponentTypesView.vue -->
<template>
  <div class="component-types-view">
    <div class="container mt-4">
      <h1 class="text-center mb-4">🏷️ Управление типами компонентов</h1>
      
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
            {{ isEditing ? '✏️ Редактирование типа' : '➕ Добавить новый тип' }}
          </h5>
        </div>
        <div class="card-body">
          <form @submit.prevent="isEditing ? updateItem() : createItem()">
            <div class="row g-3">
              <div class="col-md-8">
                <label class="form-label">Название типа *</label>
                <input v-model="formData.name" type="text" class="form-control" required>
              </div>
              <div class="col-12">
                <label class="form-label">Описание</label>
                <textarea v-model="formData.description" class="form-control" rows="3" 
                         placeholder="Описание типа компонента..."></textarea>
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

      <!-- Список типов -->
      <div class="card">
        <div class="card-header d-flex justify-content-between align-items-center">
          <h5 class="card-title mb-0">📋 Список типов ({{ items.length }})</h5>
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
            😔 Типы компонентов не найдены
          </div>

          <div v-else class="table-responsive">
            <table class="table table-striped table-hover">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Название</th>
                  <th>Описание</th>
                  <th>Действия</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in items" :key="item.id">
                  <td>{{ item.id }}</td>
                  <td class="fw-bold">{{ item.name }}</td>
                  <td>{{ item.description || '—' }}</td>
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
  name: 'ComponentTypesView',
  data() {
    return {
      items: [],
      loading: false,
      isEditing: false,
      editingId: null,
      formData: {
        name: '',
        description: ''
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
        const response = await axios.get(`${API_BASE}/component-types/`);
        this.items = response.data;
      } catch (error) {
        console.error('Ошибка загрузки типов компонентов:', error);
        this.showNotification('Ошибка загрузки данных', 'danger');
      } finally {
        this.loading = false;
      }
    },

    // Создание типа
    async createItem() {
      this.loading = true;
      try {
        const response = await axios.post(`${API_BASE}/component-types/`, this.formData);
        this.items.push(response.data);
        this.resetForm();
        this.showNotification('Тип компонента успешно создан!', 'success');
      } catch (error) {
        console.error('Ошибка создания типа:', error);
        this.showNotification('Ошибка создания типа', 'danger');
      } finally {
        this.loading = false;
      }
    },

    // Редактирование типа
    editItem(item) {
      this.isEditing = true;
      this.editingId = item.id;
      this.formData = { ...item };
    },

    // Обновление типа
    async updateItem() {
      this.loading = true;
      try {
        const response = await axios.put(`${API_BASE}/component-types/${this.editingId}/`, this.formData);
        const index = this.items.findIndex(item => item.id === this.editingId);
        if (index !== -1) {
          this.items.splice(index, 1, response.data);
        }
        this.cancelEdit();
        this.showNotification('Тип компонента успешно обновлен!', 'success');
      } catch (error) {
        console.error('Ошибка обновления типа:', error);
        this.showNotification('Ошибка обновления типа', 'danger');
      } finally {
        this.loading = false;
      }
    },

    // Удаление типа
    async deleteItem(id) {
      if (!confirm('Вы уверены, что хотите удалить этот тип компонента?')) {
        return;
      }

      try {
        await axios.delete(`${API_BASE}/component-types/${id}/`);
        this.items = this.items.filter(item => item.id !== id);
        this.showNotification('Тип компонента успешно удален!', 'success');
      } catch (error) {
        console.error('Ошибка удаления типа:', error);
        this.showNotification('Ошибка удаления типа', 'danger');
      }
    },

    // Сброс формы
    resetForm() {
      this.isEditing = false;
      this.editingId = null;
      this.formData = {
        name: '',
        description: ''
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
.component-types-view {
  min-height: 100vh;
  background: #f8f9fa;
}
</style>