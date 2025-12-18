<!-- site_back/src/views/ManufacturersView.vue -->
<template>
  <div class="container mt-4">
    <h1 class="mb-4">Управление производителями</h1>

    
    <div class="card mb-4">
      <div class="card-header">
        <h5 class="mb-0">{{ isEditing ? 'Редактировать' : 'Добавить' }} производителя</h5>
      </div>
      <div class="card-body">
        <form @submit.prevent="saveManufacturer" enctype="multipart/form-data">
          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label">Название *</label>
              <input v-model="form.name" type="text" class="form-control" required>
            </div>
            
            <div class="col-md-6 mb-3">
              <label class="form-label">Страна *</label>
              <input v-model="form.country" type="text" class="form-control" required>
            </div>
            
            <div class="col-12 mb-3">
              <label class="form-label">Веб-сайт</label>
              <input v-model="form.website" type="url" class="form-control" placeholder="https://example.com">
            </div>
            
            
            <div class="col-12 mb-3">
              <label class="form-label">Логотип</label>
              <input 
                type="file" 
                class="form-control" 
                accept="image/*"
                @change="handleFileUpload"
                ref="fileInput"
              >
              <div class="form-text">JPG, PNG, GIF</div>
              
              
              <div v-if="imagePreview" class="mt-3">
                <p class="mb-2">Предпросмотр:</p>
                <img :src="imagePreview" class="img-thumbnail" style="max-height: 150px; cursor: pointer" 
                     @click="showImageModal(imagePreview)">
              </div>
              
              
              <div v-else-if="isEditing && currentLogo" class="mt-3">
                <p class="mb-2">Текущий логотип:</p>
                <img :src="currentLogo" class="img-thumbnail" style="max-height: 150px; cursor: pointer"
                     @click="showImageModal(currentLogo)">
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
        <h5 class="mb-0">Список производителей ({{ manufacturers.length }})</h5>
        <button @click="loadData" class="btn btn-outline-primary btn-sm">Обновить</button>
      </div>
      
      <div class="card-body">
        <div v-if="loading" class="text-center py-3">
          <div class="spinner-border text-primary"></div>
        </div>
        
        <div v-else-if="manufacturers.length === 0" class="text-center py-4 text-muted">
          Производителей нет
        </div>
        
        <div v-else class="table-responsive">
          <table class="table table-striped">
            <thead>
              <tr>
                <th>Логотип</th>
                <th>Название</th>
                <th>Страна</th>
                <th>Веб-сайт</th>
                <th>Действия</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="man in manufacturers" :key="man.id">
                <td>
                  <img 
                    v-if="man.logo_url" 
                    :src="man.logo_url" 
                    class="img-thumbnail" 
                    style="width: 50px; height: 50px; object-fit: contain; cursor: pointer"
                    @click="showImageModal(man.logo_url)"
                  >
                  <span v-else class="text-muted">-</span>
                </td>
                <td><strong>{{ man.name }}</strong></td>
                <td><span class="badge bg-info">{{ man.country }}</span></td>
                <td>
                  <a v-if="man.website" :href="man.website" target="_blank" class="text-decoration-none">
                    Сайт
                  </a>
                  <span v-else class="text-muted">-</span>
                </td>
                <td>
                  <button @click="editManufacturer(man)" class="btn btn-warning btn-sm me-1">Изменить</button>
                  <button @click="deleteManufacturer(man.id)" class="btn btn-danger btn-sm">Удалить</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    
    <div v-if="showModal" class="modal fade show d-block" style="background: rgba(0,0,0,0.8)">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Просмотр изображения</h5>
            <button type="button" class="btn-close" @click="showModal = false"></button>
          </div>
          <div class="modal-body text-center">
            <img :src="modalImageUrl" class="img-fluid" style="max-height: 70vh">
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ManufacturersView',
  data() {
    return {
      manufacturers: [],
      loading: false,
      isEditing: false,
      editId: null,
      showModal: false,
      modalImageUrl: '',
      imageFile: null,
      imagePreview: null,
      currentLogo: '',
      form: {
        name: '',
        country: '',
        website: ''
      }
    }
  },
  methods: {
    async loadData() {
      this.loading = true;
      try {
        const response = await axios.get('/api/manufacturers/');
        this.manufacturers = response.data;
      } catch (error) {
        console.error('Ошибка загрузки:', error);
        alert('Ошибка загрузки данных');
      }
      this.loading = false;
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

    async saveManufacturer() {
      this.loading = true;
      try {
        const formData = new FormData();
        
        
        formData.append('name', this.form.name);
        formData.append('country', this.form.country);
        if (this.form.website) {
          formData.append('website', this.form.website);
        }
        
        
        if (this.imageFile) {
          formData.append('logo', this.imageFile);
        }

        if (this.isEditing) {
          await axios.put(`/api/manufacturers/${this.editId}/`, formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          });
        } else {
          await axios.post('/api/manufacturers/', formData, {
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

    editManufacturer(man) {
      this.isEditing = true;
      this.editId = man.id;
      this.form = { 
        name: man.name,
        country: man.country,
        website: man.website || ''
      };
      this.currentLogo = man.logo_url;
      this.imagePreview = null;
      this.imageFile = null;
    },

    cancelEdit() {
      this.resetForm();
    },

    async deleteManufacturer(id) {
      if (!confirm('Удалить производителя?')) return;
      
      try {
        await axios.delete(`/api/manufacturers/${id}/`);
        this.manufacturers = this.manufacturers.filter(m => m.id !== id);
      } catch (error) {
        console.error('Ошибка удаления:', error);
        alert('Ошибка удаления');
      }
    },

    showImageModal(imageUrl) {
      this.modalImageUrl = imageUrl;
      this.showModal = true;
    },

    resetForm() {
      this.isEditing = false;
      this.editId = null;
      this.form = {
        name: '',
        country: '',
        website: ''
      };
      this.imageFile = null;
      this.imagePreview = null;
      this.currentLogo = '';
      if (this.$refs.fileInput) {
        this.$refs.fileInput.value = '';
      }
    }
  },
  mounted() {
    this.loadData();
  }
}
</script>

<style scoped>
.img-thumbnail {
  object-fit: contain;
  background-color: #f8f9fa;
}
</style>