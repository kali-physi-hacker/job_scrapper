import axios from 'axios'

export const API_BASE = import.meta.env.VITE_API_URL?.toString() || 'http://localhost:8000'

export const api = axios.create({
  baseURL: `${API_BASE}/api`,
  withCredentials: true,
})

export function getCookie(name: string) {
  return document.cookie.split('; ').find(row => row.startsWith(name + '='))?.split('=')[1]
}

api.interceptors.request.use(config => {
  const csrftoken = getCookie('csrftoken')
  if (csrftoken) {
    config.headers = { ...config.headers, 'X-CSRFToken': csrftoken }
  }
  return config
})

