import { createStore } from 'vuex'

function getCookie(name) {
  let cookieValue = null
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}

export default createStore({
  state: {
    user: {
      is_authenticated: false,
      username: '',
      is_superuser: false
    }
  },
  mutations: {
    SET_USER(state, userData) {
      state.user = userData
    },
    CLEAR_USER(state) {
      state.user = {
        is_authenticated: false,
        username: '',
        is_superuser: false
      }
    }
  },
  actions: {
    async checkAuth({ commit }) {
      try {
        const response = await fetch('/api/auth/user/')
        const data = await response.json()
        commit('SET_USER', {
          is_authenticated: data.is_authenticated,
          username: data.username || '',
          is_superuser: data.is_superuser || false
        })
        return data
      } catch (error) {
        console.error('Auth check failed', error)
        commit('CLEAR_USER')
      }
    },
    async login({ dispatch }, credentials) {
      try {
        const response = await fetch('/api/auth/login/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
          },
          body: JSON.stringify(credentials)
        })
        
        if (response.ok) {
          const data = await response.json()
          await dispatch('checkAuth')
          return { success: true, data }
        } else {
          return { success: false, error: 'Неверные данные' }
        }
      } catch (error) {
        console.error('Login failed', error)
        return { success: false, error: 'Ошибка сервера' }
      }
    },
    async logout({ commit }) {
      try {
        await fetch('/api/auth/logout/', {
          method: 'POST',
          headers: {
            'X-CSRFToken': getCookie('csrftoken')
          }
        })
        commit('CLEAR_USER')
        return { success: true }
      } catch (error) {
        console.error('Logout failed', error)
        return { success: false, error: 'Ошибка сервера' }
      }
    }
  },
  getters: {
    isAuthenticated: state => state.user.is_authenticated,
    username: state => state.user.username,
    isSuperUser: state => state.user.is_superuser
  }
})