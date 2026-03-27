# S1 Mini App

Telegram Mini App для интернет-магазина S1.

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
cd s1-mini-app
npm install
```

### 2. Настройка окружения

Создайте файл `.env` на основе `.env.example`:

```bash
cp .env.example .env
```

Отредактируйте `.env` и укажите URL вашего бэкенда:

```env
VITE_API_URL=http://localhost:5000/api
```

### 3. Запуск разработки

```bash
npm run dev
```

Приложение будет доступно по адресу `http://localhost:5173`

### 4. Тестирование в Telegram

Для тестирования в Telegram:

1. Задеплойте приложение (например, на Vercel)
2. В @BotFather создайте Web App через команду `/newapp`
3. Укажите URL вашего приложения
4. Откройте через кнопку меню в боте

## 📁 Структура проекта

```
src/
├── components/     # React компоненты
│   └── Header.tsx
├── pages/         # Страницы приложения
│   └── Catalog.tsx
├── store/         # Zustand store (состояние)
├── services/      # API сервисы
│   └── api.ts
├── types/         # TypeScript типы
├── lib/           # Утилиты и хуки
│   ├── telegram.ts
│   └── useBackNavigation.ts
├── App.tsx        # Основной компонент
├── main.tsx       # Точка входа
└── index.css      # Глобальные стили
```

## 🛠 Технологический стек

- **React 19** - UI библиотека
- **TypeScript** - Типизация
- **Vite** - Сборщик
- **Tailwind CSS** - Стилизация
- **Zustand** - Управление состоянием
- **React Router** - Роутинг
- **@tma.js/sdk-react** - Telegram Mini App SDK
- **Axios** - HTTP клиент
- **Lucide React** - Иконки

## 📋 Текущий статус

✅ **Phase 0**: Инициализация проекта
- [x] Создание Vite + React + TypeScript проекта
- [x] Настройка Tailwind CSS
- [x] Базовая структура папок
- [x] Конфигурационные файлы

✅ **Phase 1**: Базовая интеграция Telegram
- [x] TMA SDK инициализация
- [x] Telegram utilities (telegram.ts)
- [x] Применение темы Telegram
- [x] React Router настройка
- [x] Header компонент с BackButton
- [x] Базовая страница Catalog

⏳ **Следующие шаги**: Phase 2 - API слой

## 🔗 Ссылки

- [Бэкенд S1](https://github.com/nannyy98/S1)
- [Telegram Web Apps](https://core.telegram.org/bots/webapps)
- [@tma.js/sdk-react](https://docs.tma.ru/docs/sdk/js/packages/react)
