# 📡 ВСЕ API ENDPOINTS - ПОЛНЫЙ СПИСОК

## 🔐 АВТОРИЗАЦИЯ

Все endpoints требуют заголовок:
```
X-Telegram-Init-Data: <initData из Telegram WebApp>
```

---

## 📁 1. КАТЕГОРИИ (2 endpoints)

### GET /api/categories
**Описание:** Получить список всех активных категорий

**Пример запроса:**
```typescript
GET /api/categories
Headers: { "X-Telegram-Init-Data": "user=..." }
```

**Ответ:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Электроника",
      "emoji": "📱",
      "image_url": "https://example.com/image.jpg",
      "is_active": true,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

---

### GET /api/categories/:id
**Описание:** Получить категорию по ID

**Пример:**
```typescript
GET /api/categories/1
```

**Ответ:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Электроника",
    "emoji": "📱",
    "image_url": "https://example.com/image.jpg",
    "is_active": true
  }
}
```

---

## 🛍️ 2. ТОВАРЫ (6 endpoints)

### GET /api/products
**Описание:** Получить товары с фильтрацией и пагинацией

**Query параметры:**
- `category_id` (integer) - фильтр по категории
- `subcategory_id` (integer) - фильтр по подкатегории
- `search` (string) - поиск по названию/описанию/бренду
- `min_price` (float) - минимальная цена
- `max_price` (float) - максимальная цена
- `limit` (integer, default: 50) - количество товаров
- `offset` (integer, default: 0) - смещение

**Пример:**
```typescript
GET /api/products?category_id=1&limit=20&offset=0
```

**Ответ:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "iPhone 15 Pro",
      "description": "Флагманский смартфон Apple",
      "price": 1200.00,
      "cost_price": 900.00,
      "original_price": 1400.00,
      "category_id": 1,
      "subcategory_id": 10,
      "brand": "Apple",
      "image_url": "https://example.com/iphone.jpg",
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
**Описание:** Получить товар по ID

**Пример:**
```typescript
GET /api/products/1
```

**Ответ:**
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
**Описание:** Поиск товаров

**Query параметры:**
- `q` (string, required) - поисковый запрос (минимум 2 символа)

**Пример:**
```typescript
GET /api/products/search?q=iPhone
```

**Ответ:** Аналогично `GET /api/products`

---

### POST /api/products/:id/views
**Описание:** Увеличить счетчик просмотров товара

**Пример:**
```typescript
POST /api/products/1/views
```

**Ответ:**
```json
{
  "success": true,
  "message": "Просмотры обновлены"
}
```

---

### GET /api/products/:id/related
**Описание:** Получить похожие товары из той же категории

**Query параметры:**
- `limit` (integer, default: 4) - количество товаров

**Пример:**
```typescript
GET /api/products/1/related?limit=4
```

**Ответ:**
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

## 🛒 3. КОРЗИНА (5 endpoints)

### GET /api/cart
**Описание:** Получить корзину пользователя

**Ответ:**
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
**Описание:** Добавить товар в корзину

**Body:**
```json
{
  "product_id": 5,
  "quantity": 2
}
```

**Ответ:**
```json
{
  "success": true,
  "message": "Товар добавлен в корзину"
}
```

---

### PATCH /api/cart/:item_id
**Описание:** Обновить количество товара в корзине

**Body:**
```json
{
  "quantity": 3
}
```

**Если quantity <= 0**, товар удаляется из корзины.

**Ответ:**
```json
{
  "success": true,
  "message": "Количество обновлено"
}
```

---

### DELETE /api/cart/:item_id
**Описание:** Удалить товар из корзины

**Ответ:**
```json
{
  "success": true,
  "message": "Товар удален из корзины"
}
```

---

### POST /api/cart/clear
**Описание:** Очистить всю корзину

**Ответ:**
```json
{
  "success": true,
  "message": "Корзина очищена"
}
```

---

## 📦 4. ЗАКАЗЫ (4 endpoints)

### POST /api/orders
**Описание:** Создать новый заказ

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

**Ответ:**
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
**Описание:** Получить все заказы пользователя

**Ответ:**
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
**Описание:** Получить заказ по ID

**Пример:**
```typescript
GET /api/orders/123
```

**Ответ:** Аналогично `GET /api/orders` с деталями одного заказа.

---

### POST /api/orders/:id/cancel
**Описание:** Отменить заказ (можно если статус `pending` или `confirmed`)

**Пример:**
```typescript
POST /api/orders/123/cancel
```

**Ответ:**
```json
{
  "success": true,
  "message": "Заказ отменен"
}
```

---

## ❤️ 5. ИЗБРАННОЕ (4 endpoints)

### GET /api/favorites
**Описание:** Получить список избранных товаров

**Ответ:**
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
**Описание:** Добавить товар в избранное

**Body:**
```json
{
  "product_id": 5
}
```

**Ответ:**
```json
{
  "success": true,
  "message": "Товар добавлен в избранное"
}
```

---

### DELETE /api/favorites/:product_id
**Описание:** Удалить товар из избранного

**Пример:**
```typescript
DELETE /api/favorites/5
```

**Ответ:**
```json
{
  "success": true,
  "message": "Товар удален из избранного"
}
```

---

### POST /api/favorites/check
**Описание:** Проверить, есть ли товар в избранном

**Body:**
```json
{
  "product_id": 5
}
```

**Ответ:**
```json
{
  "success": true,
  "data": {
    "is_favorite": true
  }
}
```

---

## 📊 ИТОГОВАЯ СТАТИСТИКА

| Категория | Endpoints | Методы |
|-----------|-----------|--------|
| **Категории** | 2 | GET |
| **Товары** | 6 | GET, POST |
| **Корзина** | 5 | GET, POST, PATCH, DELETE |
| **Заказы** | 4 | GET, POST |
| **Избранное** | 4 | GET, POST, DELETE |
| **ВСЕГО** | **21** | **Различные** |

---

## 🔧 ПРИМЕР ИСПОЛЬЗОВАНИЯ НА FRONTEND

```typescript
// services/api.ts
import axios from 'axios';
import { useRawInitData } from '@tma.js/sdk-react';

const api = axios.create({
  baseURL: 'http://localhost:5000/api',
});

// Автоматически добавляем Telegram initData
api.interceptors.request.use((config) => {
  const initDataRaw = window.Telegram.WebApp.initData;
  if (initDataRaw) {
    config.headers['X-Telegram-Init-Data'] = initDataRaw;
  }
  return config;
});

// Категории
export const getCategories = () => api.get('/categories');

// Товары
export const getProducts = (params) => api.get('/products', { params });
export const getProductById = (id) => api.get(`/products/${id}`);

// Корзина
export const getCart = () => api.get('/cart');
export const addToCart = (productId, quantity) => 
  api.post('/cart', { product_id: productId, quantity });
export const updateCartItem = (itemId, quantity) => 
  api.patch(`/cart/${itemId}`, { quantity });
export const removeFromCart = (itemId) => 
  api.delete(`/cart/${itemId}`);

// Заказы
export const createOrder = (data) => api.post('/orders', data);
export const getUserOrders = () => api.get('/orders');

// Избранное
export const getFavorites = () => api.get('/favorites');
export const addToFavorites = (productId) => 
  api.post('/favorites', { product_id: productId });
export const removeFromFavorites = (productId) => 
  api.delete(`/favorites/${productId}`);
```

---

## 🎯 ГОТОВО К ИСПОЛЬЗОВАНИЮ!

Все 21 endpoints реализованы, протестированы и готовы к работе! 🚀
