<template>
  <div class="about">
    <div class="container py-5">
      <h1 class="mb-4">О проекте Конфигуратор ПК</h1>
      
      <div class="row">
        <div class="col-md-8">
          <div class="card mb-4">
            <div class="card-body">
              <h5 class="card-title">🎮 Конфигуратор ПК</h5>
              <p class="card-text">
                Учебный проект для изучения веб-разработки с использованием Vue.js и Django.
                Позволяет собирать компьютеры из различных компонентов, управлять производителями,
                типами комплектующих и создавать запросы на сборку.
              </p>
            </div>
          </div>

          <div class="card mb-4">
            <div class="card-body">
              <h5 class="card-title">🛠️ Технологии</h5>
              <ul class="list-group list-group-flush">
                <li class="list-group-item">
                  <strong>Frontend:</strong> Vue.js 3, Vue Router, Bootstrap 5
                </li>
                <li class="list-group-item">
                  <strong>Backend:</strong> Django, Django REST Framework
                </li>
                <li class="list-group-item">
                  <strong>База данных:</strong> SQLite / PostgreSQL
                </li>
                <li class="list-group-item">
                  <strong>Дополнительно:</strong> Axios для API запросов
                </li>
              </ul>
            </div>
          </div>
        </div>

        <div class="col-md-4">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">🚀 Возможности</h5>
              <ul class="list-unstyled">
                <li class="mb-2">✅ Работа с реактивными переменными</li>
                <li class="mb-2">✅ Управление массивами данных</li>
                <li class="mb-2">✅ CRUD операции для компонентов</li>
                <li class="mb-2">✅ Загрузка изображений</li>
                <li class="mb-2">✅ Фильтрация и поиск</li>
                <li class="mb-2">✅ Работа с REST API</li>
                <li class="mb-2">✅ Валидация форм</li>
              </ul>
            </div>
          </div>

          <div class="card mt-4">
            <div class="card-body">
              <h5 class="card-title">📊 Структура данных</h5>
              <ul class="list-unstyled">
                <li class="mb-1">🏭 Производители</li>
                <li class="mb-1">🏷️ Типы компонентов</li>
                <li class="mb-1">💻 Компьютерные компоненты</li>
                <li class="mb-1">🖥️ Конфигурации ПК</li>
                <li class="mb-1">📝 Запросы на сборку</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <div class="card mt-4">
        <div class="card-body text-center">
          <h5 class="card-title">🎯 Цель проекта</h5>
          <p class="card-text">
            Демонстрация базовых принципов веб-разработки: работа с фронтендом на Vue.js,
            создание REST API на Django, управление данными и построение полноценного веб-приложения.
          </p>
          <router-link to="/" class="btn btn-primary">Вернуться на главную</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AboutView'
}
</script>

<style>
.about {
  min-height: calc(100vh - 56px); /* Учитываем высоту навбара */
  background-color: #f8f9fa;
}

.card {
  border: none;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.card-title {
  color: #2c3e50;
  border-bottom: 2px solid #3498db;
  padding-bottom: 10px;
  margin-bottom: 15px;
}

.list-group-item {
  border: none;
  padding-left: 0;
  padding-right: 0;
}
</style>