"""
База данных для телеграм-бота интернет-магазина
"""
import logging

import sqlite3

class DatabaseManager:
    def __init__(self, db_path='shop_bot.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        # Обновление схемы: роль пользователя
        try:
            conn_alter = sqlite3.connect(self.db_path)
            cur_alter = conn_alter.cursor()
            cur_alter.execute("ALTER TABLE users ADD COLUMN role TEXT")
            conn_alter.commit()
        except Exception:
            pass
        finally:
            try:
                conn_alter.close()
            except Exception:
                pass

        """Инициализация базы данных"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Создаем все таблицы
            self.create_tables(cursor)
            # Миграция таблицы orders (добаляем недостающие колонки)
            self._migrate_orders_table(cursor)
            
            # Создаем тестовые данные если база пустая
            if self.is_database_empty(cursor):
                self.create_test_data(cursor)
            
            conn.commit()
            
        except Exception as e:
            logging.info(f"Ошибка инициализации базы данных: {e}")
            if 'conn' in locals():
                conn.rollback()
        finally:
            if 'conn' in locals():
                conn.close()
    
    def create_tables(self, cursor):
        """Создание всех таблиц"""
        
        # Пользователи
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
        
        # Категории товаров
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
# Товары
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
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories (id),
    FOREIGN KEY (subcategory_id) REFERENCES subcategories (id)
)
        ''')
        
        # Корзина
        cursor.execute('''
CREATE TABLE IF NOT EXISTS cart (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    product_id INTEGER,
    quantity INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (product_id) REFERENCES products (id)
)
        ''')
        
        # Заказы
        cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    total_amount REAL,
    status TEXT DEFAULT 'pending',
    delivery_address TEXT,
    payment_method TEXT,
    payment_status TEXT DEFAULT 'pending',
    promo_discount REAL DEFAULT 0,
    delivery_cost REAL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
        ''')
        
        # Товары в заказах
        # Галерея изображений товаров
        cursor.execute('''
CREATE TABLE IF NOT EXISTS product_images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    image_url TEXT NOT NULL,
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products (id)
)
        ''')

        # Товары в заказах
        cursor.execute('''
CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    price REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders (id),
    FOREIGN KEY (product_id) REFERENCES products (id)
)
        ''')
        
        # Подкатегории/бренды
        cursor.execute('''
CREATE TABLE IF NOT EXISTS subcategories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category_id INTEGER,
    emoji TEXT,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories (id)
)
        ''')
        
        # Отзывы
        cursor.execute('''
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    product_id INTEGER,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (product_id) REFERENCES products (id)
)
        ''')
        
        # Избранное
        cursor.execute('''
CREATE TABLE IF NOT EXISTS favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    product_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (product_id) REFERENCES products (id),
    UNIQUE(user_id, product_id)
)
        ''')
        
        # Уведомления
        cursor.execute('''
CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    type TEXT DEFAULT 'info',
    is_read INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
        ''')
        
        # Баллы лояльности
        cursor.execute('''
CREATE TABLE IF NOT EXISTS loyalty_points (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE,
    current_points INTEGER DEFAULT 0,
    total_earned INTEGER DEFAULT 0,
    current_tier TEXT DEFAULT 'Bronze',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
        ''')
        
        # Промокоды
        cursor.execute('''
CREATE TABLE IF NOT EXISTS promo_codes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    discount_type TEXT NOT NULL,
    discount_value REAL NOT NULL,
    min_order_amount REAL DEFAULT 0,
    max_uses INTEGER,
    expires_at TIMESTAMP,
    description TEXT,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
        ''')
        
        # Использование промокодов
        cursor.execute('''
CREATE TABLE IF NOT EXISTS promo_uses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    promo_code_id INTEGER,
    user_id INTEGER,
    order_id INTEGER,
    discount_amount REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (promo_code_id) REFERENCES promo_codes (id),
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (order_id) REFERENCES orders (id)
)
        ''')
        
        # Отгрузки
        cursor.execute('''
CREATE TABLE IF NOT EXISTS shipments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    tracking_number TEXT UNIQUE,
    delivery_provider TEXT,
    delivery_option TEXT,
    time_slot TEXT,
    status TEXT DEFAULT 'created',
    estimated_delivery TIMESTAMP,
    scheduled_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders (id)
)
        ''')
        
        # Бизнес расходы
        cursor.execute('''
CREATE TABLE IF NOT EXISTS business_expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    expense_type TEXT NOT NULL,
    amount REAL NOT NULL,
    description TEXT,
    expense_date DATE NOT NULL,
    is_tax_deductible INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
        ''')
        
        # Поставщики
        cursor.execute('''
CREATE TABLE IF NOT EXISTS suppliers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    contact_email TEXT,
    phone TEXT,
    address TEXT,
    payment_terms TEXT,
    cost_per_unit REAL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
        ''')
        
        # Правила инвентаризации
        cursor.execute('''
CREATE TABLE IF NOT EXISTS inventory_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    reorder_point INTEGER NOT NULL,
    reorder_quantity INTEGER NOT NULL,
    supplier_id INTEGER,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products (id),
    FOREIGN KEY (supplier_id) REFERENCES suppliers (id)
)
        ''')
        
        # Движения товаров
        cursor.execute('''
CREATE TABLE IF NOT EXISTS inventory_movements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    movement_type TEXT NOT NULL,
    quantity_change INTEGER NOT NULL,
    old_quantity INTEGER,
    new_quantity INTEGER,
    supplier_id INTEGER,
    cost_per_unit REAL,
    reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products (id),
    FOREIGN KEY (supplier_id) REFERENCES suppliers (id)
)
        ''')
        
        # Заказы поставщикам
        cursor.execute('''
CREATE TABLE IF NOT EXISTS purchase_orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    supplier_id INTEGER,
    quantity INTEGER NOT NULL,
    cost_per_unit REAL NOT NULL,
    total_amount REAL NOT NULL,
    status TEXT DEFAULT 'pending',
    received_quantity INTEGER DEFAULT 0,
    delivered_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products (id),
    FOREIGN KEY (supplier_id) REFERENCES suppliers (id)
)
        ''')
        
        # Правила автоматизации
        cursor.execute('''
CREATE TABLE IF NOT EXISTS automation_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    trigger_type TEXT NOT NULL,
    conditions TEXT,
    actions TEXT,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
        ''')
        
        # Выполнения автоматизации
        cursor.execute('''
CREATE TABLE IF NOT EXISTS automation_executions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_id INTEGER,
    user_id INTEGER,
    rule_type TEXT,
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (rule_id) REFERENCES automation_rules (id),
    FOREIGN KEY (user_id) REFERENCES users (id)
)
        ''')
        
        # Логи безопасности
        cursor.execute('''
CREATE TABLE IF NOT EXISTS security_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    activity_type TEXT NOT NULL,
    details TEXT,
    severity TEXT DEFAULT 'low',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
        ''')
        
        # Блокировки пользователей
        cursor.execute('''
CREATE TABLE IF NOT EXISTS security_blocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    reason TEXT NOT NULL,
    blocked_until TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
        ''')
        
        # API ключи
        cursor.execute('''
CREATE TABLE IF NOT EXISTS api_keys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key_name TEXT NOT NULL,
    api_key TEXT UNIQUE NOT NULL,
    permissions TEXT,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
        ''')
        
        # Логи webhook'ов
        cursor.execute('''
CREATE TABLE IF NOT EXISTS webhook_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider TEXT NOT NULL,
    order_id INTEGER,
    user_id INTEGER,
    status TEXT NOT NULL,
    error_message TEXT,
    payload_preview TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders (id),
    FOREIGN KEY (user_id) REFERENCES users (id)
)
        ''')
        
        # Маркетинговые кампании
        cursor.execute('''
CREATE TABLE IF NOT EXISTS marketing_campaigns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    segment TEXT,
    campaign_type TEXT,
    target_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
        ''')
        
        # Резервы товаров
        cursor.execute('''
CREATE TABLE IF NOT EXISTS stock_reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    order_id INTEGER,
    quantity INTEGER NOT NULL,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products (id),
    FOREIGN KEY (order_id) REFERENCES orders (id)
)
        ''')
        
        # Сессии инвентаризации
        cursor.execute('''
CREATE TABLE IF NOT EXISTS stocktaking_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location TEXT DEFAULT 'Основной склад',
    status TEXT DEFAULT 'active',
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_by INTEGER,
    FOREIGN KEY (created_by) REFERENCES users (id)
)
        ''')
        
        # Элементы инвентаризации
        cursor.execute('''
CREATE TABLE IF NOT EXISTS stocktaking_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER,
    product_id INTEGER,
    system_quantity INTEGER,
    counted_quantity INTEGER,
    counted_at TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES stocktaking_sessions (id),
    FOREIGN KEY (product_id) REFERENCES products (id)
)
        ''')
        
        # Логи активности пользователей
        cursor.execute('''
CREATE TABLE IF NOT EXISTS user_activity_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT NOT NULL,
    search_query TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
        ''')
        
        # Товары флеш-распродажи
        cursor.execute('''
CREATE TABLE IF NOT EXISTS flash_sale_products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    promo_code_id INTEGER,
    product_id INTEGER,
    FOREIGN KEY (promo_code_id) REFERENCES promo_codes (id),
    FOREIGN KEY (product_id) REFERENCES products (id)
)
        ''')
        
        # Запланированные посты
        cursor.execute('''
CREATE TABLE IF NOT EXISTS scheduled_posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    image_url TEXT,
    time_morning TEXT,
    time_afternoon TEXT,
    time_evening TEXT,
    target_audience TEXT DEFAULT 'all',
    bot_username TEXT DEFAULT 'Safar_call_bot',
    website_url TEXT DEFAULT 'https://your-website.com',
    include_reviews INTEGER DEFAULT 1,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
        ''')
        
        # Статистика постов
        cursor.execute('''
CREATE TABLE IF NOT EXISTS post_statistics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER,
    time_period TEXT,
    sent_count INTEGER DEFAULT 0,
    error_count INTEGER DEFAULT 0,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES scheduled_posts (id)
)
        ''')
        
        # Создаем индексы для оптимизации
        self.create_indexes(cursor)
    
    def create_indexes(self, cursor):
        """Создание индексов для оптимизации"""
        indexes = [
            'CREATE INDEX IF NOT EXISTS idx_users_telegram_id ON users(telegram_id)',
            'CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id)',
            'CREATE INDEX IF NOT EXISTS idx_orders_user ON orders(user_id)',
            'CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status)',
            'CREATE INDEX IF NOT EXISTS idx_cart_user ON cart(user_id)',
            'CREATE INDEX IF NOT EXISTS idx_reviews_product ON reviews(product_id)',
            'CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_id)',
            'CREATE INDEX IF NOT EXISTS idx_inventory_movements_product ON inventory_movements(product_id)',
            'CREATE INDEX IF NOT EXISTS idx_security_logs_user ON security_logs(user_id)',
            'CREATE INDEX IF NOT EXISTS idx_automation_executions_user ON automation_executions(user_id)'
        ]
        
        for index_sql in indexes:
            try:
                cursor.execute(index_sql)
            except Exception as e:
                logging.info(f"Ошибка создания индекса: {e}")
    
    def is_database_empty(self, cursor):
        """Проверка пустоты базы данных"""
        cursor.execute('SELECT COUNT(*) FROM categories')
        return cursor.fetchone()[0] == 0
    
    def create_test_data(self, cursor):
        """Создание тестовых данных"""
        # Создаем админа из переменных окружения
        from config import BOT_CONFIG
        admin_telegram_id = BOT_CONFIG.get('admin_telegram_id')
        admin_name = BOT_CONFIG.get('admin_name', 'Admin')
        
        if admin_telegram_id:
            try:
                admin_telegram_id = int(admin_telegram_id)
                cursor.execute('''
                    INSERT OR IGNORE INTO users (telegram_id, name, is_admin, language, created_at)
                    VALUES (?, ?, 1, 'ru', CURRENT_TIMESTAMP)
                ''', (admin_telegram_id, admin_name))
                logging.info(f"✅ Админ создан: {admin_name} (ID: {admin_telegram_id})")
            except ValueError:
                logging.info(f"⚠️ Неверный ADMIN_TELEGRAM_ID: {admin_telegram_id}")
        else:
            logging.info("⚠️ ADMIN_TELEGRAM_ID не установлен в конфигурации")
        
        # Категории
        categories = [
            ('Электроника', 'Смартфоны, ноутбуки, гаджеты', '📱'),
            ('Одежда', 'Мужская и женская одежда', '👕'),
            ('Дом и сад', 'Товары для дома и дачи', '🏠'),
            ('Спорт', 'Спортивные товары и инвентарь', '⚽'),
            ('Красота', 'Косметика и парфюмерия', '💄'),
            ('Книги', 'Художественная и техническая литература', '📚')
        ]
        
        cursor.executemany(
            'INSERT INTO categories (name, description, emoji) VALUES (?, ?, ?)',
            categories
        )
        
        # Подкатегории/бренды
        subcategories = [
            ('Apple', 1, '🍎'),      # Электроника - Apple
            ('Samsung', 1, '📱'),    # Электроника - Samsung
            ('Nike', 2, '✔️'),       # Одежда - Nike
            ('Levi\'s', 2, '👖'),    # Одежда - Levi's
            ('Delonghi', 3, '☕'),   # Дом и сад - Delonghi
            ('Adidas', 4, '👟'),     # Спорт - Adidas
            ('Chanel', 5, '💎'),     # Красота - Chanel
            ('Книги', 6, '📖')       # Книги - общие
        ]
        
        cursor.executemany(
            'INSERT INTO subcategories (name, category_id, emoji) VALUES (?, ?, ?)',
            subcategories
        )
        
        # Товары
        products = [
            ('iPhone 14', 'Смартфон Apple iPhone 14 128GB', 799.99, 1, 1, 'Apple', 'https://images.pexels.com/photos/788946/pexels-photo-788946.jpeg', 50, 0, 0, 1, 600.00),
            ('Samsung Galaxy S23', 'Флагманский смартфон Samsung', 699.99, 1, 1, 'Samsung', 'https://images.pexels.com/photos/1092644/pexels-photo-1092644.jpeg', 30, 0, 0, 1, 500.00),
            ('MacBook Air M2', 'Ноутбук Apple MacBook Air с чипом M2', 1199.99, 1, 1, 'Apple', 'https://images.pexels.com/photos/18105/pexels-photo.jpg', 20, 0, 0, 1, 900.00),
            ('Футболка Nike', 'Спортивная футболка Nike Dri-FIT', 29.99, 2, 2, 'Nike', 'https://images.pexels.com/photos/8532616/pexels-photo-8532616.jpeg', 100, 0, 0, 1, 15.00),
            ('Джинсы Levi\'s', 'Классические джинсы Levi\'s 501', 79.99, 2, 2, 'Levi\'s', 'https://images.pexels.com/photos/1598507/pexels-photo-1598507.jpeg', 75, 0, 0, 1, 40.00),
            ('Кофеварка Delonghi', 'Автоматическая кофеварка', 299.99, 3, 3, 'Delonghi', 'https://images.pexels.com/photos/324028/pexels-photo-324028.jpeg', 25, 0, 0, 1, 180.00),
            ('Набор посуды', 'Набор кастрюль из нержавеющей стали', 149.99, 3, 3, 'Generic', 'https://images.pexels.com/photos/4226796/pexels-photo-4226796.jpeg', 40, 0, 0, 1, 80.00),
            ('Кроссовки Adidas', 'Беговые кроссовки Adidas Ultraboost', 159.99, 4, 4, 'Adidas', 'https://images.pexels.com/photos/2529148/pexels-photo-2529148.jpeg', 60, 0, 0, 1, 90.00),
            ('Гантели 10кг', 'Набор гантелей для домашних тренировок', 89.99, 4, 4, 'Generic', 'https://images.pexels.com/photos/416717/pexels-photo-416717.jpeg', 35, 0, 0, 1, 50.00),
            ('Крем для лица', 'Увлажняющий крем с гиалуроновой кислотой', 49.99, 5, 5, 'Generic', 'https://images.pexels.com/photos/3685530/pexels-photo-3685530.jpeg', 80, 0, 0, 1, 25.00),
            ('Парфюм Chanel', 'Туалетная вода Chanel No.5', 129.99, 5, 5, 'Chanel', 'https://images.pexels.com/photos/965989/pexels-photo-965989.jpeg', 45, 0, 0, 1, 70.00),
            ('Книга "Python для начинающих"', 'Учебник по программированию на Python', 39.99, 6, 6, 'Generic', 'https://images.pexels.com/photos/159711/books-bookstore-book-reading-159711.jpeg', 90, 0, 0, 1, 20.00),
            ('Роман "1984"', 'Классический роман Джорджа Оруэлла', 19.99, 6, 6, 'Generic', 'https://images.pexels.com/photos/46274/pexels-photo-46274.jpeg', 120, 0, 0, 1, 10.00),
            ('Беспроводные наушники', 'AirPods Pro с шумоподавлением', 249.99, 1, 1, 'Apple', 'https://images.pexels.com/photos/3394650/pexels-photo-3394650.jpeg', 70, 0, 0, 1, 150.00)
        ]
        
        cursor.executemany('''
            INSERT INTO products (name, description, price, category_id, subcategory_id, brand, image_url, stock, views, sales_count, is_active, cost_price)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', products)
        
        # Промокоды
        promo_codes = [
            ('WELCOME10', 'percentage', 10, 0, None, None, 'Скидка 10% для новых клиентов'),
            ('SAVE20', 'percentage', 20, 100, 100, None, 'Скидка 20% при заказе от $100'),
            ('FIXED15', 'fixed', 15, 50, 50, None, 'Скидка $15 при заказе от $50'),
            ('VIP25', 'percentage', 25, 200, 20, None, 'VIP скидка 25% для заказов от $200')
        ]
        
        cursor.executemany('''
            INSERT INTO promo_codes (code, discount_type, discount_value, min_order_amount, max_uses, expires_at, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', promo_codes)
        
        # Поставщики
        suppliers = [
            ('Apple Inc.', 'supplier@apple.com', '+1-800-275-2273', 'Cupertino, CA', 'NET 30'),
            ('Samsung Electronics', 'b2b@samsung.com', '+82-2-2255-0114', 'Seoul, South Korea', 'NET 45'),
            ('Nike Inc.', 'wholesale@nike.com', '+1-503-671-6453', 'Beaverton, OR', 'NET 30'),
            ('Местный поставщик', 'local@supplier.uz', '+998-71-123-4567', 'Ташкент, Узбекистан', 'Предоплата')
        ]
        
        cursor.executemany('''
            INSERT INTO suppliers (name, contact_email, phone, address, payment_terms)
            VALUES (?, ?, ?, ?, ?)
        ''', suppliers)
    
    
    def execute_query(self, query, params=None):
        """Выполнение SQL запроса с корректным возвратом результата.
        SELECT -> list[tuple]
        INSERT -> lastrowid (int)
        UPDATE/DELETE -> rowcount (int)
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            q = query.strip().upper()
            if q.startswith('SELECT'):
                result = cursor.fetchall()
                # DEBUG для categories
                if 'CATEGORIES' in q:
                    logging.info(f"DEBUG execute_query: SELECT вернул {len(result)} записей")
                    if result:
                        logging.info(f"  Первая запись: {result[0]}")
            else:
                conn.commit()
                op = q.split()[0]
                if op == 'INSERT':
                    result = cursor.lastrowid
                else:
                    result = cursor.rowcount
            return result
        except Exception as e:
            logging.info(f"Ошибка выполнения запроса: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()

    def get_user_by_telegram_id(self, telegram_id):
        """Получение пользователя по telegram_id"""
        return self.execute_query(
            'SELECT * FROM users WHERE telegram_id = ?',
            (telegram_id,)
        )
    
    def add_user(self, telegram_id, name, phone=None, email=None, language='ru'):
        """Добавление нового пользователя"""
        try:
            # Проверяем, не существует ли уже пользователь
            existing = self.execute_query(
                'SELECT id FROM users WHERE telegram_id = ?',
                (telegram_id,)
            )
            
            if existing:
                return existing[0][0]  # Возвращаем существующий ID
            
            # Создаем нового пользователя
            result = self.execute_query('''
                INSERT INTO users (telegram_id, name, phone, email, language)
                VALUES (?, ?, ?, ?, ?)
            ''', (telegram_id, name, phone, email, language))
            
            return result
        except Exception as e:
            logging.info(f"Ошибка добавления пользователя: {e}")
            return None
    
    def get_categories(self):
        """Получение всех активных категорий"""
        return self.execute_query(
            'SELECT * FROM categories WHERE is_active = 1 ORDER BY name'
        )
    
    def get_products_by_category(self, category_id, limit=10, offset=0):
        """Получение товаров по категории"""
        # Сначала получаем подкатегории
        subcategories = self.execute_query('''
            SELECT DISTINCT s.id, s.name, s.emoji, COUNT(p.id) as products_count
            FROM subcategories s
            LEFT JOIN products p ON s.id = p.subcategory_id AND p.is_active = 1
            WHERE s.category_id = ? AND s.is_active = 1
            GROUP BY s.id, s.name, s.emoji
            HAVING products_count > 0
            ORDER BY s.name
        ''', (category_id,))
        
        return subcategories
    
    def get_products_by_subcategory(self, subcategory_id, limit=10, offset=0):
        """Получение товаров по подкатегории"""
        return self.execute_query('''
            SELECT * FROM products 
            WHERE subcategory_id = ? AND is_active = 1 
            ORDER BY name 
            LIMIT ? OFFSET ?
        ''', (subcategory_id, limit, offset))
    
    def get_product_by_id(self, product_id):
        """Получение товара по ID"""
        result = self.execute_query(
            'SELECT * FROM products WHERE id = ?',
            (product_id,)
        )
        return result[0] if result else None
    
    def add_to_cart(self, user_id, product_id, quantity=1):
        """Добавление товара в корзину"""
        logging.info(f"DEBUG: add_to_cart вызван с user_id={user_id}, product_id={product_id}, quantity={quantity}")
        
        # Проверяем наличие товара
        product = self.execute_query(
            'SELECT stock FROM products WHERE id = ? AND is_active = 1',
            (product_id,)
        )
        
        logging.info(f"DEBUG: Товар в базе: {product}")
        
        if not product or product[0][0] < quantity:
            logging.info(f"DEBUG: Товар недоступен или недостаточно на складе")
            return None
        
        # Проверяем, есть ли уже товар в корзине
        existing = self.execute_query(
            'SELECT id, quantity FROM cart WHERE user_id = ? AND product_id = ?',
            (user_id, product_id)
        )
        
        logging.info(f"DEBUG: Существующий товар в корзине: {existing}")
        
        if existing:
            # Обновляем количество
            new_quantity = existing[0][1] + quantity
            # Проверяем не превышает ли новое количество остаток
            if new_quantity > product[0][0]:
                logging.info(f"DEBUG: Новое количество {new_quantity} превышает остаток {product[0][0]}")
                return None
            
            # Обновляем количество и время
            result = self.execute_query(
                'UPDATE cart SET quantity = ?, created_at = CURRENT_TIMESTAMP WHERE id = ?',
                (new_quantity, existing[0][0])
            )
            logging.info(f"DEBUG: Обновление количества в корзине: {result}")
            return existing[0][0]  # Возвращаем ID записи корзины
        else:
            # Добавляем новый товар
            result = self.execute_query(
                'INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)',
                (user_id, product_id, quantity)
            )
            logging.info(f"DEBUG: Добавление нового товара в корзину: {result}")
            return result
    
    def get_cart_items(self, user_id):
        """Получение товаров из корзины"""
        return self.execute_query('''
            SELECT c.id, p.name, p.price, c.quantity, p.image_url, p.id as product_id
            FROM cart c
            JOIN products p ON c.product_id = p.id
            WHERE c.user_id = ?
            ORDER BY c.created_at DESC
        ''', (user_id,))
    
    def clear_cart(self, user_id):
        """Удаляет все позиции из корзины пользователя (совместимо со схемами cart и cart_items)."""
        try:
            # основной вариант (таблица cart)
            self.execute_query('DELETE FROM cart WHERE user_id = ?', (user_id,))
            # на всякий случай, если используется cart_items
            try:
                self.execute_query('DELETE FROM cart_items WHERE user_id = ?', (user_id,))
            except Exception:
                pass
            return 1
        except Exception as e:
            logging.info(f"Ошибка очистки корзины: {e}")
            return None

    def create_order(self, user_id, total_amount, delivery_address, payment_method, latitude=None, longitude=None):
        """Создание заказа"""
        return self.execute_query('''
            INSERT INTO orders (user_id, total_amount, delivery_address, payment_method) VALUES (?, ?, ?, ?)
        ''', (user_id, total_amount, delivery_address, payment_method))
    
    def add_order_items(self, order_id, cart_items):
        """Добавление товаров в заказ"""
        for item in cart_items:
            self.execute_query('''
                INSERT INTO order_items (order_id, product_id, quantity, price)
                VALUES (?, ?, ?, ?)
            ''', (order_id, item[5], item[3], item[2]))  # product_id, quantity, price
    
    def get_user_orders(self, user_id):
        """Получение заказов пользователя"""
        return self.execute_query('''
            SELECT * FROM orders 
            WHERE user_id = ? 
            ORDER BY created_at DESC
        ''', (user_id,))
    
    def get_order_details(self, order_id):
        """Получение деталей заказа"""
        order = self.execute_query(
            'SELECT * FROM orders WHERE id = ?',
            (order_id,)
        )
        
        items = self.execute_query('''
            SELECT oi.quantity, oi.price, p.name, p.image_url
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = ?
        ''', (order_id,))
        
        if order:
            return {
                'order': order[0],
                'items': items
            }
        return None
    
    def update_order_status(self, order_id, status):
        """Обновление статуса заказа"""
        return self.execute_query(
            'UPDATE orders SET status = ? WHERE id = ?',
            (status, order_id)
        )
    
    def search_products(self, query, limit=10):
        """Поиск товаров"""
        return self.execute_query('''
            SELECT * FROM products 
            WHERE (name LIKE ? OR description LIKE ?) AND is_active = 1
            ORDER BY name
            LIMIT ?
        ''', (f'%{query}%', f'%{query}%', limit))
    
    def add_review(self, user_id, product_id, rating, comment):
        """Добавление отзыва"""
        return self.execute_query('''
            INSERT INTO reviews (user_id, product_id, rating, comment)
            VALUES (?, ?, ?, ?)
        ''', (user_id, product_id, rating, comment))
    
    def get_product_reviews(self, product_id):
        """Получение отзывов на товар"""
        return self.execute_query('''
            SELECT r.rating, r.comment, r.created_at, u.name
            FROM reviews r
            JOIN users u ON r.user_id = u.id
            WHERE r.product_id = ?
            ORDER BY r.created_at DESC
        ''', (product_id,))
    
    def add_to_favorites(self, user_id, product_id):
        """Добавление в избранное"""
        return self.execute_query('''
            INSERT OR IGNORE INTO favorites (user_id, product_id)
            VALUES (?, ?)
        ''', (user_id, product_id))
    
    def remove_from_favorites(self, user_id, product_id):
        """Удаление из избранного"""
        return self.execute_query(
            'DELETE FROM favorites WHERE user_id = ? AND product_id = ?',
            (user_id, product_id)
        )
    
    def get_user_favorites(self, user_id):
        """Получение избранных товаров"""
        return self.execute_query('''
            SELECT p.* FROM products p
            JOIN favorites f ON p.id = f.product_id
            WHERE f.user_id = ? AND p.is_active = 1
            ORDER BY f.created_at DESC
        ''', (user_id,))
    
    def add_notification(self, user_id, title, message, notification_type='info'):
        """Добавление уведомления"""
        return self.execute_query('''
            INSERT INTO notifications (user_id, title, message, type)
            VALUES (?, ?, ?, ?)
        ''', (user_id, title, message, notification_type))
    
    def get_unread_notifications(self, user_id):
        """Получение непрочитанных уведомлений"""
        return self.execute_query('''
            SELECT * FROM notifications 
            WHERE user_id = ? AND is_read = 0
            ORDER BY created_at DESC
        ''', (user_id,))
    
    def mark_notification_read(self, notification_id):
        """Отметка уведомления как прочитанного"""
        return self.execute_query(
            'UPDATE notifications SET is_read = 1 WHERE id = ?',
            (notification_id,)
        )
    
    def get_user_loyalty_points(self, user_id):
        """Получение баллов лояльности"""
        result = self.execute_query(
            'SELECT * FROM loyalty_points WHERE user_id = ?',
            (user_id,)
        )
        
        if not result:
            # Создаем запись если её нет
            self.execute_query(
                'INSERT INTO loyalty_points (user_id) VALUES (?)',
                (user_id,)
            )
            return self.get_user_loyalty_points(user_id)
        
        return result[0]
    
    def update_loyalty_points(self, user_id, points_to_add):
        """Обновление баллов лояльности"""
        return self.execute_query('''
            UPDATE loyalty_points 
            SET current_points = current_points + ?,
                total_earned = total_earned + ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
        ''', (points_to_add, points_to_add, user_id))
    
    def remove_from_cart(self, cart_item_id):
        """Удаление товара из корзины"""
        return self.execute_query(
            'DELETE FROM cart WHERE id = ?',
            (cart_item_id,)
        )
    
    def update_cart_quantity(self, cart_item_id, quantity):
        """Обновление количества товара в корзине"""
        if quantity <= 0:
            return self.remove_from_cart(cart_item_id)
        else:
            return self.execute_query(
                'UPDATE cart SET quantity = ? WHERE id = ?',
                (quantity, cart_item_id)
            )
    
    def increment_product_views(self, product_id):
        """Увеличение счетчика просмотров товара"""
        return self.execute_query(
            'UPDATE products SET views = views + 1 WHERE id = ?',
            (product_id,)
        )
    
    def get_popular_products(self, limit=10):
        """Получение популярных товаров"""
        return self.execute_query('''
            SELECT * FROM products 
            WHERE is_active = 1
            ORDER BY views DESC, sales_count DESC
            LIMIT ?
        ''', (limit,))
    
    def update_user_language(self, user_id, language):
        """Обновление языка пользователя"""
        return self.execute_query(
            'UPDATE users SET language = ? WHERE id = ?',
            (language, user_id)
        )

# Миграция: добавить колонки для координат заказа, если их нет


    def get_subcategories_by_category(self, category_id):
        """Подкатегории по категории"""
        return self.execute_query(
            'SELECT id, name FROM subcategories WHERE category_id = ? AND is_active = 1 ORDER BY name',
            (category_id,)
        )


    def _migrate_orders_table(self, cursor):
        """Добавляет в таблицу orders недостающие колонки, если их нет (совместимость со старыми БД)."""
        try:
            cursor.execute("PRAGMA table_info(orders)")
            cols = [row[1] for row in cursor.fetchall()]
            # Обязательные поля новой схемы
            want = [
                ("payment_method", "TEXT"),
                ("payment_status", "TEXT DEFAULT 'pending'"),
                ("promo_discount", "REAL DEFAULT 0"),
                ("delivery_cost", "REAL DEFAULT 0"),
                ("created_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
            ]
            for col, ddl in want:
                if col not in cols:
                    cursor.execute(f"ALTER TABLE orders ADD COLUMN {col} {ddl}")
        except Exception as e:
            logging.info(f"orders migrate warn: {e}")

    def update_user_phone_by_telegram_id(self, telegram_id, phone):
        """Обновляет номер телефона пользователя по telegram_id"""
        if not phone:
            return 0
        # нормализация: убрать пробелы
        phone_norm = str(phone).strip()
        try:
            return self.execute_query(
                'UPDATE users SET phone = ? WHERE telegram_id = ?',
                (phone_norm, telegram_id)
            )
        except Exception as e:
            logging.info(f"Ошибка обновления телефона: {e}")
            return None
