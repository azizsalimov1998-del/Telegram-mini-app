# 🚀 QUICK START - S1 Mini App

**Get up and running in 5 minutes!**

---

## ⚡ FASTEST PATH TO RUNNING APP

### 1. Start Backend (Terminal 1)

```bash
# Navigate to backend
cd /home/duck/Документы/Safar-main/web_admin

# Install dependencies (if needed)
pip3 install -r requirements.txt

# Create .env file
cat > .env << EOF
TELEGRAM_BOT_TOKEN=your_token_here
ADMIN_NAME=admin
ADMIN_PASSWORD=admin
FLASK_SECRET_KEY=dev-secret-key
DISABLE_MINI_APP_AUTH=True
EOF

# Start server
python3 run.py
```

**Expected output:**
```
✅ CORS настроено для API
✅ Telegram Mini App API успешно подключено!
🔧 DISABLE_AUTH_FOR_DEV=True
 * Running on http://localhost:5000
```

### 2. Start Frontend (Terminal 2)

```bash
# Navigate to frontend
cd /home/duck/Документы/Safar-main/s1-mini-app

# Install dependencies
npm install

# Create .env file
echo "VITE_API_URL=http://localhost:5000/api" > .env

# Start dev server
npm run dev
```

**Expected output:**
```
VITE v6.1.0  ready in 500 ms
➜  Local:   http://localhost:5173/
```

### 3. Open in Browser

```
http://localhost:5173
```

**You should see:** S1 Shop catalog with products!

---

## ✅ VERIFICATION CHECKLIST

### Backend Working?
```bash
curl http://localhost:5000/api/categories
```
Should return JSON with categories

### Frontend Working?
- [ ] Page loads at http://localhost:5173
- [ ] Categories display
- [ ] Products display
- [ ] No console errors
- [ ] Can add to cart

---

## 🐛 TROUBLESHOOTING

### Backend won't start
```bash
# Check Python version (need 3.8+)
python3 --version

# Install missing packages
pip3 install flask flask-cors requests

# Check if port 5000 is free
lsof -i :5000
kill -9 <PID>
```

### Frontend won't start
```bash
# Clear and reinstall
rm -rf node_modules package-lock.json
npm install

# Check Node version (need 18+)
node --version
```

### API not connecting
1. Check backend is running on port 5000
2. Verify `.env` has correct URL
3. Restart frontend dev server
4. Check browser console for errors

---

## 📚 DOCUMENTATION INDEX

### For Quick Reference:
1. **[INTEGRATION_TESTING_GUIDE.md](./INTEGRATION_TESTING_GUIDE.md)** - Complete testing guide
2. **[FINAL_STATUS.md](./FINAL_STATUS.md)** - Project status
3. **[CONTEXT.md](./CONTEXT.md)** - Project context

### For Development:
1. **[README.md](./README.md)** - General overview
2. **[DEPLOY.md](./DEPLOY.md)** - Deployment instructions
3. **[PHASE_*.md](./PHASE_0_1_COMPLETE.md)** - Phase reports

### For Production:
1. **[FINAL_STATUS.md](./FINAL_STATUS.md)** - Readiness status
2. **[DEPLOY_GUIDE.md](./DEPLOY_GUIDE.md)** - Deploy instructions
3. **[INTEGRATION_TESTING_GUIDE.md](./INTEGRATION_TESTING_GUIDE.md)** - Testing guide

---

## 🎯 NEXT STEPS AFTER LOCAL TESTING

### 1. Deploy Frontend
```bash
npm install -g vercel
vercel --prod
```

### 2. Deploy Backend
- Use Render, Railway, or VPS
- Set environment variables
- Update CORS allowed origins

### 3. Configure Telegram Bot
- Get token from @BotFather
- Set Menu Button URL
- Test in Telegram app

---

## 📞 NEED HELP?

**Check these docs:**
- Integration issues → [INTEGRATION_TESTING_GUIDE.md](./INTEGRATION_TESTING_GUIDE.md)
- Build issues → [VERIFICATION_FIX_REPORT.md](./VERIFICATION_FIX_REPORT.md)
- General info → [CONTEXT.md](./CONTEXT.md)

**Common Issues:**
- Port conflicts → Change port in `run.py` or use different port
- Missing dependencies → Run `npm install` or `pip3 install -r requirements.txt`
- TypeScript errors → Run `npx tsc --noEmit` to check
- API errors → Check backend logs

---

**Last Updated:** March 26, 2026  
**Status:** ✅ Ready for Development
