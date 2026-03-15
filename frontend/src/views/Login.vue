<template>
  <div class="login-container">
    <div class="login-card">
      <div class="brand">MIROFISH</div>
      <p class="subtitle">Enter password to continue</p>

      <form @submit.prevent="handleLogin" class="login-form">
        <input
          v-model="password"
          type="password"
          placeholder="Password"
          class="password-input"
          :class="{ 'input-error': error }"
          autofocus
          @input="error = ''"
        />
        <p v-if="error" class="error-text">{{ error }}</p>
        <button type="submit" class="login-btn" :disabled="loading">
          {{ loading ? '...' : 'Enter' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '../api/auth'

const router = useRouter()
const password = ref('')
const error = ref('')
const loading = ref(false)

async function handleLogin() {
  if (!password.value.trim()) {
    error.value = 'Password required'
    return
  }

  loading.value = true
  error.value = ''

  try {
    const res = await login(password.value)
    if (res.success && res.token) {
      localStorage.setItem('mirofish_token', res.token)
      router.replace('/')
    } else {
      error.value = res.error || 'Login failed'
    }
  } catch (e) {
    error.value = 'Wrong password'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #ffffff;
}

.login-card {
  width: 100%;
  max-width: 360px;
  padding: 0 24px;
}

.brand {
  font-size: 32px;
  font-weight: 700;
  letter-spacing: 4px;
  color: #000;
  margin-bottom: 8px;
}

.subtitle {
  color: #888;
  font-size: 14px;
  margin-bottom: 32px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.password-input {
  width: 100%;
  padding: 12px 16px;
  font-family: inherit;
  font-size: 16px;
  border: 2px solid #000;
  background: #fff;
  outline: none;
  transition: border-color 0.2s;
}

.password-input:focus {
  border-color: #000;
  box-shadow: 3px 3px 0 #000;
}

.password-input.input-error {
  border-color: #e53e3e;
}

.error-text {
  color: #e53e3e;
  font-size: 13px;
  margin: 0;
}

.login-btn {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 2px;
  background: #000;
  color: #fff;
  border: 2px solid #000;
  cursor: pointer;
  transition: all 0.15s;
}

.login-btn:hover:not(:disabled) {
  background: #fff;
  color: #000;
}

.login-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
