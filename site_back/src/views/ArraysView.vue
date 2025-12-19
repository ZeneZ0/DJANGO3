
<script>
export default {
  name: 'ArraysView',
  data() {
    return {
      
      components: [
        { id: 1, name: 'Intel Core i5', price: 180, type: 'cpu' },
        { id: 2, name: 'AMD Ryzen 7', price: 250, type: 'cpu' },
        { id: 3, name: 'NVIDIA RTX 4060', price: 350, type: 'gpu' },
        { id: 4, name: 'AMD RX 7600', price: 300, type: 'gpu' },
        { id: 5, name: 'Kingston 16GB', price: 40, type: 'ram' },
        { id: 6, name: 'Samsung 1TB SSD', price: 60, type: 'storage' }
      ],
      
      newComponent: {
        name: '',
        price: 0,
        type: ''
      },
      
      selectedComponents: [],
      
      searchQuery: '',
      filterType: '',
      sortAscending: true,
      
      editingComponent: null,
      
      nextId: 7
    }
  },
  computed: {
   
    filteredComponents() {
      let filtered = this.components;
      
      
      if (this.searchQuery) {
        filtered = filtered.filter(component => 
          component.name.toLowerCase().includes(this.searchQuery.toLowerCase())
        );
      }
      
     
      if (this.filterType) {
        filtered = filtered.filter(component => component.type === this.filterType);
      }
      
      
      filtered = [...filtered].sort((a, b) => {
        return this.sortAscending ? a.price - b.price : b.price - a.price;
      });
      
      return filtered;
    },
    
   
    totalSelectedPrice() {
      return this.selectedComponents.reduce((total, id) => {
        const component = this.getComponentById(id);
        return total + (component?.price || 0);
      }, 0);
    },
    
    
    averagePrice() {
      if (this.selectedComponents.length === 0) return 0;
      return Math.round(this.totalSelectedPrice / this.selectedComponents.length);
    }
  },
  methods: {
    // Форматирование цены в доллары
    formatPrice(price) {
      if (!price) return '$0';
      return `$${price}`;
    },

    // Добавление компонента в массив
    addComponent() {
      const component = {
        id: this.nextId++,
        ...this.newComponent
      };
      this.components.push(component);
      this.newComponent = { name: '', price: 0, type: '' };
    },
    
    // Удаление компонента из массива
    removeComponent(id) {
      this.components = this.components.filter(component => component.id !== id);
      this.selectedComponents = this.selectedComponents.filter(selectedId => selectedId !== id);
    },
    
    // Редактирование компонента
    editComponent(component) {
      this.editingComponent = { ...component };
    },
    
    // Обновление компонента
    updateComponent() {
      const index = this.components.findIndex(c => c.id === this.editingComponent.id);
      if (index !== -1) {
        this.components.splice(index, 1, this.editingComponent);
      }
      this.cancelEdit();
    },
    
    cancelEdit() {
      this.editingComponent = null;
    },
    
    // Работа с выбранными компонентами
    toggleSelection(id) {
      const index = this.selectedComponents.indexOf(id);
      if (index === -1) {
        this.selectedComponents.push(id);
      } else {
        this.selectedComponents.splice(index, 1);
      }
    },
    
    removeFromSelection(id) {
      this.selectedComponents = this.selectedComponents.filter(selectedId => selectedId !== id);
    },
    
    clearSelection() {
      this.selectedComponents = [];
    },
    
    // Вспомогательные методы
    getComponentById(id) {
      return this.components.find(component => component.id === id);
    },
    
    getTypeName(type) {
      const types = {
        cpu: 'Процессор',
        gpu: 'Видеокарта',
        ram: 'Оперативная память',
        storage: 'Накопитель'
      };
      return types[type] || 'Неизвестный тип';
    },
    
    sortByPrice() {
      this.sortAscending = !this.sortAscending;
    }
  }
}
</script>

<template>
  <div class="arrays-view">
    <h1>📋 Работа с массивами</h1>
    
    <div class="currency-note">
      💰 Все цены в долларах США ($)
    </div>
    
    <div class="demo-section">
      <h2>🛒 Компоненты для ПК</h2>
      
      <!-- Форма добавления компонента -->
      <div class="add-form">
        <h3>➕ Добавить компонент</h3>
        <form @submit.prevent="addComponent" class="form">
          <input v-model="newComponent.name" placeholder="Название" required>
          <input v-model.number="newComponent.price" type="number" placeholder="Цена ($)" required>
          <select v-model="newComponent.type">
            <option value="">Выберите тип</option>
            <option value="cpu">Процессор</option>
            <option value="gpu">Видеокарта</option>
            <option value="ram">Оперативная память</option>
            <option value="storage">Накопитель</option>
          </select>
          <button type="submit">Добавить</button>
        </form>
      </div>

      <!-- Фильтрация и поиск -->
      <div class="filters">
        <h3>🔍 Фильтры</h3>
        <div class="filter-controls">
          <input v-model="searchQuery" placeholder="Поиск по названию..." class="search-input">
          <select v-model="filterType" class="type-filter">
            <option value="">Все типы</option>
            <option value="cpu">Процессоры</option>
            <option value="gpu">Видеокарты</option>
            <option value="ram">Память</option>
            <option value="storage">Накопители</option>
          </select>
          <button @click="sortByPrice" class="sort-btn">
            {{ sortAscending ? '↑ По цене' : '↓ По цене' }}
          </button>
        </div>
      </div>

      <!-- Список компонентов -->
      <div class="components-list">
        <h3>📦 Список компонентов ({{ filteredComponents.length }})</h3>
        
        <div v-if="filteredComponents.length === 0" class="empty-state">
          😔 Компоненты не найдены
        </div>
        
        <div v-else>
          <div v-for="component in filteredComponents" 
               :key="component.id" 
               class="component-item"
               :class="{
                 'selected': selectedComponents.includes(component.id),
                 'expensive': component.price > 500
               }">
            
            <div class="component-info">
              <h4>{{ component.name }}</h4>
              <p class="component-type">{{ getTypeName(component.type) }}</p>
              <p class="component-price">{{ formatPrice(component.price) }}</p>
            </div>
            
            <div class="component-actions">
              <button @click="toggleSelection(component.id)" 
                      :class="{
                        'select-btn': true,
                        'selected': selectedComponents.includes(component.id)
                      }">
                {{ selectedComponents.includes(component.id) ? '✓ Выбрано' : 'Выбрать' }}
              </button>
              <button @click="editComponent(component)" class="edit-btn">✏️</button>
              <button @click="removeComponent(component.id)" class="delete-btn">🗑️</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Выбранные компоненты -->
      <div v-if="selectedComponents.length > 0" class="selected-section">
        <h3>🛍️ Выбранные компоненты</h3>
        <div class="selected-list">
          <div v-for="id in selectedComponents" 
               :key="id" 
               class="selected-item">
            {{ getComponentById(id)?.name }} - {{ formatPrice(getComponentById(id)?.price) }}
            <button @click="removeFromSelection(id)" class="remove-btn">✕</button>
          </div>
        </div>
        
        <div class="selection-stats">
          <p><strong>Итого:</strong> {{ formatPrice(totalSelectedPrice) }}</p>
          <p><strong>Количество:</strong> {{ selectedComponents.length }} шт.</p>
          <p><strong>Средняя цена:</strong> {{ formatPrice(averagePrice) }}</p>
        </div>
        
        <button @click="clearSelection" class="clear-btn">Очистить выбор</button>
      </div>

      <!-- Модальное окно редактирования -->
      <div v-if="editingComponent" class="modal-overlay">
        <div class="modal">
          <h3>✏️ Редактировать компонент</h3>
          <form @submit.prevent="updateComponent" class="form">
            <input v-model="editingComponent.name" placeholder="Название" required>
            <input v-model.number="editingComponent.price" type="number" placeholder="Цена ($)" required>
            <select v-model="editingComponent.type" required>
              <option value="cpu">Процессор</option>
              <option value="gpu">Видеокарта</option>
              <option value="ram">Оперативная память</option>
              <option value="storage">Накопитель</option>
            </select>
            <div class="modal-actions">
              <button type="submit">Сохранить</button>
              <button type="button" @click="cancelEdit">Отмена</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>


<style scoped>
.arrays-view {
  max-width: 800px;
  margin: 0 auto;
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

.demo-section {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.add-form {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.form {
  display: flex;
  gap: 10px;
  align-items: end;
}

.form input, .form select {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  flex: 1;
}

.filters {
  margin-bottom: 20px;
}

.filter-controls {
  display: flex;
  gap: 10px;
  align-items: center;
}

.search-input, .type-filter, .sort-btn {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.search-input {
  flex: 2;
}

.type-filter {
  flex: 1;
}

.sort-btn {
  background: #3498db;
  color: white;
  border: none;
  cursor: pointer;
}

.components-list {
  margin-bottom: 20px;
}

.component-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  margin-bottom: 10px;
  transition: all 0.3s ease;
}

.component-item:hover {
  border-color: #3498db;
}

.component-item.selected {
  background: #e8f4fd;
  border-color: #3498db;
}

.component-item.expensive {
  border-left: 4px solid #e74c3c;
}

.component-info h4 {
  margin: 0 0 5px 0;
  color: #2c3e50;
}

.component-type {
  color: #7f8c8d;
  font-size: 0.9em;
  margin: 0;
}

.component-price {
  color: #27ae60;
  font-weight: bold;
  margin: 0;
}

.component-actions {
  display: flex;
  gap: 5px;
}

.select-btn, .edit-btn, .delete-btn {
  padding: 5px 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9em;
}

.select-btn {
  background: #ecf0f1;
  color: #2c3e50;
}

.select-btn.selected {
  background: #27ae60;
  color: white;
}

.edit-btn {
  background: #3498db;
  color: white;
}

.delete-btn {
  background: #e74c3c;
  color: white;
}

.selected-section {
  background: #e8f4fd;
  padding: 20px;
  border-radius: 8px;
  border-left: 4px solid #3498db;
}

.selected-list {
  margin: 15px 0;
}

.selected-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: white;
  border-radius: 4px;
  margin-bottom: 5px;
}

.remove-btn {
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  cursor: pointer;
}

.selection-stats {
  background: white;
  padding: 15px;
  border-radius: 4px;
  margin: 15px 0;
}

.clear-btn {
  background: #95a5a6;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal {
  background: white;
  padding: 30px;
  border-radius: 8px;
  min-width: 400px;
}

.modal-actions {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #7f8c8d;
  font-size: 1.1em;
}
</style>