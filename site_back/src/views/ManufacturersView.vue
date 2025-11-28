<!-- site_back/src/views/ManufacturersView.vue -->
<template>
  <div class="manufacturers-view">
    <div class="container mt-4">
      <h1 class="text-center mb-4">🏭 Управление производителями</h1>
      
      <!-- Информация о пользователе -->
      <div class="user-info alert alert-info" v-if="currentUser">
        👤 Текущий пользователь: <strong>{{ currentUser.username }}</strong>
        <span v-if="currentUser.is_superuser" class="badge bg-warning ms-2">Суперпользователь</span>
      </div>

      <!-- Фильтр по пользователю для суперпользователя -->
      <div class="card mb-3" v-if="currentUser && currentUser.is_superuser">
        <div class="card-body">
          <h6>🔍 Фильтр по пользователю (только для админа)</h6>
          <div class="row g-3 align-items-end">
            <div class="col-md-6">
              <label class="form-label">Пользователь</label>
              <select v-model="selectedUserId" class="form-select" @change="loadData">
                <option value="">Все пользователи</option>
                <option v-for="user in users" :key="user.id" :value="user.id">
                  {{ user.username }} {{ user.is_superuser ? '(admin)' : '' }}
                </option>
              </select>
            </div>
            <div class="col-md-6">
              <button class="btn btn-outline-secondary w-100" @click="clearFilter">
                ❌ Сбросить фильтр
              </button>
            </div>
          </div>
        </div>
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
            {{ isEditing ? '✏️ Редактирование производителя' : '➕ Добавить нового производителя' }}
          </h5>
        </div>
        <div class="card-body">
          <form @submit.prevent="isEditing ? updateItem() : createItem()" enctype="multipart/form-data">
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
              
              <!-- Поле для загрузки логотипа -->
              <div class="col-12">
                <label class="form-label">Логотип</label>
                <input 
                  type="file" 
                  class="form-control" 
                  accept="image/*"
                  @change="handleLogoUpload"
                  ref="logoInput"
                >
                <div class="form-text">Поддерживаются форматы: JPG, PNG, GIF</div>
                
                <!-- Предпросмотр логотипа -->
                <div v-if="logoPreview" class="mt-3">
                  <p class="mb-2"><strong>Предпросмотр:</strong></p>
                  <img :src="logoPreview" class="img-thumbnail" style="max-height: 150px; cursor: pointer" 
                       @click="openImageModal(logoPreview)" alt="Предпросмотр логотипа">
                </div>
                
                <!-- Текущее изображение при редактировании -->
                <div v-else-if="isEditing && currentLogoUrl" class="mt-3">
                  <p class="mb-2"><strong>Текущее изображение:</strong></p>
                  <img :src="currentLogoUrl" class="img-thumbnail" style="max-height: 150px; cursor: pointer"
                       @click="openImageModal(currentLogoUrl)" alt="Текущий логотип">
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

      <!-- Список производителей -->
      <div class="card">
        <div class="card-header d-flex justify-content-between align-items-center">
          <h5 class="card-title mb-0">
            📋 Список производителей ({{ items.length }})
            <span v-if="selectedUserId" class="text-muted fs-6">
              - отфильтровано по пользователю
            </span>
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
            😔 Производители не найдены
          </div>

          <div v-else class="table-responsive">
            <table class="table table-striped table-hover">
              <thead>
                <tr>
                  <th>Логотип</th>
                  <th>Название</th>
                  <th>Страна</th>
                  <th>Веб-сайт</th>
                  <th>Пользователь</th>
                  <th>Действия</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in items" :key="item.id">
                  <td>
                    <img v-if="item.logo_url" 
                         :src="item.logo_url" 
                         class="img-thumbnail" 
                         style="width: 50px; height: 50px; object-fit: contain; cursor: pointer"
                         @click="openImageModal(item.logo_url)"
                         :alt="`Логотип ${item.name}`">
                    <span v-else class="text-muted">—</span>
                  </td>
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
                    <span class="badge" :class="getUserBadgeClass(item.user_name)">
                      {{ item.user_name }}
                    </span>
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

    <!-- Модальное окно для просмотра изображения -->
    <div v-if="showImageModal" class="modal fade show d-block" style="background: rgba(0,0,0,0.8)">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">🖼️ Просмотр изображения</h5>
            <button type="button" class="btn-close" @click="closeImageModal"></button>
          </div>
          <div class="modal-body text-center">
            <img :src="modalImageUrl" class="img-fluid" style="max-height: 70vh" alt="Увеличенное изображение">
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeImageModal">Закрыть</button>
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
      users: [],
      currentUser: null,
      selectedUserId: '',
      loading: false,
      isEditing: false,
      editingId: null,
      formData: {
        name: '',
        country: '',
        website: ''
      },
      // Переменные для работы с картинками
      logoFile: null,
      logoPreview: null,
      currentLogoUrl: null,
      // Модальное окно
      showImageModal: false,
      modalImageUrl: null,
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
        let url = `${API_BASE}/manufacturers/`;
        
        // Добавляем фильтр по пользователю для суперпользователя
        if (this.currentUser && this.currentUser.is_superuser && this.selectedUserId) {
          url += `?user_id=${this.selectedUserId}`;
        }

        const response = await axios.get(url, { withCredentials: true });
        this.items = response.data;
      } catch (error) {
        console.error('Ошибка загрузки производителей:', error);
        this.showNotification('Ошибка загрузки данных', 'danger');
      } finally {
        this.loading = false;
      }
    },

    // Загрузка пользователей (для суперпользователя)
    async loadUsers() {
      try {
        const response = await axios.get(`${API_BASE}/users/`, { withCredentials: true });
        this.users = response.data;
      } catch (error) {
        console.error('Ошибка загрузки пользователей:', error);
      }
    },

    // Получение информации о текущем пользователе
    async getCurrentUser() {
      try {
        // Получаем текущего пользователя через первый запрос
        const response = await axios.get(`${API_BASE}/manufacturers/`, { withCredentials: true });
        
        // Если запрос прошел успешно, пользователь авторизован
        // Для простоты считаем что пользователь admin если есть права на просмотр всех данных
        this.currentUser = {
          username: 'admin', // В реальном приложении нужно получать из API
          is_superuser: true
        };
      } catch (error) {
        console.error('Ошибка получения информации о пользователе:', error);
      }
    },

    // Обработка загрузки логотипа
    handleLogoUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.logoFile = file;
        
        // Создаем preview
        const reader = new FileReader();
        reader.onload = (e) => {
          this.logoPreview = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    },

    // Создание производителя с картинкой
    async createItem() {
      this.loading = true;
      try {
        const formData = new FormData();
        
        // Добавляем текстовые данные
        formData.append('name', this.formData.name);
        formData.append('country', this.formData.country);
        if (this.formData.website) {
          formData.append('website', this.formData.website);
        }
        
        // Добавляем файл, если есть
        if (this.logoFile) {
          formData.append('logo', this.logoFile);
        }

        const response = await axios.post(`${API_BASE}/manufacturers/`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          },
          withCredentials: true
        });
        
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
      this.formData = { 
        name: item.name,
        country: item.country,
        website: item.website || ''
      };
      this.currentLogoUrl = item.logo_url;
      this.logoPreview = null;
      this.logoFile = null;
    },

    // Обновление производителя с картинкой
    async updateItem() {
      this.loading = true;
      try {
        const formData = new FormData();
        
        // Добавляем текстовые данные
        formData.append('name', this.formData.name);
        formData.append('country', this.formData.country);
        if (this.formData.website) {
          formData.append('website', this.formData.website);
        }
        
        // Добавляем файл, если есть новый
        if (this.logoFile) {
          formData.append('logo', this.logoFile);
        }

        const response = await axios.put(`${API_BASE}/manufacturers/${this.editingId}/`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          },
          withCredentials: true
        });
        
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
        await axios.delete(`${API_BASE}/manufacturers/${id}/`, { withCredentials: true });
        this.items = this.items.filter(item => item.id !== id);
        this.showNotification('Производитель успешно удален!', 'success');
      } catch (error) {
        console.error('Ошибка удаления производителя:', error);
        this.showNotification('Ошибка удаления производителя', 'danger');
      }
    },

    // Модальное окно для изображений
    openImageModal(imageUrl) {
      this.modalImageUrl = imageUrl;
      this.showImageModal = true;
    },

    closeImageModal() {
      this.showImageModal = false;
      this.modalImageUrl = null;
    },

    // Стиль для бейджа пользователя
    getUserBadgeClass(username) {
      return username === 'admin' ? 'bg-warning text-dark' : 'bg-secondary';
    },

    // Сброс фильтра
    clearFilter() {
      this.selectedUserId = '';
      this.loadData();
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
      this.logoFile = null;
      this.logoPreview = null;
      this.currentLogoUrl = null;
      if (this.$refs.logoInput) {
        this.$refs.logoInput.value = '';
      }
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
  async mounted() {
    await this.getCurrentUser();
    await this.loadUsers();
    await this.loadData();
  }
}
</script>

<style scoped>
.manufacturers-view {
  min-height: 100vh;
  background: #f8f9fa;
}

.user-info {
  text-align: center;
  font-weight: bold;
}

.modal {
  background: rgba(0,0,0,0.8);
}
</style>