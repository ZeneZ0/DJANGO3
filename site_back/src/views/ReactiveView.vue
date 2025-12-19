<script>
export default {
  name: 'ReactiveView',
  data() {
    return {
      name: 'Иван',
      age: 25,
      budget: 1500,
      boxColor: '#e8f4fd'
    }
  },
  computed: {
    birthYear() {
      return 2024 - this.age;
    },
    
    budgetCategory() {
      if (this.budget < 500) return 'Бюджетный';
      if (this.budget < 1200) return 'Средний';
      if (this.budget < 2500) return 'Высокий';
      return 'Элитный';
    },
    
    buildPrice() {
      return 500 + (this.age * 20);
    },
    
    statusText() {
      if (this.budget >= this.buildPrice) {
        return 'Достаточно';
      } else {
        return 'Мало';
      }
    },
    
    statusClass() {
      return this.budget >= this.buildPrice ? 'status-ok' : 'status-bad';
    }
  },
  watch: {
    budget(newVal, oldVal) {
      console.log('Бюджет изменился с', oldVal, 'на', newVal);
    }
  }
}
</script>

<template>
  <div class="reactive">
    <h1>Реактивные переменные</h1>
    
    <div class="demo">
      <h2>Основные данные</h2>
      
      <div class="data-show">
        <p>Имя: {{ name }}</p>
        <p>Возраст: {{ age }} лет</p>
        <p>Бюджет: ${{ budget }}</p>
        <p>Статус: 
          <span class="status" :class="statusClass">{{ statusText }}</span>
        </p>
      </div>

      <div class="controls">
        <h3>Изменение данных</h3>
        
        <div class="control-item">
          <label>Имя:</label>
          <input v-model="name" type="text">
        </div>
        
        <div class="control-item">
          <label>Возраст:</label>
          <input v-model.number="age" type="number">
        </div>
        
        <div class="control-item">
          <label>Бюджет:</label>
          <input v-model.number="budget" type="number">
        </div>
      </div>

      <div class="computed">
        <h3>Вычисляемые значения</h3>
        
        <div class="computed-data">
          <p>Год рождения: {{ birthYear }}</p>
          <p>Категория бюджета: {{ budgetCategory }}</p>
          <p>Цена сборки: ${{ buildPrice }}</p>
        </div>
      </div>

      <div class="styles">
        <h3>Реактивные стили</h3>
        
        <div class="color-box" :style="{ backgroundColor: boxColor }">
          <p>Цвет блока: {{ boxColor }}</p>
        </div>
        
        <select v-model="boxColor">
          <option value="#e8f4fd">Голубой</option>
          <option value="#d5f4e6">Зеленый</option>
          <option value="#f9e2e2">Красный</option>
          <option value="#f4e2f9">Фиолетовый</option>
        </select>
      </div>
    </div>
  </div>
</template>



<style>
.reactive {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.demo {
  background: white;
  padding: 20px;
  border-radius: 8px;
  border: 1px solid #ddd;
}

.data-show {
  background: #f5f5f5;
  padding: 15px;
  border-radius: 6px;
  margin-bottom: 20px;
}

.data-show p {
  margin: 8px 0;
  font-size: 16px;
}

.controls {
  margin: 20px 0;
}

.control-item {
  margin: 15px 0;
}

.control-item label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.control-item input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
}

.computed {
  margin: 20px 0;
  padding: 15px;
  background: #f9f9f9;
  border-radius: 6px;
}

.computed-data p {
  margin: 10px 0;
}

.styles {
  margin-top: 20px;
}

.color-box {
  padding: 20px;
  border-radius: 6px;
  margin: 15px 0;
  border: 2px solid #ddd;
}

select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
}

.status {
  padding: 3px 8px;
  border-radius: 4px;
  font-weight: bold;
}

.status-ok {
  background: #d4edda;
  color: #155724;
}

.status-bad {
  background: #f8d7da;
  color: #721c24;
}

h1, h2, h3 {
  color: #333;
}

h1 {
  border-bottom: 2px solid #3498db;
  padding-bottom: 10px;
}
</style>