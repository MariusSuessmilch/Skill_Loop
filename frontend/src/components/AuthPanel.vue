<template>
  <div class="auth-panel">
    <div v-if="mode === 'login'">
      <h2>Login</h2>
      <form @submit.prevent="login">
        <input v-model="email" type="email" placeholder="Email" required />
        <input v-model="password" type="password" placeholder="Password" required />
        <button type="submit">Login</button>
      </form>
      <p>
        No account?
        <a href="#" @click.prevent="mode = 'register'">Register here</a>
      </p>
      <div v-if="error" class="auth-error">{{ error }}</div>
    </div>
    <div v-else>
      <h2>Register</h2>
      <form @submit.prevent="register">
        <input v-model="email" type="email" placeholder="Email" required />
        <input v-model="password" type="password" placeholder="Password" required />
        <button type="submit">Register</button>
      </form>
      <p>
        Already have an account?
        <a href="#" @click.prevent="mode = 'login'">Login here</a>
      </p>
      <div v-if="error" class="auth-error">{{ error }}</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AuthPanel',
  data() {
    return {
      mode: 'login',
      email: '',
      password: '',
      error: ''
    }
  },
  methods: {
    async login() {
      this.error = ''
      try {
        const res = await axios.post('/api/auth/jwt/login', {
          username: this.email,
          password: this.password
        }, { withCredentials: true })
        this.$emit('login-success', res.data)
      } catch (e) {
        this.error = 'Login failed. Check your credentials.'
      }
    },
    async register() {
      this.error = ''
      try {
        await axios.post('/api/auth/register', {
          email: this.email,
          password: this.password
        })
        this.mode = 'login'
      } catch (e) {
        this.error = 'Registration failed. Email may already be in use.'
      }
    }
  }
}
</script>

<style scoped>
.auth-panel {
  max-width: 300px;
  margin: 2em auto;
  padding: 2em;
  border-radius: 8px;
  background: #232836;
  color: #fff;
  box-shadow: 0 4px 24px #0002;
}
.auth-panel h2 {
  margin-bottom: 1em;
}
.auth-panel input {
  width: 100%;
  margin-bottom: 1em;
  padding: 0.6em;
  border: none;
  border-radius: 4px;
  background: #181b26;
  color: #fff;
}
.auth-panel button {
  width: 100%;
  padding: 0.7em;
  background: #059669;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-weight: bold;
}
.auth-panel .auth-error {
  margin-top: 1em;
  color: #ff6b6b;
}
.auth-panel a {
  color: #38bdf8;
  cursor: pointer;
}
</style>
