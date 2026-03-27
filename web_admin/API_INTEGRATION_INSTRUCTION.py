"""
Интеграция REST API для Telegram Mini App в основной app.py

Добавь этот код ПОСЛЕ строки:
    telegram_bot = TelegramBotIntegration()

ПЕРЕД строкой:
    # Настройки загрузки файлов
"""

# ============================================
# ИНТЕГРАЦИЯ TELEGRAM MINI APP API
# ============================================

# Импортируем и инициализируем API
from api_mini_app import init_api, api

# Инициализируем API с базой данных и приложением
init_api(db, app)

# Регистрируем Blueprint API
app.register_blueprint(api)

print("✅ Telegram Mini App API успешно подключено!")
print("📡 Доступные endpoints:")
print("   GET  /api/categories - Список категорий")
print("   GET  /api/products - Список товаров")
print("   GET  /api/cart - Корзина пользователя")
print("   POST /api/cart - Добавить в корзину")
print("   GET  /api/orders - История заказов")
print("   POST /api/orders - Создать заказ")
print("   GET  /api/favorites - Избранное")
print("")
