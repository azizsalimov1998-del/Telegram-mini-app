# ⚡ ЗАПУСК ФРОНТЕНДА - БЫСТРАЯ ИНСТРУКЦИЯ

**Время:** 5 минут  
**Сложность:** Легко

---

## 🎯 3 ШАГА

### 1️⃣ Откройте Render Dashboard

```
https://dashboard.render.com
```

### 2️⃣ Создайте Static Site

```
New + → Static Site
→ Connect repository: Telegram-mini-app
→ Root Directory: s1-mini-app
→ Build Command: npm install && npm run build
→ Publish Directory: dist
```

### 3️⃣ Добавьте переменную

```env
VITE_API_URL = https://ВАШ_БЭКЕНД.onrender.com/api
```

**Нажмите Create Static Site** ✅

---

## ✅ ГОТОВО!

Через 3-5 минут получите URL:
```
https://safar-frontend.onrender.com
```

---

## 🔧 CORS

В backend dashboard добавьте:
```env
CORS_ORIGINS = https://safar-frontend.onrender.com
```

---

## 📱 TELEGRAM

@BotFather → My Bots → Bot Settings → Menu Button
```
URL: https://safar-frontend.onrender.com
Title: Open Shop
```

---

## 💡 ALTERNATIVE: Vercel

Проще через Vercel:

```bash
cd s1-mini-app
npm install -g vercel
vercel --prod
```

Или через GitHub на https://vercel.com

---

**DEPLOY NOW!** 🚀
