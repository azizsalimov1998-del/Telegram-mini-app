# 🚀 DEPLOY FRONTEND TO RENDER

**Quick guide to deploy S1 Mini App frontend to Render**

---

## ⚡ QUICK STEPS (10 minutes)

### 1. Push Changes to GitHub

```bash
cd /home/duck/Документы/Safar-main
git add render-frontend.yaml
git commit -m "Add Render frontend configuration"
git push origin main
```

### 2. Deploy on Render

#### Option A: Using Render Dashboard (Recommended)

1. **Go to https://dashboard.render.com**
2. Click **New +** → **Static Site**
3. Connect your repository: `Telegram-mini-app`
4. Configure:
   ```
   Name: safar-frontend
   Branch: main
   Root Directory: s1-mini-app
   Build Command: npm install && npm run build
   Publish Directory: dist
   ```

5. **Set Environment Variable:**
   ```
   VITE_API_URL = https://safar-backend.onrender.com/api
   ```

6. Click **Create Static Site**
7. Wait for deployment (~3-5 minutes)
8. Copy your URL: `https://safar-frontend.onrender.com`

#### Option B: Using Blueprint (render-frontend.yaml)

1. Go to https://dashboard.render.com
2. New + → **Blueprint**
3. Connect repository
4. Select `render-frontend.yaml`
5. Click **Apply**
6. Set environment variable in dashboard

---

## 🔧 CONFIGURATION DETAILS

### Build Settings:

```yaml
Name: safar-frontend
Type: Static Site
Region: Frankfurt
Branch: main
Root Directory: s1-mini-app
Build Command: npm install && npm run build
Publish Directory: dist
```

### Environment Variables:

```env
VITE_API_URL=https://safar-backend.onrender.com/api
NODE_VERSION=18
```

### Headers (Security):
```
Cache-Control: no-cache
X-Frame-Options: SAMEORIGIN
Content-Security-Policy: default-src 'self' ...
```

---

## ✅ AFTER DEPLOYMENT

### 1. Update Backend CORS

In Render Dashboard (backend):
```
CORS_ORIGINS=https://safar-frontend.onrender.com
```

### 2. Test Frontend

Open: `https://safar-frontend.onrender.com`

Checklist:
- [ ] Page loads
- [ ] Products display
- [ ] Can add to cart
- [ ] No console errors
- [ ] API calls work

### 3. Configure Telegram Bot

1. Open @BotFather
2. `/mybots` → Select your bot
3. Bot Settings → Menu Button
4. Set URL: `https://safar-frontend.onrender.com`
5. Title: "Open Shop"

---

## 🐛 TROUBLESHOOTING

### Build Fails

**Error: Node version**
```bash
# Add to render-frontend.yaml
envVars:
  - key: NODE_VERSION
    value: 18
```

**Error: npm install fails**
- Check package.json is valid
- Ensure Node 18+ compatibility

### Blank Page After Deploy

**Check:**
- Browser console for errors
- VITE_API_URL is set correctly
- Backend is running and accessible

### CORS Errors

**Fix:**
1. Update backend CORS_ORIGINS
2. Include frontend URL
3. Redeploy backend

---

## 💰 COST

**Render Static Site:**
- Free tier: 100GB bandwidth/month
- **Cost: $0/month**

---

## 📊 COMBINED DEPLOYMENT

### Both Services on Render:

**Backend:**
- URL: `https://safar-backend.onrender.com`
- Type: Web Service (Python/Flask)

**Frontend:**
- URL: `https://safar-frontend.onrender.com`
- Type: Static Site

**Total Cost:** $0-7/month (depending on usage)

---

## 🎯 SUCCESS CRITERIA

✅ Frontend deployed successfully  
✅ Backend deployed successfully  
✅ CORS configured correctly  
✅ Full user journey works  
✅ No console errors  
✅ Works in Telegram  

---

**Ready to deploy!** 🚀

Last Updated: March 26, 2026
