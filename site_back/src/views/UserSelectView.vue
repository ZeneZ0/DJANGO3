<!-- site_back/src/views/UserSelectView.vue -->
<template>
  <div class="user-select-view">
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card">
            <div class="card-header text-center">
              <h4 class="card-title mb-0">👥 Выбор пользователя</h4>
            </div>
            <div class="card-body">
              <div class="list-group">
                <button 
                  v-for="user in users" 
                  :key="user.id"
                  class="list-group-item list-group-item-action user-item"
                  @click="selectUser(user)"
                >
                  <div class="d-flex justify-content-between align-items-center">
                    <div>
                      <h6 class="mb-1">{{ user.username }}</h6>
                      <p class="mb-1 text-muted">{{ user.description }}</p>
                    </div>
                    <span :class="user.badgeClass">{{ user.role }}</span>
                  </div>
                </button>
              </div>

              <div class="mt-4">
                <div class="alert alert-info">
                  <h6>🔑 Пароли для входа:</h6>
                  <p class="mb-1"><strong>ZeneZ:</strong> admin123</p>
                  <p class="mb-0"><strong>vlad:</strong> vlad123</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'UserSelectView',
  data() {
    return {
      users: [
        {
          id: 1,
          username: 'ZeneZ',
          password: 'admin123',
          role: 'Администратор',
          description: 'Полный доступ ко всем функциям системы',
          badgeClass: 'badge bg-warning'
        },
        {
          id: 2,
          username: 'vlad',
          password: 'vlad123',
          role: 'Покупатель',
          description: 'Просмотр каталогов и создание заявок',
          badgeClass: 'badge bg-info'
        }
      ]
    }
  },
  methods: {
    async selectUser(user) {
      try {
        // Сохраняем выбранного пользователя
        localStorage.setItem('currentUser', JSON.stringify(user));
        
        // Создаем Basic Auth заголовок
        const credentials = btoa(`${user.username}:${user.password}`);
        localStorage.setItem('authCredentials', credentials);

        // Проверяем аутентификацию
        const response = await axios.get('/api/components/', {
          headers: {
            'Authorization': `Basic ${credentials}`
          }
        });

        // Перенаправляем на главную
        this.$router.push('/');
        
      } catch (error) {
        console.error('Ошибка входа:', error);
        alert('Ошибка входа. Проверьте подключение к серверу.');
      }
    }
  },
  mounted() {
    // Если уже выбран пользователь, перенаправляем
    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      this.$router.push('/');
    }
  }
}
</script>

<style scoped>
.user-select-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding-top: 100px;
}

.card {
  border: none;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.user-item {
  border: 1px solid #dee2e6;
  margin-bottom: 10px;
  border-radius: 10px;
  transition: all 0.3s;
}

.user-item:hover {
  background-color: #f8f9fa;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
</style>