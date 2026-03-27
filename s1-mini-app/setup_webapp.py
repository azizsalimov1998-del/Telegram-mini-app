#!/usr/bin/env python3
"""
Скрипт для настройки Telegram Web App кнопки для S1 Mini App

Использование:
    python setup_webapp.py https://your-app.vercel.app

Или оставь пустым для использования URL по умолчанию
"""

import os
import sys
import asyncio
from pathlib import Path

# Добавляем путь к проекту
sys.path.insert(0, str(Path(__file__).parent))

try:
    from telegram import Bot
    from telegram.types import WebAppInfo, MenuButtonWebApp
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False
    print("❌ Библиотека python-telegram-bot не найдена!")
    print("Установите: pip install python-telegram-bot>=20.0")
    sys.exit(1)

from config import BOT_TOKEN


async def setup_webapp(webapp_url: str = None):
    """
    Настраивает Web App кнопку в боте
    
    Args:
        webapp_url: URL Telegram Mini App (по умолчанию запросит у пользователя)
    """
    
    # Запрашиваем URL если не передан
    if not webapp_url:
        print("\n" + "="*60)
        print("🚀 Настройка Telegram Web App для S1 Mini App")
        print("="*60)
        print("\nВведите URL вашего Mini App на Vercel:")
        print("(например: https://s1-mini-app.vercel.app)")
        print()
        webapp_url = input("URL: ").strip()
        
        if not webapp_url:
            print("❌ URL не может быть пустым!")
            return False
        
        # Добавляем https если нет
        if not webapp_url.startswith('http'):
            webapp_url = f'https://{webapp_url}'
    
    # Валидация URL
    if not webapp_url.startswith(('http://', 'https://')):
        print("❌ Неверный формат URL!")
        return False
    
    print(f"\n🔧 Настройка Web App...")
    print(f"URL: {webapp_url}")
    
    try:
        # Создаем бота
        bot = Bot(token=BOT_TOKEN)
        
        # Устанавливаем кнопку меню
        print("\n📱 Установка кнопки меню...")
        await bot.set_chat_menu_button(
            menu_button=MenuButtonWebApp(
                text="🛍️ Открыть магазин",
                web_app=WebAppInfo(url=webapp_url)
            )
        )
        print("✅ Кнопка меню успешно установлена!")
        
        # Обновляем описание бота
        print("\n📝 Обновление описания бота...")
        await bot.set_my_description(
            description=f"S1 - Интернет-магазин\n\n🛍️ Откройте магазин прямо в Telegram!\n\nНажмите на кнопку меню слева, чтобы начать покупки."
        )
        print("✅ Описание обновлено!")
        
        # Получаем информацию о боте для проверки
        me = await bot.get_me()
        print(f"\n✨ Готово!")
        print(f"Бот: @{me.username}")
        print(f"Web App URL: {webapp_url}")
        print("\n" + "="*60)
        print("📋 Следующие шаги:")
        print("1. Откройте своего бота в Telegram")
        print("2. Нажмите на кнопку меню слева внизу")
        print("3. Ваше Mini App должно открыться!")
        print("="*60)
        
        await bot.close()
        return True
        
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        print("\nВозможные причины:")
        print("- Неверный токен бота (проверьте в .env или config.py)")
        print("- Недоступен Telegram API (проверьте интернет)")
        print("- Неверный формат URL")
        return False


def main():
    """Точка входа"""
    
    # Проверяем наличие токена
    if not BOT_TOKEN:
        print("❌ Токен бота не найден!")
        print("Проверьте файл config.py или переменную окружения BOT_TOKEN")
        sys.exit(1)
    
    # Получаем URL из аргументов командной строки
    webapp_url = sys.argv[1] if len(sys.argv) > 1 else None
    
    # Если есть .env файл с URL, используем его
    env_file = Path(__file__).parent / '.env'
    if env_file.exists() and not webapp_url:
        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith('S1_WEBAPP_URL='):
                        webapp_url = line.split('=')[1].strip().strip('"\'')
                        print(f"✅ Найден URL в .env: {webapp_url}")
                        break
        except Exception:
            pass
    
    # Запускаем настройку
    success = asyncio.run(setup_webapp(webapp_url))
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
