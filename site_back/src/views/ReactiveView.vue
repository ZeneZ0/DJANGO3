
<template>
  <div class="reactive-view">
    <h1>🎯 Работа с реактивными переменными</h1>
    
    <div class="demo-section">
      <h2>📊 Реактивные данные</h2>
      
      <div class="reactive-display">
        <p><strong>Имя:</strong> {{ userName }}</p>
        <p><strong>Бюджет:</strong> {{ budget }} руб.</p>
        <p><strong>Статус:</strong> 
          <span :class="statusClass">{{ statusMessage }}</span>
        </p>
      </div>

      <div class="controls">
        <h3>🔄 Изменение данных</h3>
        
        <div class="input-group">
          <label>Имя:</label>
          <input v-model="userName" type="text">
        </div>
        
        <div class="input-group">
          <label>Бюджет:</label>
          <input v-model.number="budget" type="number">
        </div>
        
        <div class="input-group">
          <label>Цвет темы:</label>
          <select v-model="themeColor">
            <option value="blue">Синий</option>
            <option value="green">Зеленый</option>
            <option value="purple">Фиолетовый</option>
          </select>
        </div>
      </div>

      <div class="computed-section">
        <h3>🧮 Вычисляемые свойства</h3>
        
        <div class="computed-display">
          <p><strong>Можно купить видеокарт:</strong> {{ possibleGPUs }}</p>
          <p><strong>Категория бюджета:</strong> {{ budgetCategory }}</p>
        </div>
      </div>

      <div class="styling-section">
        <h3>🎨 Реактивные стили</h3>
        
        <div class="style-demo" 
             :style="{
               backgroundColor: themeColor + '20',
               borderColor: themeColor
             }">
          <p>Этот блок меняет стили реактивно</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ReactiveView',
  data() {
    return {
      userName: 'Иван',
      budget: 50000,
      themeColor: 'blue'
    }
  },
  computed: {
    possibleGPUs() {
      const gpuPrice = 50000;
      return Math.floor(this.budget / gpuPrice);
    },
    
    budgetCategory() {
      if (this.budget < 30000) return 'Бюджетный';
      if (this.budget < 70000) return 'Средний';
      return 'Высокий';
    },
    
    statusMessage() {
      return this.budget >= 30000 ? 'Можно собрать ПК' : 'Бюджет недостаточен';
    },
    
    statusClass() {
      return this.budget >= 30000 ? 'status-success' : 'status-error';
    }
  }
}
</script>

<style scoped>
.reactive-view {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.demo-section {
  margin-bottom: 30px;
}

.reactive-display, .computed-display {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  margin: 15px 0;
}

.controls {
  background: white;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.input-group {
  margin: 10px 0;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input, select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.style-demo {
  padding: 20px;
  border-radius: 8px;
  margin: 15px 0;
  border: 2px solid;
}

.status-success {
  color: #27ae60;
  font-weight: bold;
}

.status-error {
  color: #e74c3c;
  font-weight: bold;
}
</style>