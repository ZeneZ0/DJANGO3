<script>
import axios from 'axios';

export default {
  name: 'BackendDataView',
  data() {
    return {
      allData: {
        componentTypes: [],
        manufacturers: [],
        components: [],
        configurations: []
      },
      activeData: {},
      loading: false,
      activeEndpoint: null,
      error: null,
      componentSearch: '',
      componentTypeFilter: '',
      endpoints: [
        { key: 'all', name: 'Все' },
        { key: 'componentTypes', name: 'Типы' },
        { key: 'manufacturers', name: 'Производители' },
        { key: 'components', name: 'Компоненты' },
        { key: 'configurations', name: 'Конфигурации' }
      ]
    }
  },
  computed: {
    filteredComponents() {
      let components = this.allData.components;
      
      if (this.componentSearch) {
        components = components.filter(c =>
          c.name.toLowerCase().includes(this.componentSearch.toLowerCase())
        );
      }
      
      if (this.componentTypeFilter) {
        components = components.filter(c =>
          c.component_type == this.componentTypeFilter
        );
      }
      
      return components;
    },
    
    showStats() {
      return this.activeEndpoint === 'all';
    },
    
    stats() {
      return {
        componentTypesCount: this.allData.componentTypes.length,
        manufacturersCount: this.allData.manufacturers.length,
        componentsCount: this.allData.components.length,
        configurationsCount: this.allData.configurations.length
      };
    },
    
    componentTypes() {
      return this.allData.componentTypes;
    }
  },
  methods: {
    async loadAllData() {
      this.loading = true;
      this.error = null;
      this.activeEndpoint = 'all';
      
      try {
        const urls = [
          '/api/component-types/',
          '/api/manufacturers/', 
          '/api/components/',
          '/api/configurations/'
        ];
        
        const requests = urls.map(url => 
          axios.get(url).catch(() => ({ data: [] }))
        );
        
        const responses = await Promise.all(requests);
        
        this.allData = {
          componentTypes: responses[0].data,
          manufacturers: responses[1].data,
          components: responses[2].data,
          configurations: responses[3].data
        };
        
        this.activeData = { ...this.allData };
        
      } catch (error) {
        console.error('Ошибка загрузки:', error);
        this.error = 'Не удалось загрузить данные';
      } finally {
        this.loading = false;
      }
    },
    
    async loadSpecificData(endpointKey) {
      if (this.loading) return;
      
      this.loading = true;
      this.error = null;
      this.activeEndpoint = endpointKey;
      this.activeData = {};
      
      try {
        let url, dataKey;
        
        switch (endpointKey) {
          case 'componentTypes':
            url = '/api/component-types/';
            dataKey = 'componentTypes';
            break;
          case 'manufacturers':
            url = '/api/manufacturers/';
            dataKey = 'manufacturers';
            break;
          case 'components':
            url = '/api/components/';
            dataKey = 'components';
            break;
          case 'configurations':
            url = '/api/configurations/';
            dataKey = 'configurations';
            break;
          default:
            return;
        }
        
        const response = await axios.get(url);
        this.allData[dataKey] = response.data;
        this.activeData[dataKey] = response.data;
        
      } catch (error) {
        console.error(`Ошибка загрузки ${endpointKey}:`, error);
        this.error = `Не удалось загрузить ${endpointKey}`;
      } finally {
        this.loading = false;
      }
    },
    
    getComponentTypeName(typeId) {
      const type = this.allData.componentTypes.find(t => t.id === typeId);
      return type ? type.name : `Тип #${typeId}`;
    },
    
    getManufacturerName(manufacturerId) {
      const manufacturer = this.allData.manufacturers.find(m => m.id === manufacturerId);
      return manufacturer ? manufacturer.name : `Произв. #${manufacturerId}`;
    },
    
    getComponentName(componentId) {
      const component = this.allData.components.find(c => c.id === componentId);
      return component ? component.name : `Компонент #${componentId}`;
    }
  },
  mounted() {
    this.loadAllData();
  }
}
</script>

<template>
  <div class="backend-data">
    <h1>Данные с сервера</h1>
    
    <div class="alert alert-info mb-3">
      Цены в долларах ($)
    </div>

    <div class="controls mb-4">
      <button @click="loadAllData" class="btn btn-primary me-2" :disabled="loading">
        Загрузить все
      </button>
      
      <div class="btn-group">
        <button 
          v-for="endpoint in endpoints" 
          :key="endpoint.key"
          @click="loadSpecificData(endpoint.key)"
          :class="['btn btn-outline-secondary', { active: activeEndpoint === endpoint.key }]"
          :disabled="loading"
        >
          {{ endpoint.name }}
        </button>
      </div>
    </div>

    
    <div v-if="activeData.components" class="mb-4">
      <h3>Компоненты</h3>
      
      <div class="row mb-3">
        <div class="col-md-6">
          <input v-model="componentSearch" placeholder="Поиск..." class="form-control">
        </div>
        <div class="col-md-6">
          <select v-model="componentTypeFilter" class="form-select">
            <option value="">Все типы</option>
            <option v-for="type in componentTypes" :key="type.id" :value="type.id">
              {{ type.name }}
            </option>
          </select>
        </div>
      </div>
      
      <div class="row">
        <div 
          v-for="item in filteredComponents" 
          :key="item.id" 
          class="col-md-4 mb-3"
        >
          <div class="card h-100" :class="{ 'border-danger': !item.in_stock }">
            <div class="card-body">
              <h5 class="card-title">{{ item.name }}</h5>
              <p class="card-text">
                Тип: <span class="badge bg-primary">{{ getComponentTypeName(item.component_type) }}</span><br>
                Производитель: <span class="badge bg-info">{{ getManufacturerName(item.manufacturer) }}</span><br>
                Цена: <strong class="text-success">${{ item.price }}</strong>
              </p>
              <p :class="item.in_stock ? 'text-success' : 'text-danger'">
                {{ item.in_stock ? 'В наличии' : 'Нет в наличии' }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

   
    <div v-if="activeData.manufacturers" class="mb-4">
      <h3>Производители</h3>
      <div class="row">
        <div v-for="item in activeData.manufacturers" :key="item.id" class="col-md-4 mb-3">
          <div class="card h-100">
            <div class="card-body">
              <h5 class="card-title">{{ item.name }}</h5>
              <p class="card-text">
                Страна: <span class="badge bg-info">{{ item.country }}</span><br>
                Сайт: <a v-if="item.website" :href="item.website" target="_blank">Перейти</a>
                <span v-else class="text-muted">-</span>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

   
    <div v-if="activeData.componentTypes" class="mb-4">
      <h3>Типы компонентов</h3>
      <div class="row">
        <div v-for="item in activeData.componentTypes" :key="item.id" class="col-md-4 mb-3">
          <div class="card h-100">
            <div class="card-body">
              <h5 class="card-title">{{ item.name }}</h5>
              <p class="card-text">{{ item.description || '-' }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

   
    <div v-if="activeData.configurations" class="mb-4">
      <h3>Конфигурации ПК</h3>
      <div class="row">
        <div v-for="item in activeData.configurations" :key="item.id" class="col-md-6 mb-3">
          <div class="card h-100">
            <div class="card-body">
              <h5 class="card-title">{{ item.name }}</h5>
              <p class="card-text">{{ item.description || '-' }}</p>
              <p class="fw-bold text-success">Общая стоимость: ${{ item.total_price }}</p>
              <div class="small">
                <p class="mb-1"><strong>Компоненты:</strong></p>
                <ul class="mb-0">
                  <li>Процессор: {{ getComponentName(item.cpu) }}</li>
                  <li>Видеокарта: {{ getComponentName(item.gpu) }}</li>
                  <li>Материнская плата: {{ getComponentName(item.motherboard) }}</li>
                  <li>Память: {{ getComponentName(item.ram) }}</li>
                  <li>Накопитель: {{ getComponentName(item.storage) }}</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    
    <div v-if="showStats" class="mb-4">
      <h3>Статистика</h3>
      <div class="row">
        <div class="col-md-3">
          <div class="card">
            <div class="card-body text-center">
              <h5>Типы</h5>
              <h2>{{ stats.componentTypesCount }}</h2>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card">
            <div class="card-body text-center">
              <h5>Производители</h5>
              <h2>{{ stats.manufacturersCount }}</h2>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card">
            <div class="card-body text-center">
              <h5>Компоненты</h5>
              <h2>{{ stats.componentsCount }}</h2>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card">
            <div class="card-body text-center">
              <h5>Конфигурации</h5>
              <h2>{{ stats.configurationsCount }}</h2>
            </div>
          </div>
        </div>
      </div>
    </div>

   
    <div v-if="error" class="alert alert-danger">
      <h5>Ошибка загрузки данных</h5>
      <p>{{ error }}</p>
      <p class="mb-0">Убедитесь, что сервер Django запущен</p>
    </div>
  </div>
</template>



<style scoped>
.backend-data {
  padding: 20px;
}

.controls {
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
}

.btn-group {
  display: flex;
  gap: 5px;
}

.btn-group .btn {
  flex: 1;
}

.card {
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-2px);
}

.card.border-danger {
  border-width: 2px;
}

.small ul {
  margin-bottom: 0;
  padding-left: 20px;
}

.small li {
  margin-bottom: 2px;
}
</style>