# 🚀 FRONTEND DEPLOYMENT TO RENDER

**Как запустить фронтенд S1 Mini App на Render**

---

## ⚡ БЫСТРЫЙ СТАРТ (5 минут)

### 1. Откройте Render Dashboard

```
https://dashboard.render.com
```

### 2. Создайте Static Site

1. Нажмите **New +** → **Static Site**
2. Connect repository: `Telegram-mini-app`
3. Configure:

```
Name: safar-frontend
Branch: main
Root Directory: s1-mini-app
Build Command: npm install && npm run build
Publish Directory: dist
Region: Frankfurt
Plan: Starter
```

### 3. Добавьте переменную окружения

```env
Key: VITE_API_URL
Value: https://ВАШ_БЭКЕНД.onrender.com/api
```

**Замените URL на ваш backend!**

### 4. Задеплойте!

Нажмите **Create Static Site**

Подождите 3-5 минут ✅

---

## 📊 КОНФИГУРАЦИЯ

### Build Settings:

```yaml
Name: safar-frontend
Type: Static Site
Root Directory: s1-mini-app
Build Command: npm install && npm run build
Publish Directory: dist
Node Version: 18
```

### Environment Variables:

```env
VITE_API_URL = https://safar-backend.onrender.com/api
NODE_VERSION = 18
```

---

## 🔧 ЧТО ПРОИСХОДИТ ПРИ СБОРКЕ

### Build Process:

1. **npm install** - Устанавливает зависимости
   ```
   React, TypeScript, Vite, Tailwind CSS, Zustand
   ```

2. **npm run build** - Создает production сборку
   ```
   Vite компилирует в /dist
   HTML, CSS, JS оптимизированы
   ```

3. **Publish** - Размещает на CDN
   ```
   Статический сайт доступен по URL
   ```

---

## 🎯 ПОСЛЕ ДЕПЛОЯ

### Вы получите URL:

```
https://safar-frontend.onrender.com
```

### Проверьте работу:

1. Откройте URL в браузере
2. Проверьте каталог товаров
3. Добавьте в корзину
4. Проверьте чекаут

### Настройте CORS в Backend:

В Render Dashboard (backend):
```env
CORS_ORIGINS = https://safar-frontend.onrender.com
```

---

## 💡 ALTERNATIVE: Vercel (ПРОЩЕ!)

Vercel лучше для React/Vite приложений!

### Deploy to Vercel:

#### Вариант 1: Через CLI

```bash
cd s1-mini-app
npm install -g vercel
vercel --prod
```

#### Вариант 2: Через GitHub

1. Зайдите на https://vercel.com
2. Import Project → From GitHub
3. Select: `Telegram-mini-app`
4. Framework Preset: Vite
5. Root Directory: `s1-mini-app`
6. Environment Variables:
   ```env
   VITE_API_URL = https://ВАШ_БЭКЕНД.onrender.com/api
   ```
7. Deploy ✅

**Преимущества Vercel:**
- ✅ Автоматический деплой из Git
- ✅ Быстрее чем Render Static Site
- ✅ Лучшая производительность
- ✅ Бесплатно 100GB трафика

---

## 🐛 TROUBLESHOOTING

### Build Failed

**Error: Node version incompatible**

**Fix:**
```env
NODE_VERSION = 18
```

**Error: npm install failed**

**Fix:**
```bash
cd s1-mini-app
rm -rf node_modules package-lock.json
npm install
git add package-lock.json
git commit -m "Update lock file"
git push
```

### Blank Page

**Причина:** Неверный VITE_API_URL

**Fix:**
1. Проверьте переменную в Dashboard
2. Убедитесь что backend доступен
3. Проверьте консоль браузера (F12)

### CORS Errors

**Причина:** Backend не разрешает frontend

**Fix:**
```env
# В backend dashboard
CORS_ORIGINS = https://safar-frontend.onrender.com
```

---

## ✅ ЧЕКЛИСТ

- [ ] Backend работает на Render
- [ ] Frontend задепложен как Static Site
- [ ] VITE_API_URL установлен
- [ ] CORS настроен в backend
- [ ] Страница открывается
- [ ] Товары загружаются
- [ ] Корзина работает
- [ ] Нет ошибок в консоли

---

## 💰 СТОИМОСТЬ

**Render Static Site:**
- Free tier: 100GB bandwidth/month
- **Cost: $0/month**

**Vercel:**
- Free tier: 100GB bandwidth/month
- **Cost: $0/month**

---

## 📊 АРХИТЕКТУРА

```
┌─────────────────────┐
│   Frontend (React)  │
│   safar-frontend    │
│   .onrender.com     │
│   or .vercel.app    │
└──────────┬──────────┘
           │ HTTP/REST API
           ↓
┌─────────────────────┐
│   Backend (Flask)   │
│   safar-backend     │
│   .onrender.com     │
│   :10000            │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│   SQLite Database   │
│   /data/shop_bot.db │
└─────────────────────┘
```

---

## 🎯 TELEGRAM INTEGRATION

### Настройте Menu Button:

1. Откройте @BotFather
2. `/mybots` → Ваш бот
3. Bot Settings → Menu Button
4. Set URL: `https://safar-frontend.onrender.com`
5. Title: "Open Shop"

Теперь кнопка будет открывать приложение! ✅

---

## 📞 SUPPORT FILES

**Use these files:**
- ✅ This file - Frontend deployment guide
- ✅ `RENDER_WORKING_CONFIG.md` - Backend config
- ✅ `QUICK_START_RENDER.md` - Quick start

**Don't use:**
- ❌ render-frontend.yaml (Blueprint doesn't support static)
- ❌ render-complete.yaml (has errors)

---

**READY TO DEPLOY!** 🚀

Last Updated: March 27, 2026  
Deployment Time: ~5 minutes  
Difficulty: Easy
