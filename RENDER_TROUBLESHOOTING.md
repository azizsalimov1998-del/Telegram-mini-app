# 🔧 RENDER DEPLOYMENT TROUBLESHOOTING

**Проблема:** Локально работает, на Render НЕ работает  
**Дата:** 27 Марта 2026

---

## 🐛 ВОЗМОЖНЫЕ ПРИЧИНЫ

### 1. Переменные окружения не установлены

**Проверьте в Render Dashboard:**

```env
VITE_API_URL = https://safar-backend.onrender.com/api
NODE_VERSION = 18
```

**Где установить:**
- Static Site → Environment → Add Variable

---

### 2. CORS не настроен на бекенде

**Симптомы:**
- Фронтенд загружается
- Товары НЕ загружаются
- Ошибка CORS в консоли

**Решение:**

В Backend Dashboard (Render):
```env
CORS_ORIGINS = https://safar-frontend.onrender.com
# ИЛИ для разработки:
CORS_ORIGINS = *
```

---

### 3. API недоступен

**Проверьте backend:**

```bash
curl https://safar-backend.onrender.com/api/categories
```

**Ожидается:** JSON с категориями  
**Если ошибка 401:** Нормально (требуется Telegram авторизация)  
**Если ошибка 500/404:** Бекенд не работает

---

### 4. Build проходит успешно, но пустая страница

**Причины:**
- Неверный VITE_API_URL
- JavaScript ошибки в консоли
- Проблемы с роутингом

**Решение:**

Откройте консоль браузера (F12):
```
Console → Проверить ошибки
Network → Проверить API запросы
```

---

## ✅ ПОШАГОВАЯ ПРОВЕРКА

### Шаг 1: Проверьте Static Site на Render

1. Откройте https://dashboard.render.com
2. Найдите **safar-frontend**
3. Проверьте статус: ✅ Available
4. Скопируйте URL: `https://...onrender.com`

---

### Шаг 2: Проверьте переменные окружения

В Dashboard фронтенда:
```
Environment → Variables
```

**Должно быть:**
```
VITE_API_URL = https://safar-backend.onrender.com/api
NODE_VERSION = 18
```

**Если нет:** Добавьте и сделайте Redeploy

---

### Шаг 3: Проверьте логи сборки

В Dashboard фронтенда:
```
Logs → View Build Logs
```

**Ожидается:**
```
npm install
npm run build
> tsc && vite build
✓ compiled in X.Xs
✓ built in X.Xs
Deployment complete!
```

**Если ошибка:** Читаем ошибку и исправляем

---

### Шаг 4: Откройте сайт

Перейдите на:
```
https://ВАШ_ФРОНТЕНД.onrender.com
```

**Проверьте:**
- [ ] Страница загружается
- [ ] Нет белого экрана
- [ ] Видны элементы интерфейса

---

### Шаг 5: Откройте консоль разработчика

Нажмите **F12** → Console

**Ошибки:**
- ❌ Красные ошибки JavaScript
- ❌ Ошибки загрузки ресурсов
- ❌ CORS errors

**Нормально:**
- ✅ Нет красных ошибок
- ✅ Предупреждения допустимы

---

### Шаг 6: Проверьте Network

F12 → Network tab

**Обновите страницу**

**Проверьте запросы:**
```
GET /api/categories
GET /api/products
```

**Статус:**
- ✅ 200 OK - работает
- ⚠️ 401 Unauthorized - нормально (нужен Telegram)
- ❌ 404 Not Found - API неверный
- ❌ 500 Internal Server Error - бекенд упал

**CORS ошибка:**
```
Access to fetch blocked by CORS policy
```

**Решение:** Настроить CORS в бекенде

---

### Шаг 7: Проверьте бекенд

```bash
curl https://safar-backend.onrender.com/api/categories
```

**Ответ:**
```json
{
  "data": [
    {"id": 1, "name": "Electronics", ...},
    ...
  ]
}
```

**Если тишина:** Бекенд не доступен

---

## 🔧 ИСПРАВЛЕНИЯ

### Проблема 1: CORS Error

**Симптомы:**
```
Access to XMLHttpRequest blocked by CORS policy
```

**Решение:**

В Backend Dashboard:
```env
CORS_ORIGINS = *
```

Или конкретный URL:
```env
CORS_ORIGINS = https://safar-frontend.onrender.com
```

**Перезапустите бекенд!**

---

### Проблема 2: VITE_API_URL не установлен

**Симптомы:**
- Запросы идут на localhost:5000
- Сеть показывает ошибки подключения

**Решение:**

1. Frontend Dashboard → Environment
2. Add Variable:
   ```
   Key: VITE_API_URL
   Value: https://safar-backend.onrender.com/api
   ```
3. Manual Deploy

---

### Проблема 3: Бекенд требует авторизацию

**Симптомы:**
- Все запросы возвращают 401
- Консоль: "Unauthorized"

**Решение (для разработки):**

В Backend Dashboard:
```env
DISABLE_MINI_APP_AUTH = true
```

⚠️ **В продакшене оставьте false!**

---

### Проблема 4: Белый экран

**Симптомы:**
- Страница белая
- Консоль пустая или ошибки JS

**Причины:**
1. JavaScript ошибка в коде
2. Не загрузился bundle
3. Проблемы с роутингом

**Диагностика:**

F12 → Console → Смотрим ошибки

**Частые ошибки:**
```
Cannot find module '../lib/telegram'
```
**Решение:** Убедитесь что telegram.ts запушен

```
process is not defined
```
**Решение:** Проблема с Vite конфигом

---

## 💡 КАК ДЕБАГИТЬ

### 1. Логи сборки

```
Dashboard → Logs → Build Logs
```

Ищем:
- ✅ "built in X.Xs"
- ❌ "error TS2307"
- ❌ "Build failed"

---

### 2. Логи сервиса

```
Dashboard → Logs → Service Logs
```

Ищем:
- Ошибки runtime
- Проблемы подключения
- CORS messages

---

### 3. Browser DevTools

**Console:**
- JavaScript ошибки
- Предупреждения React

**Network:**
- Статус запросов
- Тела запросов/ответов
- Timing

**Application:**
- LocalStorage
- Session Storage
- Cookies

---

## 📊 ЧЕКЛИСТ ПРОВЕРКИ

- [ ] Frontend задепложен на Render
- [ ] VITE_API_URL установлен
- [ ] NODE_VERSION = 18
- [ ] Сборка прошла без ошибок
- [ ] Backend доступен
- [ ] CORS настроен
- [ ] Нет ошибок в консоли
- [ ] API возвращает данные

---

## 🎯 БЫСТРЫЙ ФИКС

### Если ничего не помогает:

**1. Пересоздайте Static Site:**

```
Dashboard → Delete Service
New + → Static Site
Configure заново
```

**2. Используйте Vercel (проще!):**

```bash
cd s1-mini-app
npm install -g vercel
vercel --prod
```

**3. Проверьте локально:**

```bash
cd s1-mini-app
npm run build
npm run preview
```

Если локально работает → проблема в Render  
Если локально НЕ работает → проблема в коде

---

## 🆘 ЧАСТЫЕ ОШИБКИ

### "Cannot GET /"

**Причина:** Проблемы с роутингом  
**Решение:** Добавить _redirects файл

### "Failed to compile"

**Причина:** TypeScript ошибки  
**Решение:** Проверить логи сборки

### "Network Error"

**Причина:** API недоступен  
**Решение:** Проверить backend

---

**READY TO DEBUG!** 🔍

Last Updated: March 27, 2026  
Status: Debugging Mode
