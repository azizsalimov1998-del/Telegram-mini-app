# ⚡ QUICK DEPLOYMENT CHECKLIST

**Fast-track guide to deploy S1 Mini App to Render + Vercel**

---

## 📋 PRE-DEPLOYMENT (5 minutes)

### 1. Get Required Credentials
- [ ] Telegram Bot Token (from @BotFather)
- [ ] Your Telegram ID (from @userinfobot)
- [ ] Render account (https://render.com)
- [ ] Vercel account (https://vercel.com)

### 2. Generate Secret Key
```bash
cd /home/duck/Документы/Safar-main
python3 generate_secret_key.py
```
- [ ] Copy the generated secret key

### 3. Push to GitHub
```bash
cd /home/duck/Документы/Safar-main
git add .
git commit -m "Production ready"
git push origin main
```

---

## 🚀 BACKEND DEPLOYMENT (15 minutes)

### Option A: Quick Deploy via Render Dashboard

1. **Go to https://dashboard.render.com**
2. Click **New +** → **Web Service**
3. Connect repository: `Safar`
4. Configure:
   ```
   Name: safar-backend
   Region: Frankfurt
   Branch: main
   Root Directory: (leave blank)
   ```

5. **Build Settings:**
   ```
   Build Command: pip install -r web_admin/requirements.txt
   Start Command: ./start.sh
   ```

6. **Instance Type:** Starter (Free tier)

7. **Add Environment Variables:**
   ```
   TELEGRAM_BOT_TOKEN=your_token_here
   ADMIN_TELEGRAM_ID=your_id_here
   FLASK_SECRET_KEY=paste_generated_key
   DISABLE_MINI_APP_AUTH=false
   ENVIRONMENT=production
   CORS_ORIGINS=*
   DB_FILENAME=shop_bot.db
   ```

8. Click **Create Web Service**
9. Wait for deployment (~3-5 minutes)
10. Copy your URL: `https://safar-backend.onrender.com`

### Test Backend
```bash
curl https://safar-backend.onrender.com/api/categories
```
Should return JSON with categories ✅

---

## 🌐 FRONTEND DEPLOYMENT (10 minutes)

### Deploy to Vercel

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Deploy:**
   ```bash
   cd /home/duck/Документы/Safar-main/s1-mini-app
   vercel --prod
   ```

3. **Or use Web Interface:**
   - Go to https://vercel.com/new
   - Import `Safar` repository
   - Framework: Vite (auto-detected)
   - Build Command: `npm run build`
   - Output Directory: `dist`

4. **Set Environment Variable:**
   ```
   VITE_API_URL=https://safar-backend.onrender.com/api
   ```

5. Deploy! (~2-3 minutes)
6. Copy your URL: `https://safar.vercel.app`

---

## ⚙️ POST-DEPLOYMENT (5 minutes)

### 1. Update CORS in Backend
- Go to Render Dashboard
- Add environment variable:
  ```
  CORS_ORIGINS=https://safar.vercel.app
  ```
- Save (auto-redeploys)

### 2. Test Full Integration
```bash
# Open in browser
https://safar.vercel.app
```

Checklist:
- [ ] Page loads
- [ ] Products display
- [ ] Can add to cart
- [ ] No console errors

### 3. Configure Telegram Bot
1. Open @BotFather
2. `/mybots` → Select your bot
3. Bot Settings → Menu Button
4. Set URL: `https://safar.vercel.app`
5. Title: "Open Shop"

### 4. Test in Telegram
1. Open your bot
2. Click Menu button
3. Browse products
4. Add to cart
5. Complete purchase

---

## 🎯 SUCCESS CRITERIA

✅ Backend live at: `https://safar-backend.onrender.com`  
✅ Frontend live at: `https://safar.vercel.app`  
✅ API responds correctly  
✅ No CORS errors  
✅ Can complete purchase  
✅ Works in Telegram  

---

## 🐛 QUICK FIXES

### Backend won't deploy
- Check logs in Render Dashboard
- Verify requirements.txt exists
- Ensure start.sh is executable: `chmod +x start.sh`

### Frontend build fails
- Clear cache: `rm -rf node_modules package-lock.json`
- Reinstall: `npm install`
- Try again: `vercel --prod`

### CORS errors
- Update `CORS_ORIGINS` in Render
- Include your Vercel URL
- Wait for redeploy (~1 minute)

### Database not found
- Check disk is mounted at `/data`
- Verify `DB_FILENAME=shop_bot.db`
- Database auto-initializes on first run

---

## 📞 DETAILED GUIDES

For more information, see:
- [DEPLOY_RENDER_GUIDE.md](./DEPLOY_RENDER_GUIDE.md) - Complete deployment guide
- [INTEGRATION_TESTING_GUIDE.md](./INTEGRATION_TESTING_GUIDE.md) - Testing instructions
- [FINAL_STATUS.md](./FINAL_STATUS.md) - Project status

---

## ⏱️ TIME ESTIMATE

| Step | Time |
|------|------|
| Pre-deployment | 5 min |
| Backend deploy | 15 min |
| Frontend deploy | 10 min |
| Post-deployment | 5 min |
| **TOTAL** | **~35 minutes** |

---

## 💰 COST

- **Render:** Free tier (750 hours/month)
- **Vercel:** Free (Hobby plan)
- **Total:** $0/month for development

---

**Ready to deploy!** 🚀

Last Updated: March 26, 2026
