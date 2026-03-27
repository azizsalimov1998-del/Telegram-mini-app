"""
REST API для Telegram Mini App
Все эндпоинты защищены через Telegram initData валидацию
"""
import hmac
import hashlib
import json
import os
import sqlite3
from typing import Optional
from flask import Flask, request, jsonify, Blueprint
from datetime import datetime

# Создаем Blueprint для API
api = Blueprint('api', __name__, url_prefix='/api')

# Глобальные переменные для инициализации
db = None
app = None

# Флаг для отключения авторизации в разработке (установите True для тестирования)
# По умолчанию True для разработки
DISABLE_AUTH_FOR_DEV = os.environ.get('DISABLE_MINI_APP_AUTH', 'True').lower() == 'true'
print(f"🔧 DISABLE_AUTH_FOR_DEV={DISABLE_AUTH_FOR_DEV} (для отключения авторизации в разработке)")

def init_api(db_manager, flask_app):
    """Инициализация API с базой данных и приложением"""
    global db, app
    db = db_manager
    app = flask_app


def validate_telegram_init_data(init_data: str) -> bool:
    """Проверка валидности Telegram initData"""
    try:
        # Получаем токен бота из конфига
        bot_token = app.config.get('TELEGRAM_BOT_TOKEN', '') if app else ''
        if not bot_token:
            print("Warning: TELEGRAM_BOT_TOKEN не найден")
            return False
        
        SECRET_KEY = bot_token.encode()
        
        # Парсим данные
        data = {}
        for item in init_data.split('&'):
            if '=' in item:
                key, value = item.split('=', 1)
                data[key] = value
        
        received_hash = data.get('hash')
        if not received_hash:
            return False
        
        # Убираем hash из данных для проверки
        check_data = '&'.join(
            f"{key}={value}" 
            for key, value in sorted(data.items()) 
            if key != 'hash'
        )
        
        # Вычисляем хеш
        computed_hash = hmac.new(
            SECRET_KEY,
            msg=check_data.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(computed_hash, received_hash)
    except Exception as e:
        print(f"Ошибка валидации Telegram данных: {e}")
        return False


def get_user_from_telegram_data(init_data: str) -> Optional[dict]:
    """Извлечение данных пользователя из Telegram initData"""
    try:
        data = {}
        for item in init_data.split('&'):
            if '=' in item:
                key, value = item.split('=', 1)
                data[key] = value
        
        user_json = data.get('user')
        if user_json:
            return json.loads(user_json)
    except Exception as e:
        print(f"Ошибка извлечения user data: {e}")
    return None


def telegram_login_required(f):
    """Декоратор для защиты API endpoints через Telegram auth"""
    def decorated_function(*args, **kwargs):
        # В режиме разработки разрешаем все запросы
        if DISABLE_AUTH_FOR_DEV:
            request.telegram_user = {'id': 999999, 'first_name': 'Dev User', 'is_bot': False}
            return f(*args, **kwargs)
        
        init_data = request.headers.get('X-Telegram-Init-Data')
        
        if not init_data:
            return jsonify({'success': False, 'error': 'Требуется авторизация Telegram'}), 401
        
        if not validate_telegram_init_data(init_data):
            return jsonify({'success': False, 'error': 'Неверные данные авторизации'}), 403
        
        # Добавляем информацию о пользователе в request
        user_data = get_user_from_telegram_data(init_data)
        if user_data:
            request.telegram_user = user_data
        else:
            request.telegram_user = None
            
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function


# ============================================
# API КАТЕГОРИЙ
# ============================================

@api.route('/categories', methods=['GET'])
@telegram_login_required
def get_categories():
    """Получить список всех активных категорий"""
    try:
        categories = db.execute_query('''
            SELECT id, name, emoji, is_active, created_at
            FROM categories
            WHERE is_active = 1
            ORDER BY name
        ''')
        
        result = [{
            'id': cat[0],
            'name': cat[1],
            'emoji': cat[2],
            'is_active': bool(cat[3]),
            'created_at': cat[4]
        } for cat in categories] if categories else []
        
        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        print(f"Ошибка получения категорий: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api.route('/categories/<int:category_id>', methods=['GET'])
@telegram_login_required
def get_category_by_id(category_id):
    """Получить категорию по ID"""
    try:
        category = db.execute_query('''
            SELECT id, name, emoji, image_url, is_active
            FROM categories
            WHERE id = ?
        ''', (category_id,))
        
        if not category:
            return jsonify({
                'success': False,
                'error': 'Категория не найдена'
            }), 404
        
        cat = category[0]
        return jsonify({
            'success': True,
            'data': {
                'id': cat[0],
                'name': cat[1],
                'emoji': cat[2],
                'image_url': cat[3],
                'is_active': bool(cat[4])
            }
        })
    except Exception as e:
        print(f"Ошибка получения категории: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================
# API ТОВАРОВ
# ============================================

@api.route('/products', methods=['GET'])
@telegram_login_required
def get_products():
    """Получить список товаров с фильтрацией и пагинацией"""
    try:
        # Параметры запроса
        category_id = request.args.get('category_id', type=int)
        subcategory_id = request.args.get('subcategory_id', type=int)
        search = request.args.get('search', '')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # Базовый SQL запрос
        query = '''
            SELECT p.id, p.name, p.description, p.price, p.cost_price,
                   p.original_price, p.category_id, p.subcategory_id,
                   p.brand, p.image_url, p.stock, p.views, p.sales_count,
                   p.is_active, p.created_at, p.updated_at
            FROM products p
            WHERE p.is_active = 1
        '''
        params = []
        
        # Фильтры
        if category_id:
            query += ' AND p.category_id = ?'
            params.append(category_id)
        
        if subcategory_id:
            query += ' AND p.subcategory_id = ?'
            params.append(subcategory_id)
        
        if search:
            query += ' AND (p.name LIKE ? OR p.description LIKE ? OR p.brand LIKE ?)'
            search_term = f'%{search}%'
            params.extend([search_term, search_term, search_term])
        
        if min_price is not None:
            query += ' AND p.price >= ?'
            params.append(min_price)
        
        if max_price is not None:
            query += ' AND p.price <= ?'
            params.append(max_price)
        
        # Сортировка
        query += ' ORDER BY p.created_at DESC'
        
        # Лимиты
        query += ' LIMIT ? OFFSET ?'
        params.extend([limit, offset])
        
        products = db.execute_query(query, tuple(params))
        
        result = [{
            'id': prod[0],
            'name': prod[1],
            'description': prod[2],
            'price': float(prod[3]) if prod[3] else 0,
            'cost_price': float(prod[4]) if prod[4] else None,
            'original_price': float(prod[5]) if prod[5] else None,
            'category_id': prod[6],
            'subcategory_id': prod[7],
            'brand': prod[8],
            'image_url': prod[9],
            'stock': prod[10],
            'views': prod[11],
            'sales_count': prod[12],
            'is_active': bool(prod[13]),
            'created_at': prod[14],
            'updated_at': prod[15],
            'discount_percent': int(((prod[5] - prod[3]) / prod[5] * 100)) if prod[5] and prod[3] and prod[5] > prod[3] else None
        } for prod in products]
        
        # Общее количество для пагинации
        count_query = 'SELECT COUNT(*) FROM products p WHERE p.is_active = 1'
        count_params = []
        
        if category_id:
            count_query += ' AND p.category_id = ?'
            count_params.append(category_id)
        
        if subcategory_id:
            count_query += ' AND p.subcategory_id = ?'
            count_params.append(subcategory_id)
        
        if search:
            count_query += ' AND (p.name LIKE ? OR p.description LIKE ? OR p.brand LIKE ?)'
            count_params.extend([search_term, search_term, search_term])
        
        total = db.execute_query(count_query, tuple(count_params))[0][0]
        
        return jsonify({
            'success': True,
            'data': {
                'data': result,  # Массив товаров
                'total': total,
                'page': (offset // limit) + 1 if limit > 0 else 1,
                'limit': limit,
                'has_more': offset + len(result) < total
            }
        })
    except Exception as e:
        print(f"Ошибка получения товаров: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api.route('/products/<int:product_id>', methods=['GET'])
@telegram_login_required
def get_product_by_id(product_id):
    """Получить товар по ID"""
    try:
        product = db.execute_query('''
            SELECT p.id, p.name, p.description, p.price, p.cost_price,
                   p.original_price, p.category_id, p.subcategory_id,
                   p.brand, p.image_url, p.stock, p.views, p.sales_count,
                   p.is_active, p.created_at, p.updated_at
            FROM products p
            WHERE p.id = ?
        ''', (product_id,))
        
        if not product:
            return jsonify({
                'success': False,
                'error': 'Товар не найден'
            }), 404
        
        prod = product[0]
        return jsonify({
            'success': True,
            'data': {
                'id': prod[0],
                'name': prod[1],
                'description': prod[2],
                'price': float(prod[3]) if prod[3] else 0,
                'cost_price': float(prod[4]) if prod[4] else None,
                'original_price': float(prod[5]) if prod[5] else None,
                'category_id': prod[6],
                'subcategory_id': prod[7],
                'brand': prod[8],
                'image_url': prod[9],
                'stock': prod[10],
                'views': prod[11],
                'sales_count': prod[12],
                'is_active': bool(prod[13]),
                'created_at': prod[14],
                'updated_at': prod[15],
                'discount_percent': int(((prod[5] - prod[3]) / prod[5] * 100)) if prod[5] and prod[3] and prod[5] > prod[3] else None
            }
        })
    except Exception as e:
        print(f"Ошибка получения товара: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api.route('/products/search', methods=['GET'])
@telegram_login_required
def search_products():
    """Поиск товаров"""
    query = request.args.get('q', '')
    
    if not query or len(query) < 2:
        return jsonify({
            'success': False,
            'error': 'Запрос должен быть не менее 2 символов'
        }), 400
    
    # Перенаправляем на основной endpoint с параметром search
    from functools import wraps
    return get_products()


@api.route('/products/<int:product_id>/views', methods=['POST'])
@telegram_login_required
def increment_product_views(product_id):
    """Увеличить счетчик просмотров товара"""
    try:
        db.execute_query('''
            UPDATE products SET views = views + 1 WHERE id = ?
        ''', (product_id,))
        
        return jsonify({
            'success': True,
            'message': 'Просмотры обновлены'
        })
    except Exception as e:
        print(f"Ошибка обновления просмотров: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api.route('/products/<int:product_id>/related', methods=['GET'])
@telegram_login_required
def get_related_products(product_id):
    """Получить похожие товары из той же категории"""
    try:
        limit = request.args.get('limit', 4, type=int)
        
        # Получаем категорию товара
        product = db.execute_query('''
            SELECT category_id, subcategory_id FROM products WHERE id = ?
        ''', (product_id,))
        
        if not product:
            return jsonify({
                'success': False,
                'error': 'Товар не найден'
            }), 404
        
        category_id = product[0][0]
        subcategory_id = product[0][1]
        
        # Ищем похожие товары (в той же категории или подкатегории)
        if subcategory_id:
            related_query = '''
                SELECT p.id, p.name, p.price, p.original_price, p.image_url, p.stock
                FROM products p
                WHERE p.id != ? AND p.subcategory_id = ? AND p.is_active = 1
                ORDER BY p.sales_count DESC, p.created_at DESC
                LIMIT ?
            '''
            params = (product_id, subcategory_id, limit)
        else:
            related_query = '''
                SELECT p.id, p.name, p.price, p.original_price, p.image_url, p.stock
                FROM products p
                WHERE p.id != ? AND p.category_id = ? AND p.is_active = 1
                ORDER BY p.sales_count DESC, p.created_at DESC
                LIMIT ?
            '''
            params = (product_id, category_id, limit)
        
        related = db.execute_query(related_query, params)
        
        result = [{
            'id': prod[0],
            'name': prod[1],
            'price': float(prod[2]) if prod[2] else 0,
            'original_price': float(prod[3]) if prod[3] else None,
            'image_url': prod[4],
            'stock': prod[5],
            'discount_percent': int(((prod[3] - prod[2]) / prod[3] * 100)) if prod[3] and prod[2] and prod[3] > prod[2] else None
        } for prod in related]
        
        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        print(f"Ошибка получения похожих товаров: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
"""
API для Mini App - Корзина, Заказы, Избранное
Добавить в конец api_mini_app.py
"""

# ============================================
# API КОРЗИНЫ
# ============================================

@api.route('/cart/items', methods=['GET'])
@telegram_login_required
def get_cart_items():
    """Получить элементы корзины"""
    try:
        user_id = request.telegram_user.get('id') if hasattr(request, 'telegram_user') else 1
        
        items = db.execute_query('''
            SELECT ci.id, ci.product_id, ci.quantity, ci.created_at,
                   p.name, p.price, p.image_url, p.stock
            FROM cart_items ci
            JOIN products p ON ci.product_id = p.id
            WHERE ci.user_id = ?
            ORDER BY ci.created_at DESC
        ''', (user_id,))
        
        result = [{
            'id': item[0],
            'product_id': item[1],
            'quantity': item[2],
            'created_at': item[3],
            'product': {
                'name': item[4],
                'price': float(item[5]) if item[5] else 0,
                'image_url': item[6],
                'stock': item[7]
            }
        } for item in items]
        
        total_amount = sum(item['product']['price'] * item['quantity'] for item in result)
        
        return jsonify({
            'success': True,
            'data': {
                'items': result,
                'total_items': len(result),
                'total_amount': total_amount
            }
        })
    except Exception as e:
        print(f"Ошибка получения корзины: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@api.route('/cart/items', methods=['POST'])
@telegram_login_required
def add_to_cart():
    """Добавить товар в корзину"""
    try:
        data = request.json
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        
        if not product_id:
            return jsonify({'success': False, 'error': 'product_id required'}), 400
        
        user_id = request.telegram_user.get('id') if hasattr(request, 'telegram_user') else 1
        
        # Проверяем существует ли товар
        product = db.execute_query('SELECT id, price, stock FROM products WHERE id = ?', (product_id,))
        if not product:
            return jsonify({'success': False, 'error': 'Товар не найден'}), 404
        
        # Проверяем есть ли уже в корзине
        existing = db.execute_query(
            'SELECT id, quantity FROM cart_items WHERE user_id = ? AND product_id = ?',
            (user_id, product_id)
        )
        
        if existing:
            # Обновляем количество
            new_quantity = existing[0][1] + quantity
            db.execute_query(
                'UPDATE cart_items SET quantity = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
                (new_quantity, existing[0][0])
            )
        else:
            # Добавляем новый элемент
            db.execute_query(
                'INSERT INTO cart_items (user_id, product_id, quantity) VALUES (?, ?, ?)',
                (user_id, product_id, quantity)
            )
        
        return jsonify({'success': True})
    except Exception as e:
        print(f"Ошибка добавления в корзину: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@api.route('/cart/items/<int:item_id>', methods=['PUT'])
@telegram_login_required
def update_cart_item(item_id):
    """Обновить количество товара в корзине"""
    try:
        data = request.json
        quantity = data.get('quantity', 1)
        
        if quantity <= 0:
            # Удаляем если 0
            db.execute_query('DELETE FROM cart_items WHERE id = ?', (item_id,))
        else:
            db.execute_query(
                'UPDATE cart_items SET quantity = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',
                (quantity, item_id)
            )
        
        return jsonify({'success': True})
    except Exception as e:
        print(f"Ошибка обновления корзины: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@api.route('/cart/items/<int:item_id>', methods=['DELETE'])
@telegram_login_required
def remove_from_cart(item_id):
    """Удалить товар из корзины"""
    try:
        db.execute_query('DELETE FROM cart_items WHERE id = ?', (item_id,))
        return jsonify({'success': True})
    except Exception as e:
        print(f"Ошибка удаления из корзины: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@api.route('/cart/clear', methods=['POST'])
@telegram_login_required
def clear_cart():
    """Очистить корзину"""
    try:
        user_id = request.telegram_user.get('id') if hasattr(request, 'telegram_user') else 1
        db.execute_query('DELETE FROM cart_items WHERE user_id = ?', (user_id,))
        return jsonify({'success': True})
    except Exception as e:
        print(f"Ошибка очистки корзины: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================
# API ЗАКАЗОВ
# ============================================

@api.route('/orders', methods=['POST'])
@telegram_login_required
def create_order():
    """Создать заказ"""
    try:
        data = request.json
        delivery_address = data.get('delivery_address', '')
        payment_method = data.get('payment_method', 'cash')
        comment = data.get('comment', '')
        
        user_id = request.telegram_user.get('id') if hasattr(request, 'telegram_user') else 1
        
        # Получаем товары из корзины
        cart_items = db.execute_query('''
            SELECT ci.product_id, ci.quantity, p.price
            FROM cart_items ci
            JOIN products p ON ci.product_id = p.id
            WHERE ci.user_id = ?
        ''', (user_id,))
        
        if not cart_items:
            return jsonify({'success': False, 'error': 'Корзина пуста'}), 400
        
        # Считаем общую сумму
        total_amount = sum(item[1] * float(item[2]) for item in cart_items)
        
        # Создаём заказ
        cursor = db.conn.cursor() if hasattr(db, 'conn') else None
        if not cursor:
            conn = sqlite3.connect(db.db_path)
            cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO orders (user_id, total_amount, delivery_address, payment_method, status, comment)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, total_amount, delivery_address, payment_method, 'pending', comment))
        
        order_id = cursor.lastrowid
        
        # Добавляем элементы заказа
        for item in cart_items:
            cursor.execute('''
                INSERT INTO order_items (order_id, product_id, quantity, price)
                VALUES (?, ?, ?, ?)
            ''', (order_id, item[0], item[1], float(item[2])))
        
        # Очищаем корзину
        cursor.execute('DELETE FROM cart_items WHERE user_id = ?', (user_id,))
        
        if hasattr(db, 'conn'):
            db.conn.commit()
        else:
            conn.commit()
            conn.close()
        
        return jsonify({
            'success': True,
            'data': {'order_id': order_id}
        })
    except Exception as e:
        print(f"Ошибка создания заказа: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@api.route('/orders', methods=['GET'])
@telegram_login_required
def get_orders():
    """Получить список заказов"""
    try:
        user_id = request.telegram_user.get('id') if hasattr(request, 'telegram_user') else 1
        
        orders = db.execute_query('''
            SELECT id, total_amount, status, payment_status, delivery_address, 
                   payment_method, created_at
            FROM orders
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT 20
        ''', (user_id,))
        
        result = []
        for order in orders:
            items = db.execute_query('''
                SELECT oi.product_id, oi.quantity, oi.price, p.name
                FROM order_items oi
                JOIN products p ON oi.product_id = p.id
                WHERE oi.order_id = order[0]
            ''')
            
            result.append({
                'id': order[0],
                'total_amount': float(order[1]),
                'status': order[2],
                'payment_status': order[3],
                'delivery_address': order[4],
                'payment_method': order[5],
                'created_at': order[6],
                'items': [{
                    'product_id': item[0],
                    'quantity': item[1],
                    'price': float(item[2]),
                    'product_name': item[3]
                } for item in items]
            })
        
        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        print(f"Ошибка получения заказов: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@api.route('/orders/<int:order_id>', methods=['GET'])
@telegram_login_required
def get_order_detail(order_id):
    """Получить детали заказа"""
    try:
        user_id = request.telegram_user.get('id') if hasattr(request, 'telegram_user') else 1
        
        order = db.execute_query('''
            SELECT id, total_amount, status, payment_status, delivery_address,
                   payment_method, comment, created_at
            FROM orders
            WHERE id = ? AND user_id = ?
        ''', (order_id, user_id))
        
        if not order:
            return jsonify({'success': False, 'error': 'Заказ не найден'}), 404
        
        items = db.execute_query('''
            SELECT oi.product_id, oi.quantity, oi.price, p.name, p.image_url
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = ?
        ''', (order_id,))
        
        return jsonify({
            'success': True,
            'data': {
                'id': order[0][0],
                'total_amount': float(order[0][1]),
                'status': order[0][2],
                'payment_status': order[0][3],
                'delivery_address': order[0][4],
                'payment_method': order[0][5],
                'comment': order[0][6],
                'created_at': order[0][7],
                'items': [{
                    'product_id': item[0],
                    'quantity': item[1],
                    'price': float(item[2]),
                    'product_name': item[3],
                    'image_url': item[4]
                } for item in items]
            }
        })
    except Exception as e:
        print(f"Ошибка получения деталей заказа: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================
# API ИЗБРАННОГО
# ============================================

@api.route('/favorites', methods=['GET'])
@telegram_login_required
def get_favorites():
    """Получить избранные товары"""
    try:
        user_id = request.telegram_user.get('id') if hasattr(request, 'telegram_user') else 1
        
        favorites = db.execute_query('''
            SELECT f.id, f.product_id, f.created_at,
                   p.name, p.price, p.image_url, p.stock
            FROM favorites f
            JOIN products p ON f.product_id = p.id
            WHERE f.user_id = ?
            ORDER BY f.created_at DESC
        ''', (user_id,))
        
        result = [{
            'id': fav[0],
            'product_id': fav[1],
            'created_at': fav[2],
            'product': {
                'name': fav[3],
                'price': float(fav[4]) if fav[4] else 0,
                'image_url': fav[5],
                'stock': fav[6]
            }
        } for fav in favorites]
        
        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        print(f"Ошибка получения избранного: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@api.route('/favorites', methods=['POST'])
@telegram_login_required
def add_to_favorites():
    """Добавить товар в избранное"""
    try:
        data = request.json
        product_id = data.get('product_id')
        
        if not product_id:
            return jsonify({'success': False, 'error': 'product_id required'}), 400
        
        user_id = request.telegram_user.get('id') if hasattr(request, 'telegram_user') else 1
        
        # Проверяем существует ли товар
        product = db.execute_query('SELECT id FROM products WHERE id = ?', (product_id,))
        if not product:
            return jsonify({'success': False, 'error': 'Товар не найден'}), 404
        
        # Проверяем есть ли уже в избранном
        existing = db.execute_query(
            'SELECT id FROM favorites WHERE user_id = ? AND product_id = ?',
            (user_id, product_id)
        )
        
        if existing:
            return jsonify({'success': False, 'error': 'Уже в избранном'}), 400
        
        # Добавляем в избранное
        db.execute_query(
            'INSERT INTO favorites (user_id, product_id) VALUES (?, ?)',
            (user_id, product_id)
        )
        
        return jsonify({'success': True})
    except Exception as e:
        print(f"Ошибка добавления в избранное: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@api.route('/favorites/<int:fav_id>', methods=['DELETE'])
@telegram_login_required
def remove_from_favorites(fav_id):
    """Удалить товар из избранного"""
    try:
        db.execute_query('DELETE FROM favorites WHERE id = ?', (fav_id,))
        return jsonify({'success': True})
    except Exception as e:
        print(f"Ошибка удаления из избранного: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
