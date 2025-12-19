<script>
import axios from 'axios'

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
  name: 'BuildRequestsView',
  data() {
    return {
      requests: [],
      users: [],
      configurations: [],
      loading: false,
      isEditing: false,
      editId: null,
      selectedRequest: null,
      statusFilter: '',
      userFilter: '',
      stats: null,
      form: {
        user: '',
        configuration: '',
        budget: 0,
        status: 'pending',
        notes: ''
      },
      columnFilters: {
        id: '',
        user_name: '',
        configuration_name: '',
        budget_min: '',
        budget_max: '',
        status_filter: ''
      }
    }
  },
  computed: {
    filteredRequests() {
      let filtered = this.requests
      
      if (this.columnFilters.id) {
        filtered = filtered.filter(req => 
          req.id.toString().includes(this.columnFilters.id)
        )
      }
      
      if (this.columnFilters.user_name) {
        filtered = filtered.filter(req => 
          req.user_name.toLowerCase().includes(this.columnFilters.user_name.toLowerCase())
        )
      }
      
      if (this.columnFilters.configuration_name) {
        filtered = filtered.filter(req => {
          const configName = this.getConfigName(req.configuration).toLowerCase()
          return configName.includes(this.columnFilters.configuration_name.toLowerCase())
        })
      }
      
      if (this.columnFilters.budget_min) {
        filtered = filtered.filter(req => 
          req.budget >= parseFloat(this.columnFilters.budget_min)
        )
      }
      if (this.columnFilters.budget_max) {
        filtered = filtered.filter(req => 
          req.budget <= parseFloat(this.columnFilters.budget_max)
        )
      }
      
      if (this.columnFilters.status_filter) {
        filtered = filtered.filter(req => 
          req.status === this.columnFilters.status_filter
        )
      }
      
      return filtered
    }
  },
  methods: {
    async loadData() {
      this.loading = true
      try {
        const params = {}
        if (this.userFilter) {
          params.user_id = this.userFilter
        }
        const response = await axios.get('/api/build-requests/', { params })
        this.requests = response.data
      } catch (error) {
        console.error('Ошибка загрузки:', error)
        alert('Ошибка загрузки данных')
      }
      this.loading = false
    },

    async loadReferenceData() {
      try {
        const [configsResponse, statsResponse, authResponse] = await Promise.all([
          axios.get('/api/configurations/'),
          axios.get('/api/stats/'),
          axios.get('/api/auth/user/')
        ])
        
        this.configurations = configsResponse.data
        this.stats = statsResponse.data
        
        if (authResponse.data.is_superuser) {
          try {
            const usersResponse = await axios.get('/api/management/users/')
            this.users = usersResponse.data
          } catch (e) {
            console.error('Ошибка загрузки пользователей:', e)
          }
        }
      } catch (error) {
        console.error('Ошибка загрузки данных:', error)
      }
    },

    updateBudget() {
      const config = this.configurations.find(c => c.id === this.form.configuration)
      if (config && !this.isEditing) {
        this.form.budget = config.total_price
      }
    },

    async saveRequest() {
      this.loading = true
      try {
        if (this.isEditing) {
          await axios.put(`/api/build-requests/${this.editId}/`, this.form)
        } else {
          await axios.post('/api/build-requests/', this.form)
        }
        
        await this.loadData()
        this.resetForm()
        alert('Сохранено успешно')
      } catch (error) {
        console.error('Ошибка сохранения:', error)
        alert('Ошибка сохранения')
      }
      this.loading = false
    },

    editRequest(req) {
      this.isEditing = true
      this.editId = req.id
      this.form = { ...req }
    },

    cancelEdit() {
      this.resetForm()
    },

    async deleteRequest(id) {
      if (!confirm('Удалить запрос?')) return
      
      try {
        await axios.delete(`/api/build-requests/${id}/`)
        this.requests = this.requests.filter(r => r.id !== id)
      } catch (error) {
        console.error('Ошибка удаления:', error)
        alert('Ошибка удаления')
      }
    },

    showDetails(req) {
      this.selectedRequest = req
    },

    getConfigName(configId) {
      const config = this.configurations.find(c => c.id === configId)
      return config ? config.name : `Конфигурация #${configId}`
    },

    getStatusText(status) {
      const texts = {
        pending: 'Ожидает',
        in_progress: 'В работе',
        completed: 'Завершено',
        cancelled: 'Отменено'
      }
      return texts[status] || status
    },

    getStatusBadge(status) {
      const badges = {
        pending: 'bg-warning',
        in_progress: 'bg-info',
        completed: 'bg-success',
        cancelled: 'bg-danger'
      }
      return badges[status] || 'bg-secondary'
    },

    getStatusClass(status) {
      if (status === 'completed') return 'table-success'
      if (status === 'cancelled') return 'table-danger'
      if (status === 'in_progress') return 'table-info'
      return ''
    },

    formatDate(dateStr) {
      return new Date(dateStr).toLocaleDateString()
    },

    resetForm() {
      this.isEditing = false
      this.editId = null
      this.form = {
        user: '',
        configuration: '',
        budget: 0,
        status: 'pending',
        notes: ''
      }
    },

    async exportToExcel() {
  this.loading = true
  try {
    const params = {}
    if (this.columnFilters.id) params.id = this.columnFilters.id
    if (this.columnFilters.user_name) params.user_name = this.columnFilters.user_name
    if (this.columnFilters.configuration_name) params.configuration_name = this.columnFilters.configuration_name
    if (this.columnFilters.budget_min) params.budget_min = this.columnFilters.budget_min
    if (this.columnFilters.budget_max) params.budget_max = this.columnFilters.budget_max
    if (this.columnFilters.status_filter) params.status = this.columnFilters.status_filter
    if (this.userFilter) params.user_id = this.userFilter

    const response = await axios.get('/api/build-requests/export_excel/', {
      responseType: 'blob',
      params: params,
      headers: {
        'X-CSRFToken': getCookie('csrftoken')
      }
    })
    
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `requests_${new Date().toISOString().split('T')[0]}.xlsx`)
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

    resetFilters() {
      this.columnFilters = {
        id: '',
        user_name: '',
        configuration_name: '',
        budget_min: '',
        budget_max: '',
        status_filter: ''
      }
    }
  },
  mounted() {
    this.loadData()
    this.loadReferenceData()
  }
}
</script>
<template>
  <div class="container mt-4">
    <h1 class="mb-4">Управление запросами на сборку</h1>

    <div class="row mb-4" v-if="stats">
      <div class="col-md-3">
        <div class="card text-white bg-primary">
          <div class="card-body">
            <h6 class="card-title">Всего запросов</h6>
            <h3>{{ stats.requests_count }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card text-white bg-success">
          <div class="card-body">
            <h6 class="card-title">Средний чек</h6>
            <h3>${{ Math.round(stats.avg_request_budget) }}</h3>
          </div>
        </div>
      </div>
       <div class="col-md-6">
         <div class="alert alert-info h-100 d-flex align-items-center">
            Цены в долларах ($)
         </div>
      </div>
    </div>

    <div class="card mb-4">
      <div class="card-header">
        <h5 class="mb-0">{{ isEditing ? 'Редактировать' : 'Создать' }} запрос</h5>
      </div>
      <div class="card-body">
        <form @submit.prevent="saveRequest">
          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label">Пользователь</label>
              <select v-if="users.length > 0" v-model="form.user" class="form-select" required>
                <option value="">Выберите пользователя</option>
                <option v-for="user in users" :key="user.id" :value="user.id">
                  {{ user.username }}
                </option>
              </select>
              <input v-else type="text" class="form-control" 
                     :value="isEditing ? form.user_name : 'Текущий пользователь'" 
                     readonly disabled>
            </div>
            
            <div class="col-md-6 mb-3">
              <label class="form-label">Конфигурация *</label>
              <select v-model="form.configuration" class="form-select" required @change="updateBudget">
                <option value="">Выберите конфигурацию</option>
                <option v-for="config in configurations" :key="config.id" :value="config.id">
                  {{ config.name }} - ${{ config.total_price }}
                </option>
              </select>
            </div>
            
            <div class="col-md-4 mb-3">
              <label class="form-label">Бюджет ($) *</label>
              <input v-model.number="form.budget" type="number" step="0.01" min="0" class="form-control" required>
            </div>
            
            <div class="col-md-4 mb-3">
              <label class="form-label">Статус *</label>
              <select v-model="form.status" class="form-select" required>
                <option value="pending">Ожидает</option>
                <option value="in_progress">В работе</option>
                <option value="completed">Завершено</option>
                <option value="cancelled">Отменено</option>
              </select>
            </div>
            
            <div class="col-12 mb-3">
              <label class="form-label">Пожелания</label>
              <textarea v-model="form.notes" class="form-control" rows="3"></textarea>
            </div>
          </div>
          
          <div>
            <button type="submit" class="btn btn-success" :disabled="loading">
              {{ isEditing ? 'Сохранить' : 'Создать' }}
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
          <div class="col-md-2">
            <input v-model="columnFilters.id" 
                   placeholder="ID" 
                   class="form-control form-control-sm">
          </div>
          <div class="col-md-3">
            <input v-model="columnFilters.user_name" 
                   placeholder="Пользователь" 
                   class="form-control form-control-sm">
          </div>
          <div class="col-md-3">
            <input v-model="columnFilters.configuration_name" 
                   placeholder="Конфигурация" 
                   class="form-control form-control-sm">
          </div>
          <div class="col-md-4">
            <div class="input-group input-group-sm">
              <input v-model="columnFilters.budget_min" 
                     type="number" 
                     placeholder="Бюджет от" 
                     class="form-control">
              <input v-model="columnFilters.budget_max" 
                     type="number" 
                     placeholder="Бюджет до" 
                     class="form-control">
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-md-3">
            <select v-model="columnFilters.status_filter" class="form-select form-select-sm">
              <option value="">Все статусы</option>
              <option value="pending">Ожидает</option>
              <option value="in_progress">В работе</option>
              <option value="completed">Завершено</option>
              <option value="cancelled">Отменено</option>
            </select>
          </div>
          <div class="col-md-9 d-flex justify-content-end">
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
        <h5 class="mb-0">Список запросов ({{ filteredRequests.length }})</h5>
        <div>
          <button @click="loadData" class="btn btn-outline-primary btn-sm me-2">Обновить</button>
          <button @click="loadReferenceData" class="btn btn-outline-info btn-sm">Загрузить данные</button>
        </div>
      </div>
      
      <div class="card-body">
        <div v-if="loading" class="text-center py-3">
          <div class="spinner-border text-primary"></div>
        </div>
        
        <div v-else-if="filteredRequests.length === 0" class="text-center py-4 text-muted">
          Запросов нет
        </div>
        
        <div v-else class="table-responsive">
          <table class="table table-striped">
            <thead>
              <tr>
                <th>ID</th>
                <th>Пользователь</th>
                <th>Конфигурация</th>
                <th>Бюджет</th>
                <th>Статус</th>
                <th>Дата</th>
                <th>Действия</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="req in filteredRequests" :key="req.id" :class="getStatusClass(req.status)">
                <td>{{ req.id }}</td>
                <td><strong>{{ req.user_name }}</strong></td>
                <td>{{ getConfigName(req.configuration) }}</td>
                <td class="text-success"><strong>${{ req.budget }}</strong></td>
                <td>
                  <span :class="['badge', getStatusBadge(req.status)]">
                    {{ getStatusText(req.status) }}
                  </span>
                </td>
                <td>{{ formatDate(req.created_at) }}</td>
                <td>
                  <button @click="editRequest(req)" class="btn btn-warning btn-sm me-1">Изменить</button>
                  <button @click="showDetails(req)" class="btn btn-info btn-sm me-1">Детали</button>
                  <button @click="deleteRequest(req.id)" class="btn btn-danger btn-sm">Удалить</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div v-if="selectedRequest" class="modal fade show d-block" style="background: rgba(0,0,0,0.5)">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Детали запроса</h5>
            <button type="button" class="btn-close" @click="selectedRequest = null"></button>
          </div>
          
          <div class="modal-body">
            <div class="row">
              <div class="col-md-6">
                <p><strong>ID:</strong> {{ selectedRequest.id }}</p>
                <p><strong>Пользователь:</strong> {{ selectedRequest.user_name }}</p>
                <p><strong>Конфигурация:</strong> {{ getConfigName(selectedRequest.configuration) }}</p>
                <p><strong>Бюджет:</strong> ${{ selectedRequest.budget }}</p>
              </div>
              <div class="col-md-6">
                <p><strong>Статус:</strong> 
                  <span :class="['badge', getStatusBadge(selectedRequest.status)]">
                    {{ getStatusText(selectedRequest.status) }}
                  </span>
                </p>
                <p><strong>Дата создания:</strong> {{ formatDate(selectedRequest.created_at) }}</p>
                <p v-if="selectedRequest.notes"><strong>Пожелания:</strong> {{ selectedRequest.notes }}</p>
              </div>
            </div>
          </div>
          
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="selectedRequest = null">Закрыть</button>
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

.card {
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.modal {
  background: rgba(0,0,0,0.5);
}

.badge {
  font-size: 0.75em;
  padding: 0.25em 0.6em;
}
</style>