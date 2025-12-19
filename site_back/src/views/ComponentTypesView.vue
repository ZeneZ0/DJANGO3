<script>
import axios from 'axios';

export default {
  name: 'ComponentTypesView',
  data() {
    return {
      types: [],
      loading: false,
      isEditing: false,
      editId: null,
      form: {
        name: '',
        description: ''
      }
    }
  },
  methods: {
    async loadData() {
      this.loading = true;
      try {
        const response = await axios.get('/api/component-types/');
        this.types = response.data;
      } catch (error) {
        console.error('Ошибка загрузки:', error);
        alert('Ошибка загрузки данных');
      }
      this.loading = false;
    },

    async saveType() {
      this.loading = true;
      try {
        if (this.isEditing) {
          await axios.put(`/api/component-types/${this.editId}/`, this.form);
        } else {
          await axios.post('/api/component-types/', this.form);
        }
        
        await this.loadData();
        this.resetForm();
        alert('Сохранено успешно');
      } catch (error) {
        console.error('Ошибка сохранения:', error);
        alert('Ошибка сохранения');
      }
      this.loading = false;
    },

    editType(type) {
      this.isEditing = true;
      this.editId = type.id;
      this.form = { ...type };
    },

    cancelEdit() {
      this.resetForm();
    },

    async deleteType(id) {
      if (!confirm('Удалить тип компонента?')) return;
      
      try {
        await axios.delete(`/api/component-types/${id}/`);
        this.types = this.types.filter(t => t.id !== id);
      } catch (error) {
        console.error('Ошибка удаления:', error);
        alert('Ошибка удаления');
      }
    },

    resetForm() {
      this.isEditing = false;
      this.editId = null;
      this.form = {
        name: '',
        description: ''
      };
    }
  },
  mounted() {
    this.loadData();
  }
}
</script>

<template>
  <div class="container mt-4">
    <h1 class="mb-4">Управление типами компонентов</h1>

    <div class="card mb-4">
      <div class="card-header">
        <h5 class="mb-0">{{ isEditing ? 'Редактировать' : 'Добавить' }} тип</h5>
      </div>
      <div class="card-body">
        <form @submit.prevent="saveType">
          <div class="mb-3">
            <label class="form-label">Название *</label>
            <input v-model="form.name" type="text" class="form-control" required>
          </div>
          
          <div class="mb-3">
            <label class="form-label">Описание</label>
            <textarea v-model="form.description" class="form-control" rows="3"></textarea>
          </div>
          
          <div>
            <button type="submit" class="btn btn-success" :disabled="loading">
              {{ isEditing ? 'Сохранить' : 'Добавить' }}
            </button>
            <button type="button" v-if="isEditing" @click="cancelEdit" class="btn btn-secondary ms-2">
              Отмена
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Список типов -->
    <div class="card">
      <div class="card-header d-flex justify-content-between">
        <h5 class="mb-0">Список типов ({{ types.length }})</h5>
        <button @click="loadData" class="btn btn-outline-primary btn-sm">Обновить</button>
      </div>
      
      <div class="card-body">
        <div v-if="loading" class="text-center py-3">
          <div class="spinner-border text-primary"></div>
        </div>
        
        <div v-else-if="types.length === 0" class="text-center py-4 text-muted">
          Типов нет
        </div>
        
        <div v-else class="table-responsive">
          <table class="table table-striped">
            <thead>
              <tr>
                <th>ID</th>
                <th>Название</th>
                <th>Описание</th>
                <th>Действия</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="type in types" :key="type.id">
                <td>{{ type.id }}</td>
                <td><strong>{{ type.name }}</strong></td>
                <td>{{ type.description || '-' }}</td>
                <td>
                  <button @click="editType(type)" class="btn btn-warning btn-sm me-1">Изменить</button>
                  <button @click="deleteType(type.id)" class="btn btn-danger btn-sm">Удалить</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>



<style scoped>
.table-responsive {
  overflow-x: auto;
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}
</style>