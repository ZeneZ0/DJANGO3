<!-- site_back/src/views/UserSelectView.vue -->
<template>
  <div class="login-page">
    <div class="login-box">
      <h2>Выберите пользователя</h2>
      
      <div class="user-list">
        <div 
          v-for="user in users" 
          :key="user.id"
          class="user-item"
          @click="login(user)"
        >
          <div class="user-info">
            <div class="user-name">{{ user.name }}</div>
            <div class="user-role">{{ user.role }}</div>
          </div>
          <div class="user-desc">{{ user.desc }}</div>
        </div>
      </div>

      <div class="password-info">
        <p><strong>Пароли:</strong></p>
        <p>ZeneZ: admin123</p>
        <p>vlad: vlad123</p>
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
          name: 'ZeneZ',
          password: 'admin123',
          role: 'Администратор',
          desc: 'Полный доступ'
        },
        {
          id: 2,
          name: 'vlad',
          password: 'vlad123',
          role: 'Покупатель',
          desc: 'Просмотр и заявки'
        }
      ]
    }
  },
  methods: {
    async login(user) {
      try {
        // Сохраняем пользователя
        localStorage.setItem('user', JSON.stringify(user));
        
        // Создаем заголовок авторизации
        const auth = btoa(`${user.name}:${user.password}`);
        localStorage.setItem('auth', auth);

        // Проверяем доступ
        await axios.get('/api/components/', {
          headers: {
            'Authorization': `Basic ${auth}`
          }
        });

        // Переходим на главную
        this.$router.push('/');
        
      } catch (error) {
        alert('Ошибка входа');
      }
    }
  },
  mounted() {
    // Если уже вошли, переходим на главную
    const user = localStorage.getItem('user');
    if (user) {
      this.$router.push('/');
    }
  }
}
</script>

<style>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #f5f5f5;
  padding: 20px;
}

.login-box {
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  max-width: 400px;
  width: 100%;
}

.login-box h2 {
  text-align: center;
  margin-bottom: 20px;
  color: #333;
}

.user-list {
  margin-bottom: 20px;
}

.user-item {
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 6px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: background 0.3s;
}

.user-item:hover {
  background: #f0f0f0;
}

.user-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
}

.user-name {
  font-weight: bold;
  color: #2c3e50;
}

.user-role {
  font-size: 14px;
  color: #666;
}

.user-desc {
  font-size: 13px;
  color: #777;
}

.password-info {
  background: #e8f4fc;
  padding: 15px;
  border-radius: 6px;
  font-size: 14px;
}

.password-info p {
  margin: 5px 0;
}
</style>