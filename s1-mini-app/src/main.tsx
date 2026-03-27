import React from 'react';
import ReactDOM from 'react-dom/client';
import { App } from './App.tsx';
import './index.css';

/**
 * Инициализация Telegram Web App
 */
if (typeof window !== 'undefined' && (window as any).Telegram?.WebApp) {
  const tg = (window as any).Telegram.WebApp;
  
  // Готовность приложения
  tg.ready();
  
  // Разворачиваем на весь экран
  tg.expand();
  
  // Применяем тему
  document.documentElement.style.setProperty('--tg-theme-bg-color', tg.themeParams.bg_color);
  document.documentElement.style.setProperty('--tg-theme-text-color', tg.themeParams.text_color);
  document.documentElement.style.setProperty('--tg-theme-hint-color', tg.themeParams.hint_color);
  document.documentElement.style.setProperty('--tg-theme-link-color', tg.themeParams.link_color);
  document.documentElement.style.setProperty('--tg-theme-button-color', tg.themeParams.button_color);
  document.documentElement.style.setProperty('--tg-theme-button-text-color', tg.themeParams.button_text_color);
  document.documentElement.style.setProperty('--tg-theme-secondary-bg-color', tg.themeParams.secondary_bg_color);
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
