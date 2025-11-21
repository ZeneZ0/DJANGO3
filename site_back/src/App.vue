<!-- site_back/src/App.vue -->
<template>
  <div id="app">
    <nav class="navbar">
      <div class="nav-brand">🎮 Конфигуратор ПК</div>
      <div class="nav-links">
        <router-link to="/" class="nav-link">Главная</router-link>
        <router-link to="/about" class="nav-link">О проекте</router-link>
        <router-link to="/reactive" class="nav-link">Реактивные переменные</router-link>
        <router-link to="/arrays" class="nav-link">Работа с массивами</router-link>
        <router-link to="/backend-data" class="nav-link">Данные с бекенда</router-link>
        <router-link to="/manage-data" class="nav-link">Управление данными</router-link>
        <router-link to="/manage/component-types" class="nav-link">Типы компонентов</router-link>
        <router-link to="/manage/manufacturers" class="nav-link">Производители</router-link>
        <router-link to="/manage/components" class="nav-link">Компоненты</router-link>
        <router-link to="/manage/configurations" class="nav-link">Конфигурации</router-link>
        <router-link to="/manage/build-requests" class="nav-link">Запросы на сборку</router-link>
      </div>
    </nav>
    
    <main class="main-content">
      <router-view/>
    </main>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.navbar {
  background: #2b4a68ff;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-bottom: 1px solid #ffffffff;
}

.nav-brand {
  color: #ffffffff;
  font-size: 1.5rem;
  font-weight: bold;
}

.nav-links {
  display: flex;
  color: #ffffffff;
  gap: 1rem;
}

.nav-link {
  color: #ffffffff;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: all 0.3s;
  font-weight: 500;
}

.nav-link:hover,
.nav-link.router-link-active {
  background-color: #3381a0;
  color: white;
}

.main-content {
  padding: 2rem;
  min-height: calc(100vh - 80px);
  background: #f8f9fa;
}
</style>