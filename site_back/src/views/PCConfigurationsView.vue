<script>
import axios from 'axios';

function getCookie(name) {
  let cookieValue = null
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}

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
      columnFilters: {
        name: '',
        price_min: '',
        price_max: '',
        date_from: '',
        date_to: ''
      },
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
  computed: {
    filteredConfigs() {
      let filtered = this.configs
      
      if (this.columnFilters.name) {
        filtered = filtered.filter(config => 
          config.name.toLowerCase().includes(this.columnFilters.name.toLowerCase())
        )
      }
      
      if (this.columnFilters.price_min) {
        filtered = filtered.filter(config => 
          config.total_price >= parseFloat(this.columnFilters.price_min)
        )
      }
      
      if (this.columnFilters.price_max) {
        filtered = filtered.filter(config => 
          config.total_price <= parseFloat(this.columnFilters.price_max)
        )
      }
      
      if (this.columnFilters.date_from) {
        filtered = filtered.filter(config => 
          new Date(config.created_at) >= new Date(this.columnFilters.date_from)
        )
      }
      
      if (this.columnFilters.date_to) {
        filtered = filtered.filter(config => 
          new Date(config.created_at) <= new Date(this.columnFilters.date_to)
        )
      }
      
      return filtered
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

    async exportToExcel() {
  this.loading = true
  try {
    const params = {}
    if (this.columnFilters.name) params.name = this.columnFilters.name
    if (this.columnFilters.price_min) params.price_min = this.columnFilters.price_min
    if (this.columnFilters.price_max) params.price_max = this.columnFilters.price_max
    if (this.columnFilters.date_from) params.date_from = this.columnFilters.date_from
    if (this.columnFilters.date_to) params.date_to = this.columnFilters.date_to

    const response = await axios.get('/api/configurations/export_excel/', {
      responseType: 'blob',
      params: params,
      headers: {
        'X-CSRFToken': getCookie('csrftoken')
      }
    })
    
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `configurations_${new Date().toISOString().split('T')[0]}.xlsx`)
    document.body.appendChild(link)
    link.click()
    link.remove()
    
    alert('Файл успешно экспортирован')
  } catch (error) {
    console.error('Ошибка экспорта:', error)
    alert('Ошибка при экспорте файла')
  }
  this.loading = false
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
      return comp ? `${comp.name} ($${comp.price})` : 'Неизвестно';
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
    },

    resetFilters() {
      this.columnFilters = {
        name: '',
        price_min: '',
        price_max: '',
        date_from: '',
        date_to: ''
      }
    }
  },
  mounted() {
    this.loadData();
    this.loadComponents();
  }
}
</script>

<template>
  <div class="container mt-4">
    <h1 class="mb-4">Управление конфигурациями ПК</h1>
    
    <div class="alert alert-info mb-3">
      Цены в долларах ($)
    </div>

   
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

   
    <div class="card mb-3">
      <div class="card-header">
        <h6 class="mb-0">Фильтры по столбцам</h6>
      </div>
      <div class="card-body">
        <div class="row mb-2">
          <div class="col-md-4">
            <input v-model="columnFilters.name" 
                   placeholder="Название" 
                   class="form-control form-control-sm">
          </div>
          <div class="col-md-4">
            <div class="input-group input-group-sm">
              <input v-model="columnFilters.price_min" 
                     type="number" 
                     placeholder="Стоимость от" 
                     class="form-control">
              <input v-model="columnFilters.price_max" 
                     type="number" 
                     placeholder="Стоимость до" 
                     class="form-control">
            </div>
          </div>
          <div class="col-md-4">
            <div class="input-group input-group-sm">
              <input v-model="columnFilters.date_from" 
                     type="date" 
                     placeholder="Дата от" 
                     class="form-control">
              <input v-model="columnFilters.date_to" 
                     type="date" 
                     placeholder="Дата до" 
                     class="form-control">
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-md-12 d-flex justify-content-end">
            <button @click="resetFilters" class="btn btn-sm btn-outline-secondary me-2">
              Сбросить фильтры
            </button>
            <button @click="exportToExcel" class="btn btn-sm btn-success" :disabled="loading">
              📊 Экспорт в Excel
            </button>
          </div>
        </div>
      </div>
    </div>

   
    <div class="card">
      <div class="card-header d-flex justify-content-between">
        <h5 class="mb-0">Список конфигураций ({{ filteredConfigs.length }})</h5>
        <button @click="loadData" class="btn btn-outline-primary btn-sm">Обновить</button>
      </div>
      
      <div class="card-body">
        <div v-if="loading" class="text-center py-3">
          <div class="spinner-border text-primary"></div>
        </div>
        
        <div v-else-if="filteredConfigs.length === 0" class="text-center py-4 text-muted">
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
              <tr v-for="config in filteredConfigs" :key="config.id">
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



<style scoped>
.table-responsive {
  overflow-x: auto;
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}

.input-group-sm input {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}
</style>