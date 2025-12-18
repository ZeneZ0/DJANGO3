<!-- site_back/src/views/ArraysView.vue -->
<template>
  <div class="container mt-4">
    <h1 class="mb-4">Работа с массивами</h1>
    
    <div class="alert alert-info mb-3">
      Цены в долларах ($)
    </div>

    
    <div class="card mb-4">
      <div class="card-body">
        <h5 class="card-title">Добавить компонент</h5>
        <form @submit.prevent="addComponent" class="row g-3">
          <div class="col-md-5">
            <input v-model="newComponent.name" placeholder="Название" class="form-control" required>
          </div>
          <div class="col-md-3">
            <input v-model.number="newComponent.price" type="number" placeholder="Цена" class="form-control" required>
          </div>
          <div class="col-md-3">
            <select v-model="newComponent.type" class="form-select">
              <option value="">Тип</option>
              <option value="cpu">Процессор</option>
              <option value="gpu">Видеокарта</option>
              <option value="ram">Память</option>
              <option value="storage">Накопитель</option>
            </select>
          </div>
          <div class="col-md-1">
            <button type="submit" class="btn btn-primary w-100">+</button>
          </div>
        </form>
      </div>
    </div>

    
    <div class="row mb-3">
      <div class="col-md-6">
        <input v-model="searchQuery" placeholder="Поиск..." class="form-control">
      </div>
      <div class="col-md-4">
        <select v-model="filterType" class="form-select">
          <option value="">Все типы</option>
          <option value="cpu">Процессоры</option>
          <option value="gpu">Видеокарты</option>
          <option value="ram">Память</option>
          <option value="storage">Накопители</option>
        </select>
      </div>
      <div class="col-md-2">
        <button @click="sortByPrice" class="btn btn-outline-secondary w-100">
          {{ sortAscending ? '↑ Цена' : '↓ Цена' }}
        </button>
      </div>
    </div>

    
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">Список компонентов ({{ filteredComponents.length }})</h5>
        
        <div v-if="filteredComponents.length === 0" class="text-center text-muted py-4">
          Компоненты не найдены
        </div>
        
        <table v-else class="table">
          <tbody>
            <tr v-for="component in filteredComponents" 
                :key="component.id"
                :class="{ 'table-primary': selectedComponents.includes(component.id) }">
              <td>
                <strong>{{ component.name }}</strong><br>
                <small class="text-muted">{{ getTypeName(component.type) }}</small>
              </td>
              <td class="text-end">
                <strong>${{ component.price }}</strong>
              </td>
              <td class="text-end">
                <button @click="toggleSelection(component.id)" 
                        class="btn btn-sm me-1"
                        :class="selectedComponents.includes(component.id) ? 'btn-success' : 'btn-outline-success'">
                  {{ selectedComponents.includes(component.id) ? '✓' : '+' }}
                </button>
                <button @click="editComponent(component)" class="btn btn-warning btn-sm me-1">Изм</button>
                <button @click="removeComponent(component.id)" class="btn btn-danger btn-sm">Уд</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    
    <div v-if="selectedComponents.length > 0" class="card mt-4">
      <div class="card-body">
        <h5 class="card-title">Выбранные компоненты</h5>
        
        <ul class="list-group mb-3">
          <li v-for="id in selectedComponents" :key="id" class="list-group-item d-flex justify-content-between">
            <span>{{ getComponentById(id)?.name }} - ${{ getComponentById(id)?.price }}</span>
            <button @click="removeFromSelection(id)" class="btn btn-sm btn-outline-danger">×</button>
          </li>
        </ul>
        
        <div class="row">
          <div class="col-md-4">
            <p><strong>Итого:</strong> ${{ totalSelectedPrice }}</p>
          </div>
          <div class="col-md-4">
            <p><strong>Количество:</strong> {{ selectedComponents.length }} шт.</p>
          </div>
          <div class="col-md-4">
            <button @click="clearSelection" class="btn btn-outline-secondary w-100">Очистить</button>
          </div>
        </div>
      </div>
    </div>

    
    <div v-if="editingComponent" class="modal fade show d-block" style="background: rgba(0,0,0,0.5)">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Редактировать</h5>
            <button type="button" class="btn-close" @click="cancelEdit"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="updateComponent">
              <div class="mb-3">
                <input v-model="editingComponent.name" placeholder="Название" class="form-control" required>
              </div>
              <div class="mb-3">
                <input v-model.number="editingComponent.price" type="number" placeholder="Цена" class="form-control" required>
              </div>
              <div class="mb-3">
                <select v-model="editingComponent.type" class="form-select" required>
                  <option value="cpu">Процессор</option>
                  <option value="gpu">Видеокарта</option>
                  <option value="ram">Память</option>
                  <option value="storage">Накопитель</option>
                </select>
              </div>
              <div class="text-end">
                <button type="button" class="btn btn-secondary me-2" @click="cancelEdit">Отмена</button>
                <button type="submit" class="btn btn-primary">Сохранить</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

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
        filtered = filtered.filter(c => 
          c.name.toLowerCase().includes(this.searchQuery.toLowerCase())
        );
      }
      
      if (this.filterType) {
        filtered = filtered.filter(c => c.type === this.filterType);
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
    }
  },
  methods: {
    addComponent() {
      const component = {
        id: this.nextId++,
        ...this.newComponent
      };
      this.components.push(component);
      this.newComponent = { name: '', price: 0, type: '' };
    },
    
    removeComponent(id) {
      this.components = this.components.filter(c => c.id !== id);
      this.selectedComponents = this.selectedComponents.filter(selectedId => selectedId !== id);
    },
    
    editComponent(component) {
      this.editingComponent = { ...component };
    },
    
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
    
    getComponentById(id) {
      return this.components.find(c => c.id === id);
    },
    
    getTypeName(type) {
      const types = {
        cpu: 'Процессор',
        gpu: 'Видеокарта',
        ram: 'Память',
        storage: 'Накопитель'
      };
      return types[type] || 'Неизвестно';
    },
    
    sortByPrice() {
      this.sortAscending = !this.sortAscending;
    }
  }
}
</script>