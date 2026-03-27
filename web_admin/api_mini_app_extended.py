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
