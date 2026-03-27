# 📡 TELEGRAM MINI APP - REST API DOCUMENTATION

Полная документация по всем API endpoints для Telegram Mini App.

---

## 🔐 АВТОРИЗАЦИЯ

Все запросы к API должны включать заголовок:

```
X-Telegram-Init-Data: <initData из Telegram WebApp>
```

**Пример получения initData на фронтенде:**

```typescript
import { useRawInitData } from '@tma.js/sdk-react';

const initDataRaw = useRawInitData();

// В axios interceptors:
config.headers['X-Telegram-Init-Data'] = initDataRaw;
```

---

## 📁 КАТЕГОРИИ

### GET /api/categories

Получить список всех активных категорий.

**Headers:**
- `X-Telegram-Init-Data` (required)

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Электроника",
      "emoji": "📱",
      "image_url": "https://...",
      "is_active": true,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

---

### GET /api/categories/:id

Получить категорию по ID.

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Электроника",
    "emoji": "📱",
    "image_url": "https://...",
    "is_active": true
  }
}
```

---

## 🛍️ ТОВАРЫ

### GET /api/products

Получить список товаров с фильтрацией и пагинацией.

**Query Parameters:**
- `category_id` (integer) - фильтр по категории
- `subcategory_id` (integer) - фильтр по подкатегории
- `search` (string) - поисковый запрос
- `min_price` (float) - минимальная цена
- `max_price` (float) - максимальная цена
- `limit` (integer, default: 50) - количество товаров
- `offset` (integer, default: 0) - смещение

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "iPhone 15 Pro",
      "description": "Флагманский смартфон...",
      "price": 1200.00,
      "cost_price": 900.00,
      "original_price": 1400.00,
      "category_id": 1,
      "subcategory_id": 10,
      "brand": "Apple",
      "image_url": "https://...",
      "stock": 50,
      "views": 1234,
      "sales_count": 89,
      "is_active": true,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-02T00:00:00Z",
      "discount_percent": 14
    }
  ],
  "total": 100,
  "limit": 50,
  "offset": 0
}
```

---

### GET /api/products/:id

Получить товар по ID.

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "iPhone 15 Pro",
    "description": "...",
    "price": 1200.00,
    "original_price": 1400.00,
    "discount_percent": 14,
    ...
  }
}
```

---

### GET /api/products/search

Поиск товаров.

**Query Parameters:**
- `q` (string, required) - поисковый запрос (минимум 2 символа)

**Response:** Аналогично `GET /api/products`

---

### POST /api/products/:id/views

Увеличить счетчик просмотров товара.

**Response:**
```json
{
  "success": true,
  "message": "Просмотры обновлены"
}
```

---

### GET /api/products/:id/related

Получить похожие товары.

**Query Parameters:**
- `limit` (integer, default: 4) - количество товаров

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 2,
      "name": "iPhone 15",
      "price": 900.00,
      "original_price": 1000.00,
      "image_url": "https://...",
      "stock": 30,
      "discount_percent": 10
    }
  ]
}
```

---

## 🛒 КОРЗИНА

### GET /api/cart

Получить корзину пользователя.

**Response:**
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": 1,
        "product_id": 5,
        "quantity": 2,
        "added_at": "2024-01-01T00:00:00Z",
        "product": {
          "id": 5,
          "name": "Товар",
          "price": 100.00,
          "image_url": "https://..."
        }
      }
    ],
    "total_amount": 200.00,
    "total_items": 2
  }
}
```

---

### POST /api/cart

Добавить товар в корзину.

**Body:**
```json
{
  "product_id": 5,
  "quantity": 2
}
```

**Response:**
```json
{
  "success": true,
  "message": "Товар добавлен в корзину"
}
```

---

### PATCH /api/cart/:item_id

Обновить количество товара в корзине.

**Body:**
```json
{
  "quantity": 3
}
```

**Response:**
```json
{
  "success": true,
  "message": "Количество обновлено"
}
```

---

### DELETE /api/cart/:item_id

Удалить товар из корзины.

**Response:**
```json
{
  "success": true,
  "message": "Товар удален из корзины"
}
```

---

### POST /api/cart/clear

Очистить всю корзину.

**Response:**
```json
{
  "success": true,
  "message": "Корзина очищена"
}
```

---

## 📦 ЗАКАЗЫ

### POST /api/orders

Создать новый заказ.

**Body:**
```json
{
  "delivery_address": "г. Ташкент, ул. Чиланзар, д. 10",
  "payment_method": "cash",
  "comment": "Домофон не работает"
}
```

**Payment Methods:**
- `cash` - наличными при получении
- `payme` - Payme
- `click` - Click
- `card` - банковской картой

**Response:**
```json
{
  "success": true,
  "data": {
    "order_id": 123,
    "total_amount": 2500.00
  },
  "message": "Заказ успешно оформлен"
}
```

---

### GET /api/orders

Получить все заказы пользователя.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 123,
      "total_amount": 2500.00,
      "delivery_address": "г. Ташкент, ул. Чиланзар, д. 10",
      "payment_method": "cash",
      "status": "pending",
      "comment": "Домофон не работает",
      "created_at": "2024-01-01T00:00:00Z",
      "items": [
        {
          "product_id": 5,
          "quantity": 2,
          "price": 100.00,
          "name": "Товар"
        }
      ]
    }
  ]
}
```

**Order Statuses:**
- `pending` - ожидает подтверждения
- `confirmed` - подтвержден
- `processing` - в обработке
- `shipped` - отправлен
- `delivered` - доставлен
- `cancelled` - отменен
- `refunded` - возвращен

---

### GET /api/orders/:id

Получить заказ по ID.

**Response:** Аналогично `GET /api/orders` с деталями одного заказа.

---

### POST /api/orders/:id/cancel

Отменить заказ.

**Response:**
```json
{
  "success": true,
  "message": "Заказ отменен"
}
```

---

## ❤️ ИЗБРАННОЕ

### GET /api/favorites

Получить список изббранных товаров.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "product_id": 5,
      "added_at": "2024-01-01T00:00:00Z",
      "product": {
        "id": 5,
        "name": "Товар",
        "price": 100.00,
        "original_price": 120.00,
        "image_url": "https://...",
        "stock": 50,
        "discount_percent": 17
      }
    }
  ]
}
```

---

### POST /api/favorites

Добавить товар в избранное.

**Body:**
```json
{
  "product_id": 5
}
```

**Response:**
```json
{
  "success": true,
  "message": "Товар добавлен в избранное"
}
```

---

### DELETE /api/favorites/:product_id

Удалить товар из избранного.

**Response:**
```json
{
  "success": true,
  "message": "Товар удален из избранного"
}
```

---

### POST /api/favorites/check

Проверить, есть ли товар в избранном.

**Body:**
```json
{
  "product_id": 5
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "is_favorite": true
  }
}
```

---

## ❌ КОДЫ ОШИБОК

### 400 Bad Request
- Невалидные данные запроса
- Отсутствуют обязательные параметры
- Неверный формат данных

### 401 Unauthorized
- Отсутствует заголовок `X-Telegram-Init-Data`

### 403 Forbidden
- Неверные данные авторизации Telegram
- Истекло время действия initData

### 404 Not Found
- Ресурс не найден (товар, категория, заказ и т.д.)

### 500 Internal Server Error
- Ошибка сервера
- Проблема с базой данных

---

## 📝 ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ

### TypeScript (Frontend)

```typescript
import axios from 'axios';

const api = axios.create({
  baseURL: 'https://your-domain.com/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Добавляем Telegram initData к каждому запросу
api.interceptors.request.use((config) => {
  const initDataRaw = window.Telegram.WebApp.initData;
  if (initDataRaw) {
    config.headers['X-Telegram-Init-Data'] = initDataRaw;
  }
  return config;
});

// Получить товары
const products = await api.get('/products', {
  params: {
    category_id: 1,
    limit: 20,
  },
});

// Добавить в корзину
await api.post('/cart', {
  product_id: 5,
  quantity: 2,
});

// Создать заказ
const order = await api.post('/orders', {
  delivery_address: 'г. Ташкент, ул. 1',
  payment_method: 'cash',
});
```

---

## 🔧 НАСТРОЙКА СЕРВЕРА

### 1. Установи переменные окружения

```bash
# .env
TELEGRAM_BOT_TOKEN=your_bot_token_here
FLASK_SECRET_KEY=your_secret_key
ADMIN_NAME=AdminUser
```

### 2. Интегрируй API в app.py

Добавь после создания `telegram_bot`:

```python
from api_mini_app import init_api, api

# Инициализация API
init_api(db, app)

# Регистрация Blueprint
app.register_blueprint(api)
```

### 3. Запусти сервер

```bash
cd web_admin
python app.py
```

---

## ✅ ЧЕКЛИСТ ГОТОВНОСТИ

- [x] Все endpoints реализованы
- [x] Валидация Telegram initData работает
- [x] Обработка ошибок настроена
- [x] Документация полная
- [x] Фронтенд интегрирован
- [ ] Протестировано в production

---

## 🚀 ДЕПЛОЙ

### Vercel (Frontend)

```bash
cd s1-mini-app
vercel --prod
```

### Backend (Heroku/Render/VPS)

```bash
# Установи зависимости
pip install -r requirements.txt

# Запусти
python web_admin/app.py
```

---

**API готово к использованию!** 🎉
