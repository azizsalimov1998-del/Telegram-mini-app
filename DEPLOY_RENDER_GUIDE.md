# 🚀 DEPLOY TO RENDER - COMPLETE GUIDE

**S1 Mini App Backend Deployment**  
**Date:** March 26, 2026  
**Status:** ✅ Ready for Production

---

## 📋 TABLE OF CONTENTS

1. [Prerequisites](#prerequisites)
2. [Database Setup](#database-setup)
3. [Deploy Backend to Render](#deploy-backend-to-render)
4. [Deploy Frontend to Vercel](#deploy-frontend-to-vercel)
5. [Configuration](#configuration)
6. [Post-Deployment](#post-deployment)
7. [Troubleshooting](#troubleshooting)

---

## ✅ PREREQUISITES

### Required Accounts:
- [x] Render account (https://render.com)
- [x] Vercel account (https://vercel.com)
- [x] Telegram Bot Token (from @BotFather)
- [x] GitHub account

### Files Prepared:
- [x] `render.yaml` - Render configuration
- [x] `web_admin/requirements.txt` - Python dependencies
- [x] `start.sh` - Startup script
- [x] `.env.example` - Environment variables template

---

## 🗄️ DATABASE SETUP

### Option 1: SQLite (Current - Simple)

**Pros:**
- ✅ Simple setup
- ✅ Free (included in Render plan)
- ✅ No additional configuration

**Cons:**
- ⚠️ Limited to single instance
- ⚠️ Not suitable for high traffic
- ⚠️ Backup management required

**Current Configuration:**
```yaml
disk:
  name: safar-data
  mountPath: /data
  sizeGB: 5
```

### Option 2: PostgreSQL (Recommended for Production)

**Steps to migrate:**

1. **Create PostgreSQL on Render:**
   - Go to Render Dashboard
   - New → Database
   - Name: `safar-db`
   - Region: Frankfurt
   - Plan: Starter (Free tier available)

2. **Update requirements.txt:**
   ```txt
   psycopg2-binary==2.9.9
   ```

3. **Update app.py to use PostgreSQL:**
   ```python
   # Get database URL from environment
   DATABASE_URL = os.getenv('DATABASE_URL')
   
   if DATABASE_URL:
       # Use PostgreSQL
       db = DatabaseManager(DATABASE_URL)
   else:
       # Fallback to SQLite
       db = DatabaseManager('/data/shop_bot.db')
   ```

4. **Add environment variable:**
   ```
   DATABASE_URL=postgresql://user:password@host:5432/dbname
   ```

**For now, we'll use SQLite (Option 1) as it's already configured.**

---

## 🚀 DEPLOY BACKEND TO RENDER

### Step 1: Push to GitHub

```bash
cd /home/duck/Документы/Safar-main

# Initialize git if not already done
git init
git add .
git commit -m "Prepare for Render deployment"

# Add remote (replace with your repo)
git remote add origin https://github.com/YOUR_USERNAME/Safar.git
git push -u origin main
```

### Step 2: Create Render Service

**Method A: Using render.yaml (Recommended)**

```bash
# Install Render CLI
npm install -g @render-cloud/cli

# Login to Render
render login

# Deploy using blueprint
render up render-backend.yaml
```

**Method B: Manual Setup (Web Interface)**

1. **Go to https://dashboard.render.com**
2. Click **New +** → **Blueprint**
3. Connect your GitHub repository
4. Select the repository
5. Render will detect `render.yaml` or `render-backend.yaml`
6. Click **Apply**

### Step 3: Configure Environment Variables

In Render Dashboard, set these variables:

```env
# Required
TELEGRAM_BOT_TOKEN=your_actual_bot_token_here
ADMIN_TELEGRAM_ID=your_telegram_id_here

# Optional but recommended
CORS_ORIGINS=https://your-app.vercel.app,https://safar.vercel.app
DISABLE_MINI_APP_AUTH=false
ENVIRONMENT=production
FLASK_SECRET_KEY=generate_secure_random_key_here
ADMIN_NAME=admin
ADMIN_PASSWORD=secure_password_here
```

**Get Telegram Bot Token:**
1. Open Telegram
2. Search for @BotFather
3. Send `/newbot` or select existing bot
4. Copy the token

**Get Your Telegram ID:**
1. Search for @userinfobot
2. Start the bot
3. It will show your Telegram ID

### Step 4: Deploy Settings

**Configure in Render Dashboard:**

- **Name:** `safar-backend`
- **Region:** Frankfurt (closest to your users)
- **Branch:** `main`
- **Root Directory:** Leave blank
- **Build Command:** 
  ```bash
  pip install -r web_admin/requirements.txt
  ```
- **Start Command:** 
  ```bash
  ./start.sh
  ```

**Instance Type:**
- Plan: **Starter** (Free tier or $7/month)
- Auto-Deploy: **Enabled**

### Step 5: Deploy

1. Click **Create Web Service**
2. Wait for build to complete (~3-5 minutes)
3. Check logs for any errors
4. Note the deployed URL: `https://safar-backend.onrender.com`

---

## 🌐 DEPLOY FRONTEND TO VERCEL

### Step 1: Prepare Frontend

```bash
cd /home/duck/Документы/Safar-main/s1-mini-app

# Update .env.production
cat > .env.production << EOF
VITE_API_URL=https://safar-backend.onrender.com/api
EOF

# Build to test
npm run build
```

### Step 2: Deploy to Vercel

**Method A: Vercel CLI**

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
cd s1-mini-app
vercel --prod
```

**Method B: Vercel Web Interface**

1. Go to https://vercel.com/new
2. Import your Git repository
3. Configure project:
   - **Framework Preset:** Vite
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
   - **Install Command:** `npm install`

### Step 3: Set Environment Variables in Vercel

In Vercel Dashboard → Settings → Environment Variables:

```env
VITE_API_URL=https://safar-backend.onrender.com/api
```

### Step 4: Configure Custom Domain (Optional)

1. In Vercel Dashboard → Domains
2. Add your domain: `app.yoursite.com`
3. Update DNS records as instructed
4. Wait for SSL certificate (~5 minutes)

---

## ⚙️ CONFIGURATION

### Update CORS in Backend

After frontend is deployed, update backend CORS:

1. In Render Dashboard → Environment
2. Add/Update `CORS_ORIGINS`:
   ```
   CORS_ORIGINS=https://your-app.vercel.app,https://safar.vercel.app
   ```
3. Save changes (auto-redeploys)

### Update API URL in Frontend

If backend URL changes:

1. In Vercel Dashboard → Environment Variables
2. Update `VITE_API_URL`
3. Redeploy (automatic)

---

## 🔧 POST-DEPLOYMENT TASKS

### 1. Test Backend API

```bash
# Replace with your actual Render URL
BACKEND_URL=https://safar-backend.onrender.com

# Test categories endpoint
curl ${BACKEND_URL}/api/categories

# Test products endpoint
curl ${BACKEND_URL}/api/products

# Expected: JSON response with data
```

### 2. Test Frontend

Open your Vercel URL in browser:
```
https://your-app.vercel.app
```

**Checklist:**
- [ ] Page loads
- [ ] Categories display
- [ ] Products load
- [ ] Can add to cart
- [ ] Checkout works
- [ ] No console errors

### 3. Configure Telegram Bot

1. Open @BotFather
2. Send `/mybots`
3. Select your bot
4. Bot Settings → Menu Button
5. Set URL: `https://your-app.vercel.app`
6. Set title: "Open Shop"

### 4. Test in Telegram

1. Open your bot in Telegram
2. Click Menu button
3. Complete test purchase
4. Verify order appears in admin panel

### 5. Monitor Logs

**Backend (Render):**
- Dashboard → Logs
- Watch for errors
- Check response times

**Frontend (Vercel):**
- Dashboard → Functions
- Monitor deployments
- Check analytics

---

## 🐛 TROUBLESHOOTING

### Backend Issues

#### Problem: Service won't start
**Solution:**
```bash
# Check logs in Render Dashboard
# Common issues:
# - Missing dependencies
# - Wrong start command
# - Port not set correctly

# Test locally first
cd web_admin
python3 run.py
```

#### Problem: Database not found
**Solution:**
```bash
# Ensure disk is mounted correctly
# Check /data directory exists
# Verify DB_FILENAME environment variable

# Re-run initialization
python3 init_test_db.py
```

#### Problem: CORS errors
**Solution:**
```bash
# Update CORS_ORIGINS in Render
# Include your Vercel URL
# Redeploy backend

# Example:
CORS_ORIGINS=https://my-app.vercel.app
```

#### Problem: 500 Internal Server Error
**Solution:**
- Check Render logs
- Verify TELEGRAM_BOT_TOKEN is valid
- Check database permissions
- Ensure all tables exist

### Frontend Issues

#### Problem: API requests fail
**Solution:**
```bash
# Check VITE_API_URL is correct
# Verify backend is running
# Test API directly with curl
# Check browser console for errors
```

#### Problem: Build fails
**Solution:**
```bash
# Clear cache and rebuild
rm -rf node_modules package-lock.json
npm install
npm run build

# Check Node version (should be 18+)
node --version
```

#### Problem: Styles not loading
**Solution:**
```bash
# Verify Tailwind config
# Check CSS imports
# Rebuild frontend
npm run build
```

---

## 📊 MONITORING & MAINTENANCE

### Render Monitoring

**Dashboard Metrics:**
- CPU usage
- Memory usage
- Request count
- Response times
- Error rates

**Alerts:**
- Enable email notifications
- Set up Slack integration (optional)

### Vercel Monitoring

**Analytics:**
- Page views
- Bandwidth usage
- Function invocations
- Error rates

**Performance:**
- Core Web Vitals
- Load times
- Bundle sizes

### Regular Maintenance

**Weekly:**
- Review error logs
- Check disk space usage
- Monitor API response times

**Monthly:**
- Update dependencies
- Review security patches
- Backup database (if SQLite)

**Quarterly:**
- Performance audit
- Cost review
- Consider PostgreSQL migration

---

## 💰 COST ESTIMATE

### Render (Backend)

**Starter Plan:**
- Free tier: 750 hours/month (~$0)
- Database: 5GB included
- Bandwidth: 100GB included
- **Total: ~$0-7/month** (depending on usage)

### Vercel (Frontend)

**Hobby Plan:**
- Free for personal projects
- Unlimited deployments
- 100GB bandwidth/month
- **Total: $0/month**

### Total Monthly Cost:
- **Development:** $0
- **Production (light traffic):** $7
- **Production (medium traffic):** $15-25

---

## 🎯 DEPLOYMENT CHECKLIST

### Pre-Deployment
- [ ] All code committed to GitHub
- [ ] Dependencies updated
- [ ] Environment variables documented
- [ ] Database initialized
- [ ] Tests passed locally

### Backend Deployment
- [ ] Render account created
- [ ] Repository connected
- [ ] Environment variables set
- [ ] Build successful
- [ ] Service running
- [ ] API endpoints responding

### Frontend Deployment
- [ ] Vercel account created
- [ ] Repository imported
- [ ] API URL updated
- [ ] Build successful
- [ ] Site live
- [ ] No console errors

### Integration
- [ ] CORS configured
- [ ] Frontend connects to backend
- [ ] Full user journey tested
- [ ] Telegram bot configured
- [ ] Test in Telegram app

### Post-Deployment
- [ ] Monitoring enabled
- [ ] Logs reviewed
- [ ] Performance acceptable
- [ ] Documentation updated
- [ ] Team notified

---

## 📞 SUPPORT RESOURCES

### Render Documentation
- [Deploying Python](https://render.com/docs/deploy-python)
- [Environment Variables](https://render.com/docs/environment-variables)
- [Persistent Disks](https://render.com/docs/disks)

### Vercel Documentation
- [Deploying React](https://vercel.com/docs/deployments/git)
- [Environment Variables](https://vercel.com/docs/concepts/projects/environment-variables)
- [Previews](https://vercel.com/docs/concepts/deployments/previews)

### Project Documentation
- [INTEGRATION_TESTING_GUIDE.md](./INTEGRATION_TESTING_GUIDE.md)
- [FINAL_STATUS.md](./FINAL_STATUS.md)
- [SERVERS_RUNNING.md](./SERVERS_RUNNING.md)

---

## 🎉 SUCCESS CRITERIA

Your deployment is successful when:

✅ Backend responds at: `https://safar-backend.onrender.com/api`  
✅ Frontend loads at: `https://your-app.vercel.app`  
✅ API calls succeed (no CORS errors)  
✅ Can complete full purchase flow  
✅ Orders appear in database  
✅ Telegram bot opens the app  
✅ No errors in logs  
✅ Response time < 500ms  

---

**Last Updated:** March 26, 2026  
**Status:** ✅ Ready for Deployment  
**Estimated Time:** 30-45 minutes  
**Difficulty:** Intermediate

🚀 **READY TO DEPLOY!**
