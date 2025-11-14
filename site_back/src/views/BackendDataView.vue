<!-- site_back/src/views/BackendDataView.vue -->
<template>
  <div class="backend-view">
    <h1>📡 Данные с бекенда Django</h1>
    
    <div class="currency-note">
      💰 Все цены в долларах США ($)
    </div>
    
    <div class="controls">
      <button @click="loadAllData" class="load-btn" :disabled="loading">
        {{ loading ? '🔄 Загрузка...' : '📥 Загрузить все данные' }}
      </button>
      
      <div class="data-selector">
        <button 
          v-for="endpoint in endpoints" 
          :key="endpoint.key"
          @click="loadSpecificData(endpoint.key)"
          :class="['endpoint-btn', { active: activeEndpoint === endpoint.key }]"
          :disabled="loading"
        >
          {{ endpoint.name }}
        </button>
      </div>
    </div>

    <!-- Уведомления -->
    <div v-if="notification.message" :class="['notification', notification.type]">
      {{ notification.message }}
    </div>

    <!-- Компоненты -->
    <div v-if="activeData.componentTypes" class="data-section">
      <h2>🏷️ Типы компонентов</h2>
      <div class="items-grid">
        <div v-for="item in activeData.componentTypes" :key="item.id" class="item-card">
          <h3>{{ item.name }}</h3>
          <p>{{ item.description || 'Описание отсутствует' }}</p>
        </div>
      </div>
    </div>

    <!-- Производители -->
    <div v-if="activeData.manufacturers" class="data-section">
      <h2>🏭 Производители</h2>
      <div class="items-grid">
        <div v-for="item in activeData.manufacturers" :key="item.id" class="item-card">
          <h3>{{ item.name }}</h3>
          <p>🌍 {{ item.country }}</p>
          <p v-if="item.website">🔗 {{ item.website }}</p>
        </div>
      </div>
    </div>

    <!-- Компоненты -->
    <div v-if="activeData.components" class="data-section">
      <h2>💻 Компоненты</h2>
      <div class="search-controls">
        <input v-model="componentSearch" placeholder="Поиск компонентов..." class="search-input">
        <select v-model="componentTypeFilter" class="filter-select">
          <option value="">Все типы</option>
          <option v-for="type in componentTypes" :key="type.id" :value="type.id">
            {{ type.name }}
          </option>
        </select>
      </div>
      
      <div class="items-grid">
        <div 
          v-for="item in filteredComponents" 
          :key="item.id" 
          class="item-card component-card"
          :class="{ 'out-of-stock': !item.in_stock }"
        >
          <h3>{{ item.name }}</h3>
          <p>🏷️ {{ getComponentTypeName(item.component_type) }}</p>
          <p>🏭 {{ getManufacturerName(item.manufacturer) }}</p>
          <p class="price">{{ formatPrice(item.price) }}</p>
          <p :class="item.in_stock ? 'in-stock' : 'out-of-stock-text'">
            {{ item.in_stock ? '✅ В наличии' : '❌ Нет в наличии' }}
          </p>
          <div v-if="item.specifications && Object.keys(item.specifications).length > 0" class="specs">
            <p><strong>Характеристики:</strong></p>
            <ul>
              <li v-for="(value, key) in item.specifications" :key="key">
                {{ key }}: {{ value }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Конфигурации -->
    <div v-if="activeData.configurations" class="data-section">
      <h2>🖥️ Конфигурации ПК</h2>
      <div class="items-grid">
        <div v-for="item in activeData.configurations" :key="item.id" class="item-card config-card">
          <h3>{{ item.name }}</h3>
          <p>{{ item.description || 'Без описания' }}</p>
          <p class="total-price">Итого: {{ formatPrice(item.total_price) }}</p>
          <div class="config-details">
            <p><strong>Компоненты:</strong></p>
            <ul>
              <li>⚙️ Процессор: {{ getComponentName(item.cpu) }}</li>
              <li>🎮 Видеокарта: {{ getComponentName(item.gpu) }}</li>
              <li>🔌 Мат. плата: {{ getComponentName(item.motherboard) }}</li>
              <li>💾 Память: {{ getComponentName(item.ram) }}</li>
              <li>💿 Накопитель: {{ getComponentName(item.storage) }}</li>
              <li>⚡ БП: {{ getComponentName(item.power_supply) }}</li>
              <li>📦 Корпус: {{ getComponentName(item.case) }}</li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Статистика -->
    <div v-if="showStats" class="stats-section">
      <h2>📊 Статистика</h2>
      <div class="stats-grid">
        <div class="stat-card">
          <h3>🏷️ Типов компонентов</h3>
          <p class="stat-number">{{ stats.componentTypesCount }}</p>
        </div>
        <div class="stat-card">
          <h3>🏭 Производителей</h3>
          <p class="stat-number">{{ stats.manufacturersCount }}</p>
        </div>
        <div class="stat-card">
          <h3>💻 Компонентов</h3>
          <p class="stat-number">{{ stats.componentsCount }}</p>
        </div>
        <div class="stat-card">
          <h3>🖥️ Конфигураций</h3>
          <p class="stat-number">{{ stats.configurationsCount }}</p>
        </div>
      </div>
    </div>

    <!-- Ошибка загрузки -->
    <div v-if="error" class="error-section">
      <h2>❌ Ошибка загрузки данных</h2>
      <p>{{ error }}</p>
      <p class="help-text">
        Убедитесь, что Django сервер запущен на порту 8000:
        <code>python manage.py runserver</code>
      </p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

const API_BASE = '/api';

export default {
  name: 'BackendDataView',
  data() {
    return {
      // Все данные
      allData: {
        componentTypes: [],
        manufacturers: [],
        components: [],
        configurations: []
      },
      // Активные данные для отображения
      activeData: {},
      // Состояние загрузки
      loading: false,
      // Активный endpoint
      activeEndpoint: null,
      // Ошибки
      error: null,
      // Уведомления
      notification: {
        message: '',
        type: ''
      },
      // Поиск и фильтры
      componentSearch: '',
      componentTypeFilter: '',
      // Endpoints
      endpoints: [
        { key: 'all', name: 'Все данные' },
        { key: 'componentTypes', name: 'Типы' },
        { key: 'manufacturers', name: 'Производители' },
        { key: 'components', name: 'Компоненты' },
        { key: 'configurations', name: 'Конфигурации' }
      ]
    }
  },
  computed: {
    // Фильтрованные компоненты
    filteredComponents() {
      let components = this.allData.components;
      
      // Поиск по названию
      if (this.componentSearch) {
        components = components.filter(component =>
          component.name.toLowerCase().includes(this.componentSearch.toLowerCase())
        );
      }
      
      // Фильтрация по типу
      if (this.componentTypeFilter) {
        components = components.filter(component =>
          component.component_type == this.componentTypeFilter
        );
      }
      
      return components;
    },
    
    // Статистика
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
    // Форматирование цены в доллары
    formatPrice(price) {
      if (!price) return '$0';
      
      // Просто добавляем знак доллара к существующей цене
      return `$${price}`;
    },

    // Загрузка всех данных
    async loadAllData() {
      this.loading = true;
      this.error = null;
      this.activeEndpoint = 'all';
      
      try {
        const endpoints = [
          'component-types',
          'manufacturers', 
          'components',
          'configurations'
        ];
        
        const requests = endpoints.map(endpoint => 
          axios.get(`${API_BASE}/${endpoint}/`).catch(error => {
            console.error(`Ошибка загрузки ${endpoint}:`, error);
            return { data: [] };
          })
        );
        
        const responses = await Promise.all(requests);
        
        this.allData = {
          componentTypes: responses[0].data,
          manufacturers: responses[1].data,
          components: responses[2].data,
          configurations: responses[3].data
        };
        
        this.activeData = { ...this.allData };
        this.showNotification('Данные успешно загружены!', 'success');
        
      } catch (error) {
        console.error('Ошибка загрузки данных:', error);
        this.error = 'Не удалось загрузить данные с сервера';
        this.showNotification('Ошибка загрузки данных', 'error');
      } finally {
        this.loading = false;
      }
    },
    
    // Загрузка конкретных данных
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
            url = 'component-types';
            dataKey = 'componentTypes';
            break;
          case 'manufacturers':
            url = 'manufacturers';
            dataKey = 'manufacturers';
            break;
          case 'components':
            url = 'components';
            dataKey = 'components';
            break;
          case 'configurations':
            url = 'configurations';
            dataKey = 'configurations';
            break;
          default:
            return;
        }
        
        const response = await axios.get(`${API_BASE}/${url}/`);
        this.allData[dataKey] = response.data;
        this.activeData[dataKey] = response.data;
        
        this.showNotification(`Данные ${this.getEndpointName(endpointKey)} загружены`, 'success');
        
      } catch (error) {
        console.error(`Ошибка загрузки ${endpointKey}:`, error);
        this.error = `Не удалось загрузить ${this.getEndpointName(endpointKey)}`;
        this.showNotification(`Ошибка загрузки ${this.getEndpointName(endpointKey)}`, 'error');
      } finally {
        this.loading = false;
      }
    },
    
    // Вспомогательные методы
    getEndpointName(key) {
      const names = {
        componentTypes: 'типов компонентов',
        manufacturers: 'производителей',
        components: 'компонентов',
        configurations: 'конфигураций'
      };
      return names[key] || key;
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
    },
    
    showNotification(message, type = 'info') {
      this.notification = { message, type };
      setTimeout(() => {
        this.notification.message = '';
      }, 4000);
    }
  },
  mounted() {
    // Автоматически загружаем данные при монтировании
    this.loadAllData();
  }
}
</script>

<style scoped>
.backend-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.currency-note {
  background: #e8f4fd;
  padding: 10px 15px;
  border-radius: 5px;
  margin-bottom: 15px;
  border-left: 4px solid #3498db;
  font-weight: bold;
  color: #2c3e50;
  text-align: center;
}

.controls {
  background: white;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.load-btn {
  background: #3498db;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  margin-bottom: 15px;
}

.load-btn:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
}

.data-selector {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.endpoint-btn {
  background: #ecf0f1;
  border: 2px solid #bdc3c7;
  padding: 8px 16px;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.endpoint-btn:hover {
  background: #d5dbdb;
}

.endpoint-btn.active {
  background: #3498db;
  color: white;
  border-color: #3498db;
}

.endpoint-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.data-section {
  background: white;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 15px;
}

.item-card {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  border-left: 4px solid #3498db;
}

.component-card.out-of-stock {
  opacity: 0.7;
  border-left-color: #e74c3c;
}

.config-card {
  border-left-color: #9b59b6;
}

.item-card h3 {
  margin: 0 0 10px 0;
  color: #2c3e50;
}

.item-card p {
  margin: 5px 0;
  color: #7f8c8d;
}

.price {
  color: #27ae60 !important;
  font-weight: bold;
  font-size: 1.1em;
}

.total-price {
  color: #e67e22 !important;
  font-weight: bold;
  font-size: 1.2em;
}

.in-stock {
  color: #27ae60 !important;
  font-weight: bold;
}

.out-of-stock-text {
  color: #e74c3c !important;
  font-weight: bold;
}

.specs {
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid #ddd;
}

.specs ul {
  margin: 5px 0;
  padding-left: 20px;
}

.specs li {
  color: #7f8c8d;
  font-size: 0.9em;
}

.config-details ul {
  margin: 10px 0;
  padding-left: 20px;
}

.config-details li {
  color: #7f8c8d;
  margin: 3px 0;
}

.search-controls {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.search-input, .filter-select {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  flex: 1;
}

.stats-section {
  background: white;
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.stat-card {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  border-top: 4px solid #3498db;
}

.stat-card h3 {
  margin: 0 0 10px 0;
  color: #2c3e50;
  font-size: 1em;
}

.stat-number {
  font-size: 2em;
  font-weight: bold;
  color: #3498db;
  margin: 0;
}

.error-section {
  background: #f8d7da;
  color: #721c24;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #f5c6cb;
}

.help-text {
  margin-top: 10px;
  font-size: 0.9em;
}

.help-text code {
  background: #f1f1f1;
  padding: 2px 6px;
  border-radius: 3px;
}

.notification {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 15px 20px;
  border-radius: 5px;
  color: white;
  font-weight: bold;
  z-index: 1000;
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.notification.success {
  background: #27ae60;
}

.notification.error {
  background: #e74c3c;
}

.notification.info {
  background: #3498db;
}
</style>