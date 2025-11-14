<!-- site_back/src/views/HomeView.vue -->
<template>
  <div class="home">
    <div class="welcome">
      <h1>Добро пожаловать в Конфигуратор ПК! 🎮</h1>
      <p>Собирайте компьютеры мечты с нашим конструктором</p>
      
      <div class="features">
        <div class="feature-card">
          <h3>⚡ Реактивные переменные</h3>
          <p>Изучите работу с реактивными данными в Vue</p>
          <router-link to="/reactive" class="feature-link">Перейти →</router-link>
        </div>
        
        <div class="feature-card">
          <h3>📋 Работа с массивами</h3>
          <p>Управляйте списками компонентов ПК</p>
          <router-link to="/arrays" class="feature-link">Перейти →</router-link>
        </div>
        
        <div class="feature-card">
          <h3>🛠️ Конфигуратор</h3>
          <p>Собирайте компьютеры из компонентов</p>
          <p class="coming-soon">Скоро...</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomeView'
}
</script>

<style scoped>
.home {
  padding: 2rem;
}

.welcome {
  text-align: center;
  margin-bottom: 3rem;
}

.welcome h1 {
  color: #2c3e50;
  margin-bottom: 1rem;
  font-size: 2.5rem;
}

.welcome p {
  color: #7f8c8d;
  font-size: 1.2rem;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 3rem;
}

.feature-card {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-card h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.feature-card p {
  color: #7f8c8d;
  margin-bottom: 1.5rem;
}

.feature-link {
  display: inline-block;
  background: #3498db;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  text-decoration: none;
  transition: background 0.3s ease;
}

.feature-link:hover {
  background: #2980b9;
}

.coming-soon {
  color: #e74c3c !important;
  font-style: italic;
}
</style>