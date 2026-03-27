#!/usr/bin/env python3
"""
Initialize database with test data for Mini App testing
"""
import sqlite3
import os

DB_PATH = 'shop_bot.db'

def init_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("✅ Creating tables...")
    
    # Categories
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            emoji TEXT,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Products
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            category_id INTEGER,
            subcategory_id INTEGER,
            brand TEXT,
            image_url TEXT,
            stock INTEGER DEFAULT 0,
            views INTEGER DEFAULT 0,
            sales_count INTEGER DEFAULT 0,
            is_active INTEGER DEFAULT 1,
            cost_price REAL DEFAULT 0,
            original_price REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Cart items
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cart_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')
    
    # Orders
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            total_amount REAL NOT NULL,
            status TEXT DEFAULT 'pending',
            delivery_address TEXT,
            payment_method TEXT,
            payment_status TEXT DEFAULT 'pending',
            promo_discount REAL DEFAULT 0,
            delivery_cost REAL DEFAULT 0,
            comment TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Order items
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')
    
    # Favorites
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')
    
    # Users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE NOT NULL,
            name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            language TEXT DEFAULT 'ru',
            is_admin INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            acquisition_channel TEXT
        )
    ''')
    
    conn.commit()
    print("✅ Tables created successfully!")
    
    # Check if we need to add test data
    cursor.execute('SELECT COUNT(*) FROM categories')
    count = cursor.fetchone()[0]
    
    if count == 0:
        print("📦 Adding test data...")
        
        # Add categories
        categories = [
            ('Electronics', 'Electronic devices and gadgets', '📱'),
            ('Clothing', 'Men and women clothing', '👕'),
            ('Home & Garden', 'Home improvement and garden', '🏡'),
            ('Sports', 'Sports equipment and apparel', '⚽'),
            ('Books', 'Books and magazines', '📚'),
            ('Toys', 'Toys and games', '🎮')
        ]
        
        cursor.executemany('''
            INSERT INTO categories (name, description, emoji, is_active)
            VALUES (?, ?, ?, 1)
        ''', categories)
        
        # Add products
        products = [
            ('Smartphone Pro X', 'Latest smartphone with advanced features', 999000, 1, 'TechBrand', None, 15),
            ('Wireless Earbuds', 'High-quality wireless earbuds with noise cancellation', 250000, 1, 'AudioTech', None, 30),
            ('Smart Watch', 'Fitness tracking smartwatch', 450000, 1, 'TechBrand', None, 20),
            ('Cotton T-Shirt', 'Comfortable cotton t-shirt', 50000, 2, 'FashionCo', None, 100),
            ('Denim Jeans', 'Classic denim jeans', 120000, 2, 'FashionCo', None, 50),
            ('Running Shoes', 'Lightweight running shoes', 180000, 4, 'SportyFeet', None, 40),
            ('Yoga Mat', 'Non-slip yoga mat', 35000, 4, 'FitGear', None, 60),
            ('Desk Lamp', 'LED desk lamp with adjustable brightness', 75000, 3, 'HomeLight', None, 25),
            ('Coffee Maker', 'Automatic coffee maker', 350000, 3, 'KitchenPro', None, 15),
            ('Science Fiction Novel', 'Bestselling sci-fi novel', 25000, 5, 'BookWorld', None, 80),
            ('Board Game', 'Strategy board game for family', 65000, 6, 'GameMaster', None, 35),
            ('Bluetooth Speaker', 'Portable bluetooth speaker', 150000, 1, 'AudioTech', None, 45)
        ]
        
        cursor.executemany('''
            INSERT INTO products (name, description, price, category_id, brand, image_url, stock, is_active)
            VALUES (?, ?, ?, ?, ?, NULL, ?, 1)
        ''', [(p[0], p[1], p[2], p[3], p[4], p[6]) for p in products])
        
        conn.commit()
        print("✅ Test data added successfully!")
    else:
        print("ℹ️  Database already has data, skipping test data insertion")
    
    # Print summary
    cursor.execute('SELECT COUNT(*) FROM categories')
    cat_count = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM products')
    prod_count = cursor.fetchone()[0]
    
    print(f"\n📊 Database Summary:")
    print(f"   Categories: {cat_count}")
    print(f"   Products: {prod_count}")
    print(f"\n✅ Database ready for testing!")
    
    conn.close()

if __name__ == '__main__':
    init_database()
