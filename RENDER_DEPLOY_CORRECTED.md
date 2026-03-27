# ✅ RENDER DEPLOYMENT - CORRECTED GUIDE

**Issue:** Render Blueprint doesn't support `type: static`  
**Solution:** Deploy frontend separately through dashboard

---

## ❌ ПРОБЛЕМА

Render Blueprint **НЕ поддерживает** тип `static` в YAML файле.

**Ошибка:**
```
unknown type "static"
```

**Причина:**
- Blueprint работает только с `type: web`, `type: pserv`, `type: worker`
- Static Sites нужно создавать через Dashboard вручную

---

## ✅ ПРАВИЛЬНОЕ РЕШЕНИЕ

### Шаг 1: Backend через Blueprint

Используйте файл `render-backend-only.yaml`:

1. Откройте https://dashboard.render.com
2. New + → **Blueprint**
3. Connect repository: `Telegram-mini-app`
4. Выберите файл: **render-backend-only.yaml**
5. Нажмите **Apply**

**Backend задеплоится автоматически!** ✅

---

### Шаг 2: Frontend через Dashboard (вручную)

Static Site нельзя создать через Blueprint, нужно вручную:

1. Откройте https://dashboard.render.com
2. New + → **Static Site**
3. Connect repository: `Telegram-mini-app`
4. Configure settings:

```
Name: safar-frontend
Branch: main
Root Directory: s1-mini-app
Build Command: npm install && npm run build
Publish Directory: dist
Region: Frankfurt
Plan: Starter
```

5. Add Environment Variable:
```
Key: VITE_API_URL
Value: https://safar-backend.onrender.com/api
```

6. Click **Create Static Site**

**Frontend задеплоится!** ✅

---

## 📊 ИТОГОВАЯ КОНФИГУРАЦИЯ

### Backend (Blueprint):
- File: `render-backend-only.yaml`
- Type: Web Service (Python/Flask)
- Auto-deploy: Yes

### Frontend (Manual):
- Created via Dashboard
- Type: Static Site
- Build: npm install && npm run build
- Publish: dist

---

## 🔧 ПОЧЕМУ ТАК?

### Blueprint ограничения:

**Поддерживает:**
- ✅ `type: web` - Web services
- ✅ `type: pserv` - Private services
- ✅ `type: worker` - Background workers
- ✅ `type: redis` - Redis instances

**Не поддерживает:**
- ❌ `type: static` - Static sites
- ❌ `type: cronJob` - Cron jobs

### Решение:
Static Sites создаются только через Dashboard вручную.

---

## 💰 ALTERNATIVE: Vercel для Frontend

Вместо Render Static Site, можно использовать Vercel (проще!):

### Deploy to Vercel:

```bash
cd s1-mini-app
npm install -g vercel
vercel --prod
```

**Преимущества:**
- ✅ Автоматический деплой из GitHub
- ✅ Не нужен Blueprint
- ✅ Быстрее и проще
- ✅ Бесплатно 100GB трафика

---

## ⚙️ ENVIRONMENT VARIABLES

### Backend (в Blueprint):
```env
TELEGRAM_BOT_TOKEN=your_token
ADMIN_TELEGRAM_ID=your_id
FLASK_SECRET_KEY=secure_key
CORS_ORIGINS=*  # или URL фронтенда после деплоя
```

### Frontend (в Dashboard):
```env
VITE_API_URL=https://ВАШ_БЭКЕНД.onrender.com/api
```

---

## 🎯 ПОШАГОВЫЙ ДЕПЛОЙ

### 1. Backend (Blueprint) - 5 минут

```bash
# Файл уже в GitHub
render-backend-only.yaml
```

1. Dashboard.render.com
2. New + → Blueprint
3. Connect repo
4. Select file
5. Apply ✅

### 2. Frontend (Manual) - 5 минут

1. Dashboard.render.com
2. New + → Static Site
3. Connect repo
4. Settings:
   - Root: s1-mini-app
   - Build: npm install && npm run build
   - Publish: dist
5. Add env var: VITE_API_URL
6. Create ✅

### 3. Update CORS - 1 минута

В Backend Dashboard:
```
CORS_ORIGINS = https://safar-frontend.onrender.com
```

---

## ✅ ЧЕКЛИСТ

- [x] render-backend-only.yaml создан
- [ ] Backend задепложен через Blueprint
- [ ] Frontend создан через Dashboard
- [ ] VITE_API_URL установлен
- [ ] CORS настроен
- [ ] Оба сервиса работают

---

## 🐛 TROUBLESHOOTING

### "Blueprint failed"
- Проверьте логи
- Убедитесь что render-backend-only.yaml валидный
- Проверьте requirements.txt

### "Static Site build failed"
- Check Node version: add `NODE_VERSION=18`
- Verify package.json exists
- Check build logs

### "CORS error after deploy"
- Update CORS_ORIGINS in backend
- Use exact frontend URL
- Redeploy backend

---

## 📞 SUPPORT FILES

**Use these files:**
- ✅ `render-backend-only.yaml` - For Blueprint (backend only)
- ❌ ~~`render-complete.yaml`~~ - Don't use (has errors)
- ❌ ~~`render-frontend.yaml`~~ - Don't use (invalid type)

**Documentation:**
- This file - Deployment guide
- `DEPLOY_READY.md` - General readiness check

---

**Ready to deploy!** 🚀

Last Updated: March 26, 2026  
Status: ✅ Corrected for Render limitations
