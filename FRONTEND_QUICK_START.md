# ⚡ БЫСТРЫЙ ЗАПУСК ФРОНТЕНДА НА RENDER

**Время:** 10 минут | **Сложность:** Средняя

---

## 🎯 КРАТКАЯ ИНСТРУКЦИЯ

### 1️⃣ Откройте Render
```
https://dashboard.render.com
```

### 2️⃣ Создайте Static Site
- New + → Static Site
- Repository: `Telegram-mini-app`
- Branch: `main`

### 3️⃣ Настройте
```
Name: safar-frontend
Root Directory: s1-mini-app
Build Command: npm install && npm run build
Publish Directory: dist
```

### 4️⃣ Добавьте переменную
```
VITE_API_URL = https://ВАШ_БЭКЕНД.onrender.com/api
```

### 5️⃣ Deploy!
- Нажмите "Create Static Site"
- Подождите 3-5 минут
- Готово! ✅

---

## 🔗 URL ПОСЛЕ ДЕПЛОЯ

```
Frontend: https://safar-frontend.onrender.com
Backend:  https://ВАШ_БЭКЕНД.onrender.com
```

---

## ⚙️ НАСТРОЙКА CORS

В бэкенде (Render Dashboard):
```
CORS_ORIGINS = https://safar-frontend.onrender.com
```

---

## 📱 TELEGRAM BOT

@BotFather → My Bots → Bot Settings → Menu Button
```
URL: https://safar-frontend.onrender.com
Title: Open Shop
```

---

## ✅ ПРОВЕРКА

- [ ] Страница открывается
- [ ] Товары загружаются
- [ ] Корзина работает
- [ ] Нет ошибок CORS
- [ ] В Telegram работает

---

## 💰 СТОИМОСТЬ

**$0/месяц** (бесплатный план)

---

## 🆘 ЕСЛИ ЧТО-ТО НЕ ТАК

1. Проверьте логи в Render
2. Проверьте VITE_API_URL
3. Проверьте CORS в бэкенде
4. Посмотрите полную инструкцию: `RUN_FRONTEND_RENDER_RU.md`

---

**ПОЕХАЛИ!** 🚀
