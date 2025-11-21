<!-- site_back/src/views/ReactiveView.vue -->
<template>
  <div class="reactive-view">
    <h1>🎯 Работа с реактивными переменными</h1>
    
    <div class="currency-note">
      💰 Все цены в долларах США ($)
    </div>
    
    <!-- Реактивное отображение данных -->
    <div class="demo-section">
      <h2>📊 Реактивные данные</h2>
      
      <div class="reactive-display">
        <p><strong>Имя:</strong> {{ userName }}</p>
        <p><strong>Возраст:</strong> {{ age }} лет</p>
        <p><strong>Бюджет:</strong> {{ formatPrice(budget) }}</p>
        <p><strong>Статус:</strong> 
          <span :class="statusClass">{{ statusMessage }}</span>
        </p>
      </div>

      <!-- Реактивное обновление данных -->
      <div class="controls">
        <h3>🔄 Изменение данных</h3>
        
        <div class="input-group">
          <label>Имя:</label>
          <input v-model="userName" type="text" placeholder="Введите имя">
        </div>
        
        <div class="input-group">
          <label>Возраст:</label>
          <input v-model.number="age" type="number" min="0" placeholder="Введите возраст">
        </div>
        
        <div class="input-group">
          <label>Бюджет ($):</label>
          <input v-model.number="budget" type="number" min="0" placeholder="Введите бюджет">
        </div>
        
        <div class="input-group">
          <label>Цвет темы:</label>
          <select v-model="themeColor" @change="updateTheme">
            <option value="blue">Синий</option>
            <option value="green">Зеленый</option>
            <option value="purple">Фиолетовый</option>
            <option value="orange">Оранжевый</option>
          </select>
        </div>
      </div>

      <!-- Реактивные вычисления -->
      <div class="computed-section">
        <h3>🧮 Вычисляемые свойства (Computed)</h3>
        
        <div class="computed-display">
          <p><strong>Год рождения:</strong> {{ birthYear }}</p>
          <p><strong>Можно купить видеокарт:</strong> {{ possibleGPUs }}</p>
          <p><strong>Категория бюджета:</strong> {{ budgetCategory }}</p>
          <p><strong>Цена сборки:</strong> {{ formatPrice(buildPrice) }}</p>
        </div>
      </div>

      <!-- Реактивные стили -->
      <div class="styling-section">
        <h3>🎨 Реактивные стили</h3>
        
        <div class="style-demo" 
             :style="{
               backgroundColor: themeColor + '20',
               borderColor: themeColor,
               color: textColor
             }">
          <p>Этот блок меняет стили реактивно</p>
          <p>Текущий цвет: {{ themeColor }}</p>
        </div>
        
        <div class="budget-meter">
          <div class="meter-background">
            <div class="meter-fill" :style="meterStyle"></div>
          </div>
          <p>Заполнение: {{ meterPercentage }}%</p>
        </div>
      </div>

      <!-- Реактивные классы -->
      <div class="class-section">
        <h3>🏷️ Реактивные классы</h3>
        
        <div :class="[
          'status-box',
          budgetStatus
        ]">
          <p>{{ budgetStatusText }}</p>
        </div>
        
        <button @click="togglePremium" 
                :class="{
                  'btn': true,
                  'btn-premium': isPremium,
                  'btn-standard': !isPremium
                }">
          {{ isPremium ? '⭐ Премиум режим' : '⚡ Стандартный режим' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ReactiveView',
  data() {
    return {
      // Реактивные переменные
      userName: 'Иван',
      age: 25,
      budget: 1500,
      themeColor: 'blue',
      isPremium: false,
      baseBuildPrice: 800
    }
  },
  computed: {
    // Вычисляемые свойства (реактивные)
    birthYear() {
      const currentYear = new Date().getFullYear();
      return currentYear - this.age;
    },
    
    possibleGPUs() {
      const gpuPrice = 500; // Цена видеокарты в долларах
      return Math.floor(this.budget / gpuPrice);
    },
    
    budgetCategory() {
      if (this.budget < 500) return 'Бюджетный';
      if (this.budget < 1200) return 'Средний';
      if (this.budget < 2500) return 'Высокий';
      return 'Элитный';
    },
    
    buildPrice() {
      let price = this.baseBuildPrice;
      if (this.isPremium) {
        price *= 1.5; // Премиум сборка дороже
      }
      if (this.age > 30) {
        price *= 0.9; // Скидка за возраст
      }
      return Math.round(price);
    },
    
    statusMessage() {
      if (this.budget >= this.buildPrice) {
        return 'Можно собрать ПК';
      } else {
        return 'Бюджет недостаточен';
      }
    },
    
    statusClass() {
      return this.budget >= this.buildPrice ? 'status-success' : 'status-error';
    },
    
    textColor() {
      const colors = {
        blue: '#2c3e50',
        green: '#27ae60',
        purple: '#8e44ad',
        orange: '#e67e22'
      };
      return colors[this.themeColor] || '#2c3e50';
    },
    
    meterPercentage() {
      const maxBudget = 3000;
      return Math.min((this.budget / maxBudget) * 100, 100);
    },
    
    meterStyle() {
      return {
        width: this.meterPercentage + '%',
        backgroundColor: this.themeColor
      };
    },
    
    budgetStatus() {
      if (this.budget < 500) return 'budget-low';
      if (this.budget < 1500) return 'budget-medium';
      return 'budget-high';
    },
    
    budgetStatusText() {
      switch (this.budgetStatus) {
        case 'budget-low': return '🟡 Низкий бюджет';
        case 'budget-medium': return '🟢 Средний бюджет';
        case 'budget-high': return '🔴 Высокий бюджет';
        default: return '⚪ Неопределен';
      }
    }
  },
  methods: {
    // Форматирование цены в доллары
    formatPrice(price) {
      if (!price) return '$0';
      return `$${price}`;
    },

    updateTheme() {
      console.log('Тема изменена на:', this.themeColor);
    },
    
    togglePremium() {
      this.isPremium = !this.isPremium;
    }
  },
  // Наблюдатели за изменениями
  watch: {
    budget(newBudget, oldBudget) {
      console.log(`Бюджет изменился: $${oldBudget} → $${newBudget}`);
      
      if (newBudget > oldBudget) {
        console.log('🎉 Бюджет увеличен!');
      } else if (newBudget < oldBudget) {
        console.log('📉 Бюджет уменьшен');
      }
    },
    
    userName(newName) {
      console.log('Имя пользователя изменено на:', newName);
    }
  }
}
</script>

<style scoped>
.reactive-view {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.currency-note {
  background: #e8f4fd;
  padding: 10px 15px;
  border-radius: 5px;
  margin-bottom: 15px;
  border-left: 4px solid #3498db;
  font-weight: bold;
  color: #2c3e50;
  text-align: center;
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
  transition: all 0.3s ease;
}

.budget-meter {
  margin: 20px 0;
}

.meter-background {
  width: 100%;
  height: 20px;
  background: #ecf0f1;
  border-radius: 10px;
  overflow: hidden;
}

.meter-fill {
  height: 100%;
  transition: width 0.5s ease;
}

.status-box {
  padding: 15px;
  border-radius: 8px;
  margin: 10px 0;
  font-weight: bold;
  text-align: center;
}

.budget-low {
  background: #fff3cd;
  border: 1px solid #ffeaa7;
  color: #856404;
}

.budget-medium {
  background: #d1ecf1;
  border: 1px solid #bee5eb;
  color: #0c5460;
}

.budget-high {
  background: #f8d7da;
  border: 1px solid #f5c6cb;
  color: #721c24;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: all 0.3s ease;
}

.btn-premium {
  background: linear-gradient(135deg, #ffd700, #ffed4e);
  color: #000;
}

.btn-standard {
  background: #3498db;
  color: white;
}

.status-success {
  color: #27ae60;
  font-weight: bold;
}

.status-error {
  color: #e74c3c;
  font-weight: bold;
}

.computed-section, .styling-section, .class-section {
  background: white;
  padding: 20px;
  border-radius: 8px;
  margin: 20px 0;
  border: 1px solid #e9ecef;
}
</style>