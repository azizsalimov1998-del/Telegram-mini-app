import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  base: '/', // Важно для Telegram Mini App
  server: {
    host: '0.0.0.0', // Разрешить подключения извне
    allowedHosts: [
      'episode-core-tumor-answer.trycloudflare.com',
      '.trycloudflare.com', // Разрешить все поддомены cloudflare
      'localhost',
      '127.0.0.1'
    ],
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false,
      }
    }
  }
})
