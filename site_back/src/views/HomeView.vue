<script>
export default {
  name: 'HomeView'
}
</script>

<template>
  <div class="home">
    <div class="header">
      <h1>Конфигуратор ПК</h1>
      <p>Создайте идеальный компьютер</p>
    </div>

    <div class="content">
      <div class="features">
        <div class="feature">
          <h3>Реактивные переменные</h3>
          <p>Пример работы с Vue 3</p>
          <router-link to="/reactive" class="btn btn-primary">Перейти</router-link>
        </div>
        
        <div class="feature">
          <h3>Работа с массивами</h3>
          <p>Списки компонентов ПК</p>
          <router-link to="/arrays" class="btn btn-primary">Перейти</router-link>
        </div>
        
        <div class="feature">
          <h3>Данные с сервера</h3>
          <p>Работа с Django API</p>
          <router-link to="/backend-data" class="btn btn-primary">Перейти</router-link>
        </div>
        
        <div class="feature">
          <h3>Каталог</h3>
          <p>Все компоненты ПК</p>
          <router-link to="/components" class="btn btn-primary">Перейти</router-link>
        </div>
      </div>

      <div class="info">
        <div class="info-card">
          <h4>Бюджетные сборки</h4>
          <p>От $500</p>
          <p>Для офиса и учебы</p>
        </div>
        
        <div class="info-card">
          <h4>Игровые сборки</h4>
          <p>$1000 - $2000</p>
          <p>Для комфортного гейминга</p>
        </div>
        
        <div class="info-card">
          <h4>Профессиональные</h4>
          <p>От $2000</p>
          <p>Для работы с графикой</p>
        </div>
      </div>

      <div class="cta">
        <h3>Начать сборку</h3>
        <p>Выберите компоненты и соберите компьютер</p>
        <div class="cta-buttons">
          <router-link to="/components" class="btn btn-success">Каталог</router-link>
          <router-link to="/configs" class="btn btn-info">Готовые сборки</router-link>
        </div>
      </div>
    </div>
  </div>
</template>



<style scoped>
.home {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  text-align: center;
  margin-bottom: 30px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.header h1 {
  color: #333;
  margin-bottom: 10px;
}

.header p {
  color: #666;
  font-size: 18px;
}

.content {
  padding: 20px;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.feature {
  background: white;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #ddd;
  text-align: center;
}

.feature h3 {
  margin-bottom: 10px;
  color: #333;
}

.feature p {
  color: #666;
  margin-bottom: 15px;
}

.info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.info-card {
  background: #e8f4fd;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  border: 1px solid #cce7ff;
}

.info-card h4 {
  margin-bottom: 10px;
  color: #0056b3;
}

.info-card p {
  margin: 5px 0;
  color: #333;
}

.cta {
  background: #007bff;
  color: white;
  padding: 30px;
  border-radius: 8px;
  text-align: center;
}

.cta h3 {
  margin-bottom: 10px;
}

.cta p {
  margin-bottom: 20px;
  opacity: 0.9;
}

.cta-buttons {
  display: flex;
  gap: 15px;
  justify-content: center;
}

.btn {
  display: inline-block;
  padding: 8px 16px;
  border-radius: 4px;
  text-decoration: none;
  font-weight: bold;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-success {
  background: #28a745;
  color: white;
}

.btn-info {
  background: #17a2b8;
  color: white;
}

.btn:hover {
  opacity: 0.9;
}

@media (max-width: 768px) {
  .features,
  .info {
    grid-template-columns: 1fr;
  }
  
  .cta-buttons {
    flex-direction: column;
    align-items: center;
  }
  
  .cta-buttons .btn {
    width: 200px;
  }
}
</style>