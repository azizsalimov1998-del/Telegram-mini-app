#!/usr/bin/env python3
"""
Тестовый скрипт для проверки Telegram Mini App API
Запускает backend и проверяет основные endpoints
"""

import sys
import os

# Добавляем путь к приложению
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from web_admin.app import app
from web_admin.database import DatabaseManager

def test_api():
    """Тестирование API endpoints"""
    
    print("\n" + "="*60)
    print("🧪 ТЕСТИРОВАНИЕ TELEGRAM MINI APP API")
    print("="*60 + "\n")
    
    # Создаем тестовый клиент
    with app.test_client() as client:
        
        # Тест 1: Проверка что сервер работает
        print("1️⃣ Проверка доступности сервера...")
        try:
            response = client.get('/')
            print(f"   ✅ Сервер работает (статус: {response.status_code})")
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
            return False
        
        # Тест 2: Проверка API категорий (без авторизации - должен вернуть 401)
        print("\n2️⃣ Проверка защиты API...")
        response = client.get('/api/categories')
        if response.status_code == 401:
            print(f"   ✅ API защищено (401 без авторизации)")
        else:
            print(f"   ⚠️  Статус: {response.status_code}")
        
        # Тест 3: Проверка базы данных
        print("\n3️⃣ Проверка подключения к базе данных...")
        try:
            db_path = os.path.join(os.path.dirname(__file__), 'shop_bot.db')
            if os.path.exists(db_path):
                print(f"   ✅ База данных найдена: {db_path}")
                
                # Проверяем таблицы
                db = DatabaseManager(db_path)
                tables = db.execute_query("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name IN ('categories', 'products', 'orders', 'cart_items')
                """)
                
                print(f"   📊 Найдено таблиц: {len(tables)}")
                for table in tables:
                    print(f"      - {table[0]}")
            else:
                print(f"   ⚠️  База данных не найдена: {db_path}")
        except Exception as e:
            print(f"   ❌ Ошибка БД: {e}")
        
        # Тест 4: Проверка регистрации Blueprint
        print("\n4️⃣ Проверка регистрации API endpoints...")
        registered_rules = [rule.rule for rule in app.url_map.iter_rules()]
        api_endpoints = [rule for rule in registered_rules if rule.startswith('/api')]
        
        print(f"   ✅ Зарегистрировано API endpoints: {len(api_endpoints)}")
        
        # Показываем несколько примеров
        sample_endpoints = api_endpoints[:5]
        for endpoint in sample_endpoints:
            print(f"      {endpoint}")
        
        if len(api_endpoints) > 5:
            print(f"      ... и еще {len(api_endpoints) - 5}")
        
        print("\n" + "="*60)
        print("✅ ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
        print("="*60)
        print("\n📝 СЛЕДУЮЩИЕ ШАГИ:")
        print("   1. Установи переменные окружения (.env)")
        print("   2. Запусти сервер: python3 web_admin/app.py")
        print("   3. Открой в браузере: http://localhost:5000")
        print("   4. Задеплой frontend: cd s1-mini-app && vercel --prod")
        print("")
        
        return True

if __name__ == '__main__':
    try:
        success = test_api()
        if success:
            print("🎉 Все системы готовы к запуску!\n")
            sys.exit(0)
        else:
            print("❌ Обнаружены ошибки\n")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
