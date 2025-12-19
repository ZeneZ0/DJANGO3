<script>
export default {
  name: 'App',
  created() {
    this.$store.dispatch('checkAuth')
  },
  methods: {
    async logout() {
      const result = await this.$store.dispatch('logout')
      if (result.success) {
        this.$router.push('/login')
      }
    },
    openAdmin() {
      window.open('/admin/', '_blank')
    }
  }
}
</script>

<template>
  <div id="app">
    <header class="header">
      <div class="header-title">Конфигуратор ПК</div>
      <nav class="nav">
        <router-link to="/" class="nav-link">Главная</router-link>
        
        <template v-if="$store.getters.isAuthenticated">
          <router-link to="/backend-data" class="nav-link">Данные</router-link>
          
          <router-link v-if="$store.getters.isSuperUser" to="/manage/components" class="nav-link">
            Компоненты
          </router-link>
          
          <router-link v-if="$store.getters.isSuperUser" to="/manage/configurations" class="nav-link">
            Конфигурации
          </router-link>
          
          <router-link to="/manage/build-requests" class="nav-link">Запросы</router-link>
          
          <button v-if="$store.getters.isSuperUser" @click="openAdmin" class="nav-link admin-btn">
            Админка
          </button>
          
          <div class="user-info">
            {{ $store.getters.username }}
          </div>
          <button @click="logout" class="nav-link logout-btn">Выход</button>
        </template>
        
        <router-link v-else to="/login" class="nav-link login-btn">Войти</router-link>
      </nav>
    </header>
    
    <main class="content">
      <router-view/>
    </main>
  </div>
</template>

<style>
body {
  margin: 0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.header {
  background: #2c3e50;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: white;
}

.header-title {
  font-size: 1.5rem;
  font-weight: bold;
}

.nav {
  display: flex;
  gap: 10px;
  align-items: center;
}

.nav-link {
  color: white;
  text-decoration: none;
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 14px;
  border: none;
  background: transparent;
  cursor: pointer;
}

.nav-link:hover {
  background: #3498db;
}

.nav-link.router-link-active {
  background: #2980b9;
}

.admin-btn {
  background: #e74c3c;
}

.admin-btn:hover {
  background: #c0392b;
}

.login-btn {
  background: #27ae60;
}

.logout-btn {
  background: #7f8c8d;
}

.user-info {
  margin: 0 10px;
  font-weight: bold;
  color: #bdc3c7;
}

.content {
  padding: 20px;
  background: #ecf0f1;
  min-height: calc(100vh - 70px);
}
</style>