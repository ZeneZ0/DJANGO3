<script>
export default {
  name: 'LoginView',
  data() {
    return {
      username: '',
      password: '',
      error: '',
      loading: false
    }
  },
  methods: {
    async handleLogin() {
      this.loading = true
      this.error = ''
      try {
        const result = await this.$store.dispatch('login', {
          username: this.username,
          password: this.password
        })
        
        if (result.success) {
          this.$router.push('/')
        } else {
          this.error = result.error || 'Неверное имя пользователя или пароль'
        }
      } catch (err) {
        this.error = 'Ошибка сервера'
        console.error(err)
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<template>
  <div class="login-container">
    <div class="card login-card">
      <div class="card-header bg-primary text-white">
        <h4 class="mb-0">Вход в систему</h4>
      </div>
      <div class="card-body">
        <form @submit.prevent="handleLogin">
          <div class="mb-3">
            <label class="form-label">Имя пользователя</label>
            <input v-model="username" type="text" class="form-control" required autofocus>
          </div>
          <div class="mb-3">
            <label class="form-label">Пароль</label>
            <input v-model="password" type="password" class="form-control" required>
          </div>
          <div v-if="error" class="alert alert-danger">
            {{ error }}
          </div>
          <button type="submit" class="btn btn-primary w-100" :disabled="loading">
            {{ loading ? 'Вход...' : 'Войти' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 200px);
}

.login-card {
  width: 100%;
  max-width: 400px;
}
</style>