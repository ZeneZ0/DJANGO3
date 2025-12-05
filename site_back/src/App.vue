<!-- site_back/src/App.vue -->
<template>
  <div id="app">
    <header class="header">
      <div class="header-title">Конфигуратор ПК</div>
      <nav class="nav">
        <router-link to="/" class="nav-link">Главная</router-link>
        <router-link to="/about" class="nav-link">О проекте</router-link>
        <router-link to="/reactive" class="nav-link">Реактивность</router-link>
        <router-link to="/arrays" class="nav-link">Массивы</router-link>
        <router-link to="/data" class="nav-link">Данные</router-link>
        <router-link to="/components" class="nav-link">Компоненты</router-link>
        <router-link to="/configs" class="nav-link">Конфигурации</router-link>
        <router-link to="/requests" class="nav-link">Запросы</router-link>
        <button @click="openAdmin" class="nav-link admin-btn">Админка</button>
      </nav>
    </header>
    
    <main class="content">
      <router-view/>
    </main>
  </div>
</template>

<script>
export default {
  name: 'App',
  methods: {
    openAdmin() {
      window.open('/admin/', '_blank');
    }
  }
}
</script>

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
}

.nav-link {
  color: white;
  text-decoration: none;
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 14px;
}

.nav-link:hover {
  background: #3498db;
}

.nav-link.router-link-active {
  background: #2980b9;
}

.admin-btn {
  background: #e74c3c;
  border: none;
  cursor: pointer;
}

.admin-btn:hover {
  background: #c0392b;
}

.content {
  padding: 20px;
  background: #ecf0f1;
  min-height: calc(100vh - 70px);
}
</style>