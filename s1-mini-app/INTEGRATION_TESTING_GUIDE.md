# 🧪 INTEGRATION & TESTING GUIDE

**S1 Mini App - Complete Integration Instructions**  
**Date:** March 26, 2026  
**Status:** ✅ Ready for Testing

---

## 📋 TABLE OF CONTENTS

1. [Quick Start](#quick-start)
2. [Backend Setup](#backend-setup)
3. [Frontend Setup](#frontend-setup)
4. [Testing Checklist](#testing-checklist)
5. [API Endpoints Reference](#api-endpoints-reference)
6. [Troubleshooting](#troubleshooting)

---

## 🚀 QUICK START

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+
- SQLite3
- Telegram Bot Token (from @BotFather)

### 1. Backend (Port 5000)
```bash
cd /home/duck/Документы/Safar-main/web_admin
python3 run.py
```

### 2. Frontend (Port 5173)
```bash
cd /home/duck/Документы/Safar-main/s1-mini-app
npm install
npm run dev
```

### 3. Test in Browser
Open: http://localhost:5173

---

## 🔧 BACKEND SETUP

### Step 1: Install Python Dependencies

```bash
cd /home/duck/Документы/Safar-main/web_admin
pip3 install -r requirements.txt
```

**Required packages:**
```
Flask==3.0.0
Flask-CORS==4.0.0
requests==2.31.0
```

### Step 2: Configure Environment

Create `.env` file in root directory:

```bash
cp .env.example .env
nano .env
```

**Required variables:**
```env
# Bot token from @BotFather
TELEGRAM_BOT_TOKEN=your_bot_token_here

# Admin credentials
ADMIN_NAME=admin
ADMIN_PASSWORD=admin_password

# Flask secret key
FLASK_SECRET_KEY=your-secret-key-change-in-production

# Development mode (disable auth for testing)
DISABLE_MINI_APP_AUTH=True
```

### Step 3: Verify Database

Check that database exists and has required tables:

```bash
sqlite3 shop_bot.db ".tables"
```

**Required tables:**
- categories
- products
- cart_items
- orders
- order_items
- favorites
- users

### Step 4: Add Test Data (Optional)

Run this SQL to add sample data:

```sql
-- Categories
INSERT INTO categories (name, emoji, is_active) VALUES 
('Электроника', '📱', 1),
('Одежда', '👕', 1),
('Дом и сад', '🏡', 1);

-- Products
INSERT INTO products (name, description, price, category_id, stock, is_active) VALUES
('Смартфон', 'Мощный смартфон', 999000, 1, 10, 1),
('Футболка', 'Хлопковая футболка', 50000, 2, 50, 1),
('Лампа', 'Настольная лампа', 75000, 3, 20, 1);
```

### Step 5: Start Backend Server

```bash
cd /home/duck/Документы/Safar-main/web_admin
python3 run.py
```

**Expected output:**
```
✅ CORS настроено для API
✅ Telegram Mini App API успешно подключено!
🔧 DISABLE_AUTH_FOR_DEV=True (для отключения авторизации в разработке)
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://172.19.0.1:5000
```

---

## 💻 FRONTEND SETUP

### Step 1: Install Dependencies

```bash
cd /home/duck/Документы/Safar-main/s1-mini-app
npm install
```

### Step 2: Configure Environment

```bash
cp .env.example .env
nano .env
```

**Set API URL:**
```env
VITE_API_URL=http://localhost:5000/api
```

### Step 3: Start Development Server

```bash
npm run dev
```

**Expected output:**
```
  VITE v6.1.0  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

### Step 4: Build for Production

```bash
npm run build
npm run preview
```

**Build output:**
```
✓ built in 17.13s
dist/index.html                   0.64 kB │ gzip:   0.38 kB
dist/assets/index-CjEY5KcF.css   15.60 kB │ gzip:   4.13 kB
dist/assets/index-PbMm_BsX.js   323.18 kB │ gzip: 101.52 kB
```

---

## ✅ TESTING CHECKLIST

### Backend API Tests

#### 1. Categories API
```bash
# Get all categories
curl http://localhost:5000/api/categories
```

**Expected response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "Электроника",
      "emoji": "📱",
      "is_active": true,
      "created_at": "2026-03-26T10:00:00"
    }
  ]
}
```

#### 2. Products API
```bash
# Get all products
curl http://localhost:5000/api/products

# Get product by ID
curl http://localhost:5000/api/products/1

# Search products
curl "http://localhost:5000/api/products/search?q=смартфон"
```

#### 3. Cart API
```bash
# Get cart items
curl http://localhost:5000/api/cart/items

# Add to cart
curl -X POST http://localhost:5000/api/cart/items \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 2}'

# Update cart item
curl -X PUT http://localhost:5000/api/cart/items/1 \
  -H "Content-Type: application/json" \
  -d '{"quantity": 3}'

# Delete from cart
curl -X DELETE http://localhost:5000/api/cart/items/1

# Clear cart
curl -X POST http://localhost:5000/api/cart/clear
```

#### 4. Orders API
```bash
# Create order
curl -X POST http://localhost:5000/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "delivery_address": "Tashkent, Yunusabad",
    "payment_method": "cash",
    "comment": "Deliver after 6PM"
  }'

# Get orders
curl http://localhost:5000/api/orders

# Get order details
curl http://localhost:5000/api/orders/1
```

#### 5. Favorites API
```bash
# Get favorites
curl http://localhost:5000/api/favorites

# Add to favorites
curl -X POST http://localhost:5000/api/favorites \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1}'

# Remove from favorites
curl -X DELETE http://localhost:5000/api/favorites/1
```

### Frontend Component Tests

#### Manual Testing Flow

1. **Catalog Page** (`/`)
   - [ ] Categories load and display
   - [ ] Products load and display
   - [ ] Category filter works
   - [ ] Search works
   - [ ] Product cards show correct info
   - [ ] "Add to Cart" button works

2. **Product Detail** (`/product/:id`)
   - [ ] Product information loads
   - [ ] Images display correctly
   - [ ] Price and discount shown
   - [ ] Quantity selector works
   - [ ] "Add to Cart" adds item
   - [ ] Related products show
   - [ ] Share button works
   - [ ] Favorite button toggles

3. **Cart** (`/cart`)
   - [ ] Cart items display
   - [ ] Quantity +/- works
   - [ ] Remove item works
   - [ ] Total amount calculates
   - [ ] Clear cart works
   - [ ] Empty state shows when empty
   - [ ] Checkout button navigates

4. **Checkout** (`/checkout`)
   - [ ] Contact form validates
   - [ ] Address input works
   - [ ] Payment method selection works
   - [ ] Order summary displays
   - [ ] Submit creates order
   - [ ] Redirects to orders after success

5. **Orders** (`/orders`)
   - [ ] Orders list displays
   - [ ] Status badges show correctly
   - [ ] Order details expand
   - [ ] Empty state shows when no orders

6. **Profile** (`/profile`)
   - [ ] User info displays
   - [ ] Statistics calculate
   - [ ] Navigation menu works
   - [ ] Logout button works

7. **Favorites** (`/favorites`)
   - [ ] Favorite products display
   - [ ] Remove from favorites works
   - [ ] "Add to Cart" works
   - [ ] Empty state shows

### Integration Tests

#### Full User Journey

1. **Browse → Buy Flow**
   ```
   Catalog → Product Detail → Add to Cart → 
   Cart → Checkout → Place Order → Orders
   ```

2. **Favorite Flow**
   ```
   Catalog → Product Detail → Add to Favorites → 
   Favorites → Add to Cart → Checkout
   ```

3. **Repeat Purchase**
   ```
   Profile → Orders → View Order → 
   Product Detail → Add to Cart → Checkout
   ```

---

## 📚 API ENDPOINTS REFERENCE

### Base URL
```
Development: http://localhost:5000/api
Production: https://your-api-domain.com/api
```

### Authentication
All endpoints require `X-Telegram-Init-Data` header (except in dev mode with `DISABLE_MINI_APP_AUTH=True`)

### Categories

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/categories` | Get all active categories |
| GET | `/categories/:id` | Get category by ID |

### Products

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/products` | Get all products (with filters) |
| GET | `/products/:id` | Get product by ID |
| GET | `/products/search?q=query` | Search products |
| POST | `/products/:id/views` | Increment view count |
| GET | `/products/:id/related` | Get related products |

### Cart

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/cart/items` | Get cart items |
| POST | `/cart/items` | Add item to cart |
| PUT | `/cart/items/:id` | Update cart item quantity |
| DELETE | `/cart/items/:id` | Remove item from cart |
| POST | `/cart/clear` | Clear entire cart |

### Orders

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/orders` | Create new order |
| GET | `/orders` | Get user's orders |
| GET | `/orders/:id` | Get order details |

### Favorites

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/favorites` | Get favorite items |
| POST | `/favorites` | Add item to favorites |
| DELETE | `/favorites/:id` | Remove from favorites |

---

## 🐛 TROUBLESHOOTING

### Backend Issues

#### Problem: CORS errors
**Solution:**
```bash
pip3 install flask-cors
# Verify in app.py:
# CORS(app, resources={r"/api/*": {"origins": "*"}})
```

#### Problem: Database not found
**Solution:**
```bash
# Check DB path in app.py
ls -la shop_bot.db
# Run migrations if needed
```

#### Problem: Port already in use
**Solution:**
```bash
# Find process using port 5000
lsof -i :5000
# Kill it
kill -9 <PID>
# Or change port in run.py
```

#### Problem: Module not found
**Solution:**
```bash
# Install dependencies
pip3 install -r requirements.txt
# Check Python path
export PYTHONPATH=/path/to/Safar-main
```

### Frontend Issues

#### Problem: API requests fail
**Solution:**
1. Check `.env` file exists
2. Verify `VITE_API_URL` is correct
3. Restart dev server: `npm run dev`
4. Check browser console for errors

#### Problem: Build fails
**Solution:**
```bash
# Clear cache
rm -rf node_modules package-lock.json
npm install
npm run build
```

#### Problem: TypeScript errors
**Solution:**
```bash
# Type check
npx tsc --noEmit
# Fix reported errors
```

#### Problem: Styles not loading
**Solution:**
```bash
# Reinstall Tailwind
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### Integration Issues

#### Problem: Authorization errors
**Solution:**
Set `DISABLE_MINI_APP_AUTH=True` in backend `.env` for development

#### Problem: Empty data
**Solution:**
Add test data to database:
```sql
INSERT INTO categories (name, emoji, is_active) VALUES ('Test', '📦', 1);
INSERT INTO products (name, description, price, category_id, stock, is_active) 
VALUES ('Test Product', 'Description', 1000, 1, 10, 1);
```

#### Problem: Images not showing
**Solution:**
1. Check image URLs in database
2. Verify `static/uploads` folder exists
3. Check Flask serves static files
4. Use placeholder images for testing

---

## 📊 PERFORMANCE CHECKLIST

### Backend Optimization
- [ ] Enable database connection pooling
- [ ] Add query caching
- [ ] Optimize SQL queries with indexes
- [ ] Enable Gzip compression
- [ ] Set proper cache headers

### Frontend Optimization
- [ ] Enable code splitting
- [ ] Lazy load images
- [ ] Implement infinite scroll
- [ ] Cache API responses (React Query)
- [ ] Minimize bundle size

### Network Optimization
- [ ] Enable CDN for static assets
- [ ] Compress images
- [ ] Use HTTP/2
- [ ] Enable browser caching
- [ ] Minimize API calls

---

## 🎯 PRODUCTION DEPLOYMENT

### Frontend (Vercel)

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Deploy**
   ```bash
   cd s1-mini-app
   vercel --prod
   ```

3. **Set Environment Variables**
   ```
   VITE_API_URL=https://your-api.render.com/api
   ```

### Backend (Render)

1. **Create Web Service**
   - Connect GitHub repository
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `python3 web_admin/run.py`

2. **Environment Variables**
   ```
   TELEGRAM_BOT_TOKEN=your_token
   ADMIN_NAME=admin
   ADMIN_PASSWORD=your_password
   FLASK_SECRET_KEY=your_secret
   DISABLE_MINI_APP_AUTH=False
   ```

3. **CORS Configuration**
   Update `app.py` with production domain:
   ```python
   CORS(app, resources={r"/api/*": {"origins": "https://your-app.vercel.app"}})
   ```

### Final Integration

1. **Update Frontend API URL**
   ```env
   VITE_API_URL=https://your-api.render.com/api
   ```

2. **Configure Telegram Bot**
   - Open @BotFather
   - Use `/mybots`
   - Select your bot
   - Bot Settings → Menu Button
   - Set URL to: `https://your-app.vercel.app`

3. **Test in Telegram**
   - Open your bot
   - Click Menu button
   - Test full user journey

---

## 📞 SUPPORT

### Documentation
- [CONTEXT.md](./CONTEXT.md) - Project context
- [STATUS_REPORT.md](./STATUS_REPORT.md) - Current status
- [VERIFICATION_FIX_REPORT.md](./VERIFICATION_FIX_REPORT.md) - Bug fixes

### External Resources
- [Telegram Web Apps Docs](https://core.telegram.org/bots/webapps)
- [@tma.js/sdk-react](https://docs.tma.ru/docs/sdk/js/packages/react)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev)

---

## ✅ READY TO LAUNCH CHECKLIST

### Backend
- [x] All API endpoints implemented
- [x] Database tables created
- [x] CORS configured
- [x] Authorization working
- [x] Test data added
- [ ] Production deployment
- [ ] Environment variables set

### Frontend
- [x] All pages implemented
- [x] All components working
- [x] API integration complete
- [x] Build successful
- [x] No TypeScript errors
- [ ] Production deployment
- [ ] Environment variables set

### Integration
- [ ] Backend accessible online
- [ ] Frontend accessible online
- [ ] Telegram bot configured
- [ ] Full user journey tested
- [ ] No console errors
- [ ] Mobile responsive
- [ ] Dark/light theme working

---

**Last updated:** March 26, 2026  
**Status:** ✅ Ready for Integration Testing  
**Next step:** Deploy to production and test in Telegram
