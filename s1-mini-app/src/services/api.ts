import axios, { AxiosInstance } from 'axios';
import { getTelegramAuthHeaders } from '../lib/telegram';

// Базовый URL API - работает только через Telegram с авторизацией
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

/**
 * Создание Axios instance с предустановленными настройками
 */
const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

/**
 * Интерцептор для автоматического добавления Telegram initData
 */
api.interceptors.request.use((config) => {
  const telegramHeaders = getTelegramAuthHeaders();
  
  if (telegramHeaders['X-Telegram-Init-Data']) {
    config.headers['X-Telegram-Init-Data'] = telegramHeaders['X-Telegram-Init-Data'];
  }
  
  return config;
}, (error) => {
  return Promise.reject(error);
});

/**
 * Интерцептор для обработки ошибок
 */
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    
    // Обработка ошибок авторизации
    if (error.response?.status === 401) {
      console.warn('Unauthorized - проверьте валидность Telegram initData');
    }
    
    return Promise.reject(error);
  }
);

export default api;
