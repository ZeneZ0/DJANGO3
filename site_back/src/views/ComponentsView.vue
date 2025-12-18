<!-- site_back/src/views/ComponentsView.vue -->
<template>
  <div class="container mt-4">
    <h1 class="mb-4">Управление компонентами</h1>

    <div class="alert alert-info mb-3">
      Цены в долларах ($)
    </div>

  
    <div class="card mb-4">
      <div class="card-header">
        <h5 class="mb-0">{{ isEditing ? 'Редактировать' : 'Добавить' }} компонент</h5>
      </div>
      <div class="card-body">
        <form @submit.prevent="saveComponent" enctype="multipart/form-data">
          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label">Название *</label>
              <input v-model="form.name" type="text" class="form-control" required>
            </div>
            
            <div class="col-md-3 mb-3">
              <label class="form-label">Тип *</label>
              <select v-model="form.component_type" class="form-select" required>
                <option value="">Выберите тип</option>
                <option v-for="type in componentTypes" :key="type.id" :value="type.id">
                  {{ type.name }}
                </option>
              </select>
            </div>
            
            <div class="col-md-3 mb-3">
              <label class="form-label">Производитель *</label>
              <select v-model="form.manufacturer" class="form-select" required>
                <option value="">Выберите производителя</option>
                <option v-for="man in manufacturers" :key="man.id" :value="man.id">
                  {{ man.name }}
                </option>
              </select>
            </div>
            
            <div class="col-md-4 mb-3">
              <label class="form-label">Цена ($) *</label>
              <input v-model.number="form.price" type="number" step="0.01" min="0" class="form-control" required>
            </div>
            
            <div class="col-md-8 mb-3">
              <label class="form-label">Описание</label>
              <textarea v-model="form.description" class="form-control" rows="2"></textarea>
            </div>
            
            <div class="col-md-6 mb-3">
              <div class="form-check">
                <input v-model="form.in_stock" class="form-check-input" type="checkbox">
                <label class="form-check-label">В наличии</label>
              </div>
            </div>
            
            
            <div class="col-12 mb-3">
              <label class="form-label">Изображение</label>
              <input 
                type="file" 
                class="form-control" 
                accept="image/*"
                @change="handleFileUpload"
                ref="fileInput"
              >
              
              
              <div v-if="imagePreview" class="mt-3">
                <p class="mb-2">Предпросмотр:</p>
                <img :src="imagePreview" class="img-thumbnail" style="max-height: 150px; cursor: pointer" 
                     @click="showImageModal(imagePreview)">
              </div>
              
              
              <div v-else-if="isEditing && currentImage" class="mt-3">
                <p class="mb-2">Текущее изображение:</p>
                <img :src="currentImage" class="img-thumbnail" style="max-height: 150px; cursor: pointer"
                     @click="showImageModal(currentImage)">
              </div>
            </div>
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

    
    <div class="card">
      <div class="card-header d-flex justify-content-between">
        <h5 class="mb-0">Список компонентов ({{ components.length }})</h5>
        <div>
          <button @click="loadData" class="btn btn-outline-primary btn-sm me-2">Обновить</button>
          <button @click="loadReferenceData" class="btn btn-outline-info btn-sm">Загрузить справочники</button>
        </div>
      </div>
      
      <div class="card-body">
        <div v-if="loading" class="text-center py-3">
          <div class="spinner-border text-primary"></div>
        </div>
        
        <div v-else-if="components.length === 0" class="text-center py-4 text-muted">
          Компонентов нет
        </div>
        
        <div v-else class="table-responsive">
          <table class="table table-striped">
            <thead>
              <tr>
                <th>Изображение</th>
                <th>Название</th>
                <th>Тип</th>
                <th>Производитель</th>
                <th>Цена</th>
                <th>Наличие</th>
                <th>Действия</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="comp in components" :key="comp.id" :class="{ 'table-warning': !comp.in_stock }">
                <td>
                  <img 
                    v-if="comp.image_url" 
                    :src="comp.image_url" 
                    class="img-thumbnail" 
                    style="width: 50px; height: 50px; object-fit: contain; cursor: pointer"
                    @click="showImageModal(comp.image_url)"
                  >
                  <span v-else class="text-muted">-</span>
                </td>
                <td><strong>{{ comp.name }}</strong></td>
                <td><span class="badge bg-primary">{{ comp.component_type_name }}</span></td>
                <td><span class="badge bg-info">{{ comp.manufacturer_name }}</span></td>
                <td class="text-success"><strong>${{ comp.price }}</strong></td>
                <td>
                  <span :class="['badge', comp.in_stock ? 'bg-success' : 'bg-danger']">
                    {{ comp.in_stock ? 'В наличии' : 'Нет в наличии' }}
                  </span>
                </td>
                <td>
                  <button @click="editComponent(comp)" class="btn btn-warning btn-sm me-1">Изменить</button>
                  <button @click="showDetails(comp)" class="btn btn-info btn-sm me-1">Детали</button>
                  <button @click="deleteComponent(comp.id)" class="btn btn-danger btn-sm">Удалить</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    
    <div v-if="selectedComponent" class="modal fade show d-block" style="background: rgba(0,0,0,0.5)">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Детали компонента</h5>
            <button type="button" class="btn-close" @click="selectedComponent = null"></button>
          </div>
          
          <div class="modal-body">
            <div class="row">
              <div class="col-md-6">
                <p><strong>Название:</strong> {{ selectedComponent.name }}</p>
                <p><strong>Тип:</strong> {{ selectedComponent.component_type_name }}</p>
                <p><strong>Производитель:</strong> {{ selectedComponent.manufacturer_name }}</p>
                <p><strong>Цена:</strong> ${{ selectedComponent.price }}</p>
                <p><strong>Наличие:</strong> 
                  <span :class="['badge', selectedComponent.in_stock ? 'bg-success' : 'bg-danger']">
                    {{ selectedComponent.in_stock ? 'В наличии' : 'Нет в наличии' }}
                  </span>
                </p>
              </div>
              <div class="col-md-6">
                <p><strong>Описание:</strong> {{ selectedComponent.description || '-' }}</p>
                <div v-if="selectedComponent.image_url" class="mb-3">
                  <p><strong>Изображение:</strong></p>
                  <img :src="selectedComponent.image_url" class="img-thumbnail" style="max-height: 200px; cursor: pointer"
                       @click="showImageModal(selectedComponent.image_url)">
                </div>
              </div>
            </div>
          </div>
          
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="selectedComponent = null">Закрыть</button>
          </div>
        </div>
      </div>
    </div>

    
    <div v-if="showImageModal" class="modal fade show d-block" style="background: rgba(0,0,0,0.5)">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Изображение</h5>
            <button type="button" class="btn-close" @click="showImageModal = false"></button>
          </div>
          <div class="modal-body text-center">
            <img :src="modalImage" class="img-fluid" style="max-height: 70vh">
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ComponentsView',
  data() {
    return {
      components: [],
      componentTypes: [],
      manufacturers: [],
      loading: false,
      isEditing: false,
      editId: null,
      selectedComponent: null,
      showImageModal: false,
      modalImage: '',
      imageFile: null,
      imagePreview: null,
      currentImage: '',
      form: {
        name: '',
        component_type: '',
        manufacturer: '',
        price: 0,
        description: '',
        in_stock: true
      }
    }
  },
  methods: {
    async loadData() {
      this.loading = true;
      try {
        const response = await axios.get('/api/components/');
        this.components = response.data;
      } catch (error) {
        console.error('Ошибка загрузки:', error);
        alert('Ошибка загрузки данных');
      }
      this.loading = false;
    },

    async loadReferenceData() {
      try {
        const [types, mans] = await Promise.all([
          axios.get('/api/component-types/'),
          axios.get('/api/manufacturers/')
        ]);
        this.componentTypes = types.data;
        this.manufacturers = mans.data;
      } catch (error) {
        console.error('Ошибка загрузки справочников:', error);
      }
    },

    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.imageFile = file;
        
        
        const reader = new FileReader();
        reader.onload = (e) => {
          this.imagePreview = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    },

    async saveComponent() {
      this.loading = true;
      try {
        const formData = new FormData();
        
        
        formData.append('name', this.form.name);
        formData.append('component_type', this.form.component_type);
        formData.append('manufacturer', this.form.manufacturer);
        formData.append('price', this.form.price);
        formData.append('description', this.form.description);
        formData.append('in_stock', this.form.in_stock);
        
        
        if (this.imageFile) {
          formData.append('image', this.imageFile);
        }

        if (this.isEditing) {
          await axios.put(`/api/components/${this.editId}/`, formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          });
        } else {
          await axios.post('/api/components/', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          });
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

    editComponent(comp) {
      this.isEditing = true;
      this.editId = comp.id;
      this.form = { 
        name: comp.name,
        component_type: comp.component_type,
        manufacturer: comp.manufacturer,
        price: comp.price,
        description: comp.description || '',
        in_stock: comp.in_stock
      };
      this.currentImage = comp.image_url;
      this.imagePreview = null;
      this.imageFile = null;
    },

    cancelEdit() {
      this.resetForm();
    },

    async deleteComponent(id) {
      if (!confirm('Удалить компонент?')) return;
      
      try {
        await axios.delete(`/api/components/${id}/`);
        this.components = this.components.filter(c => c.id !== id);
      } catch (error) {
        console.error('Ошибка удаления:', error);
        alert('Ошибка удаления');
      }
    },

    showDetails(comp) {
      this.selectedComponent = comp;
    },

    showImageModal(imageUrl) {
      this.modalImage = imageUrl;
      this.showImageModal = true;
    },

    resetForm() {
      this.isEditing = false;
      this.editId = null;
      this.form = {
        name: '',
        component_type: '',
        manufacturer: '',
        price: 0,
        description: '',
        in_stock: true
      };
      this.imageFile = null;
      this.imagePreview = null;
      this.currentImage = '';
      if (this.$refs.fileInput) {
        this.$refs.fileInput.value = '';
      }
    }
  },
  mounted() {
    this.loadData();
    this.loadReferenceData();
  }
}
</script>

<style scoped>
.img-thumbnail {
  object-fit: contain;
  background-color: #f8f9fa;
}

.table-warning {
  background-color: rgba(255, 193, 7, 0.1);
}
</style>