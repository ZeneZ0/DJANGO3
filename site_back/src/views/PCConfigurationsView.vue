<!-- site_back/src/views/PCConfigurationsView.vue -->
<template>
  <div class="container mt-4">
    <h1 class="mb-4">Управление конфигурациями ПК</h1>
    
    <div class="alert alert-info mb-3">
      Цены в долларах ($)
    </div>

    <!-- Форма -->
    <div class="card mb-4">
      <div class="card-header">
        <h5 class="mb-0">{{ isEditing ? 'Редактировать' : 'Добавить' }} конфигурацию</h5>
      </div>
      <div class="card-body">
        <form @submit.prevent="saveConfig">
          <div class="mb-3">
            <label class="form-label">Название:</label>
            <input v-model="form.name" type="text" class="form-control" required>
          </div>
          
          <div class="mb-3">
            <label class="form-label">Описание:</label>
            <textarea v-model="form.description" class="form-control" rows="2"></textarea>
          </div>

          <h5>Выбор компонентов</h5>
          
          <div class="row">
            <div class="col-md-6 mb-3" v-for="type in componentTypes" :key="type.id">
              <label class="form-label">{{ type.name }}:</label>
              <select v-model="form[getFieldName(type.name)]" class="form-select" required>
                <option value="">Выберите</option>
                <option 
                  v-for="comp in getComponents(type.id)" 
                  :key="comp.id" 
                  :value="comp.id"
                >
                  {{ comp.name }} (${{ comp.price }})
                </option>
              </select>
            </div>
          </div>

          <div class="alert alert-light mb-3">
            <strong>Общая стоимость: ${{ calculateTotal() }}</strong>
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

    <!-- Список конфигураций -->
    <div class="card">
      <div class="card-header d-flex justify-content-between">
        <h5 class="mb-0">Список конфигураций ({{ configs.length }})</h5>
        <button @click="loadData" class="btn btn-outline-primary btn-sm">Обновить</button>
      </div>
      
      <div class="card-body">
        <div v-if="loading" class="text-center py-3">
          <div class="spinner-border text-primary"></div>
        </div>
        
        <div v-else-if="configs.length === 0" class="text-center py-4 text-muted">
          Конфигураций нет
        </div>
        
        <div v-else class="table-responsive">
          <table class="table table-striped">
            <thead>
              <tr>
                <th>ID</th>
                <th>Название</th>
                <th>Стоимость</th>
                <th>Дата</th>
                <th>Действия</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="config in configs" :key="config.id">
                <td>{{ config.id }}</td>
                <td><strong>{{ config.name }}</strong></td>
                <td class="text-success"><strong>${{ config.total_price }}</strong></td>
                <td>{{ formatDate(config.created_at) }}</td>
                <td>
                  <button @click="editConfig(config)" class="btn btn-warning btn-sm me-1">Изменить</button>
                  <button @click="showDetails(config)" class="btn btn-info btn-sm me-1">Детали</button>
                  <button @click="deleteConfig(config.id)" class="btn btn-danger btn-sm">Удалить</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Модальное окно деталей -->
    <div v-if="selectedConfig" class="modal fade show d-block" style="background: rgba(0,0,0,0.5)">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Детали конфигурации</h5>
            <button type="button" class="btn-close" @click="selectedConfig = null"></button>
          </div>
          
          <div class="modal-body">
            <p><strong>Название:</strong> {{ selectedConfig.name }}</p>
            <p><strong>Описание:</strong> {{ selectedConfig.description || '-' }}</p>
            <p><strong>Общая стоимость:</strong> ${{ selectedConfig.total_price }}</p>
            
            <div class="mt-3">
              <h6>Компоненты:</h6>
              <ul class="list-group">
                <li class="list-group-item" v-for="type in componentTypes" :key="type.id">
                  <strong>{{ type.name }}:</strong> 
                  {{ getComponentName(selectedConfig[getFieldName(type.name)]) }}
                </li>
              </ul>
            </div>
          </div>
          
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="selectedConfig = null">Закрыть</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'PCConfigurationsView',
  data() {
    return {
      configs: [],
      components: [],
      componentTypes: [],
      loading: false,
      isEditing: false,
      editId: null,
      selectedConfig: null,
      form: {
        name: '',
        description: '',
        cpu: '',
        gpu: '',
        motherboard: '',
        ram: '',
        storage: '',
        power_supply: '',
        case: ''
      }
    }
  },
  methods: {
    async loadData() {
      this.loading = true;
      try {
        const response = await axios.get('/api/configurations/');
        this.configs = response.data;
      } catch (error) {
        console.error('Ошибка загрузки:', error);
        alert('Ошибка загрузки данных');
      }
      this.loading = false;
    },

    async loadComponents() {
      try {
        const [comps, types] = await Promise.all([
          axios.get('/api/components/'),
          axios.get('/api/component-types/')
        ]);
        this.components = comps.data;
        this.componentTypes = types.data;
      } catch (error) {
        console.error('Ошибка загрузки компонентов:', error);
      }
    },

    getFieldName(typeName) {
      const map = {
        'Процессор': 'cpu',
        'Видеокарта': 'gpu',
        'Материнская плата': 'motherboard',
        'Оперативная память': 'ram',
        'Накопитель': 'storage',
        'Блок питания': 'power_supply',
        'Корпус': 'case'
      };
      return map[typeName] || '';
    },

    getComponents(typeId) {
      return this.components.filter(c => c.component_type === typeId);
    },

    getComponentName(compId) {
      const comp = this.components.find(c => c.id === compId);
      return comp ? comp.name : 'Неизвестно';
    },

    calculateTotal() {
      let total = 0;
      const fields = ['cpu', 'gpu', 'motherboard', 'ram', 'storage', 'power_supply', 'case'];
      
      fields.forEach(field => {
        if (this.form[field]) {
          const comp = this.components.find(c => c.id === this.form[field]);
          if (comp) total += parseFloat(comp.price);
        }
      });
      
      return total;
    },

    async saveConfig() {
      this.loading = true;
      try {
        if (this.isEditing) {
          await axios.put(`/api/configurations/${this.editId}/`, this.form);
        } else {
          await axios.post('/api/configurations/', this.form);
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

    editConfig(config) {
      this.isEditing = true;
      this.editId = config.id;
      this.form = { ...config };
    },

    cancelEdit() {
      this.resetForm();
    },

    async deleteConfig(id) {
      if (!confirm('Удалить конфигурацию?')) return;
      
      try {
        await axios.delete(`/api/configurations/${id}/`);
        this.configs = this.configs.filter(c => c.id !== id);
      } catch (error) {
        console.error('Ошибка удаления:', error);
        alert('Ошибка удаления');
      }
    },

    showDetails(config) {
      this.selectedConfig = config;
    },

    formatDate(dateStr) {
      return new Date(dateStr).toLocaleDateString();
    },

    resetForm() {
      this.isEditing = false;
      this.editId = null;
      this.form = {
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
    }
  },
  mounted() {
    this.loadData();
    this.loadComponents();
  }
}
</script>

<style scoped>
.table-responsive {
  overflow-x: auto;
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}
</style>