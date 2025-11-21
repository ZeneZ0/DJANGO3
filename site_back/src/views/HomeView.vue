<!-- site_back/src/views/HomeView.vue -->
<template>
  <div class="home">
    <div class="welcome">
      <h1>Добро пожаловать в Конфигуратор ПК! 🎮</h1>
      <p>Собирайте компьютеры мечты с нашим конструктором</p>
      
      <div class="price-examples">
        <p>💵 Примеры сборок: от <strong>$500</strong> до <strong>$3000</strong></p>
      </div>
      
      <div class="features">
        <div class="feature-card">
          <h3>⚡ Реактивные переменные</h3>
          <p>Изучите работу с реактивными данными в Vue</p>
          <p class="feature-price">Примеры цен: $150 - $1500</p>
          <router-link to="/reactive" class="feature-link">Перейти →</router-link>
        </div>
        
        <div class="feature-card">
          <h3>📋 Работа с массивами</h3>
          <p>Управляйте списками компонентов ПК</p>
          <p class="feature-price">Компоненты: $40 - $500</p>
          <router-link to="/arrays" class="feature-link">Перейти →</router-link>
        </div>
        
        <div class="feature-card">
          <h3>📡 Данные с бекенда</h3>
          <p>Работа с реальными данными из Django API</p>
          <p class="feature-price">Реальные цены из базы</p>
          <router-link to="/backend-data" class="feature-link">Перейти →</router-link>
        </div>
        
        <div class="feature-card">
          <h3>🛠️ Конфигуратор</h3>
          <p>Собирайте компьютеры из компонентов</p>
          <p class="feature-price">Сборки от $800</p>
          <p class="coming-soon">Скоро...</p>
        </div>
      </div>
    </div>

    <div class="quick-stats">
      <h2>🚀 Быстрый старт</h2>
      <div class="stats-grid">
        <div class="stat-item">
          <h4>Бюджетная сборка</h4>
          <p class="stat-price">$500 - $800</p>
          <p>Идеально для офисных задач</p>
        </div>
        <div class="stat-item">
          <h4>Игровая сборка</h4>
          <p class="stat-price">$1000 - $2000</p>
          <p>Для комфортного гейминга</p>
        </div>
        <div class="stat-item">
          <h4>Профессиональная</h4>
          <p class="stat-price">$2000+</p>
          <p>Для работы с графикой и видео</p>
        </div>
      </div>
    </div>

    <div class="cta-section">
      <h2>🎯 Начните сборку прямо сейчас!</h2>
      <p>Выберите подходящий бюджет и создайте идеальный компьютер</p>
      <div class="cta-buttons">
        <router-link to="/arrays" class="cta-btn primary">💻 Начать сборку</router-link>
        <router-link to="/backend-data" class="cta-btn secondary">📊 Посмотреть компоненты</router-link>
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
  max-width: 1200px;
  margin: 0 auto;
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
  margin-bottom: 1rem;
}

.price-examples {
  background: #e8f4fd;
  padding: 10px 20px;
  border-radius: 8px;
  display: inline-block;
  margin-bottom: 2rem;
  border-left: 4px solid #3498db;
}

.price-examples p {
  margin: 0;
  color: #2c3e50;
  font-weight: bold;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
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
  position: relative;
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
  margin-bottom: 1rem;
}

.feature-price {
  color: #27ae60 !important;
  font-weight: bold;
  font-size: 1.1em;
}

.feature-link {
  display: inline-block;
  background: #3498db;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  text-decoration: none;
  transition: background 0.3s ease;
  margin-top: 0.5rem;
}

.feature-link:hover {
  background: #2980b9;
}

.coming-soon {
  color: #e74c3c !important;
  font-style: italic;
  margin-top: 0.5rem;
}

.quick-stats {
  background: #f8f9fa;
  padding: 2rem;
  border-radius: 10px;
  margin-bottom: 3rem;
}

.quick-stats h2 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 2rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.stat-item {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.stat-item h4 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.stat-price {
  color: #27ae60;
  font-weight: bold;
  font-size: 1.2em;
  margin-bottom: 0.5rem;
}

.stat-item p {
  color: #7f8c8d;
  margin: 0;
}

.tech-stack {
  margin-bottom: 3rem;
}

.tech-stack h2 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 2rem;
}

.tech-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.tech-item {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.tech-item h4 {
  color: #2c3e50;
  margin-bottom: 1rem;
  text-align: center;
}

.tech-item ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.tech-item li {
  padding: 0.5rem 0;
  color: #7f8c8d;
  border-bottom: 1px solid #ecf0f1;
}

.tech-item li:last-child {
  border-bottom: none;
}

.cta-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 3rem;
  border-radius: 10px;
  text-align: center;
}

.cta-section h2 {
  margin-bottom: 1rem;
}

.cta-section p {
  margin-bottom: 2rem;
  opacity: 0.9;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.cta-btn {
  padding: 0.75rem 1.5rem;
  border-radius: 5px;
  text-decoration: none;
  font-weight: bold;
  transition: all 0.3s ease;
}

.cta-btn.primary {
  background: #f39c12;
  color: white;
}

.cta-btn.primary:hover {
  background: #e67e22;
  transform: translateY(-2px);
}

.cta-btn.secondary {
  background: transparent;
  color: white;
  border: 2px solid white;
}

.cta-btn.secondary:hover {
  background: white;
  color: #764ba2;
  transform: translateY(-2px);
}

/* Адаптивность */
@media (max-width: 768px) {
  .home {
    padding: 1rem;
  }
  
  .welcome h1 {
    font-size: 2rem;
  }
  
  .features {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .tech-grid {
    grid-template-columns: 1fr;
  }
  
  .cta-buttons {
    flex-direction: column;
    align-items: center;
  }
  
  .cta-btn {
    width: 200px;
  }
}
</style>