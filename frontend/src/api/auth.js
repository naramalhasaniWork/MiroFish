import axios from 'axios'

const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5001'

export async function login(password) {
  const res = await axios.post(`${baseURL}/api/auth/login`, { password })
  return res.data
}

export function getToken() {
  return localStorage.getItem('mirofish_token')
}

export function clearToken() {
  localStorage.removeItem('mirofish_token')
}

export function isAuthenticated() {
  return !!getToken()
}
