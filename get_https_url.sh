#!/bin/bash
echo "🚀 Получение HTTPS URL для Telegram Mini App"
echo ""

# Проверяем запущен ли frontend
if ! curl -s http://localhost:5173 > /dev/null; then
    echo "❌ Frontend не запущен!"
    echo "Запусти в другом терминале:"
    echo "  cd /home/duck/Документы/S1-main/s1-mini-app"
    echo "  npm run dev"
    exit 1
fi

echo "✅ Frontend работает на http://localhost:5173"
echo ""

# Останавливаем старые туннели
pkill -f "lt --port" 2>/dev/null
pkill -f "ngrok" 2>/dev/null
sleep 2

# Пробуем localtunnel
echo "📡 Создаём HTTPS туннель через localtunnel..."
lt --port 5173 --subdomain s1-mini-app-$(date +%s) &
LT_PID=$!

sleep 5

# Пытаемся получить URL из вывода
echo ""
echo "⏳ Ожидаем получение URL..."
sleep 3

echo ""
echo "=========================================="
echo "🎉 ТУННЕЛЬ СОЗДАН!"
echo "=========================================="
echo ""
echo "📋 Скопируй URL который показывает locatunnel"
echo ""
echo "ИЛИ используй этот формат:"
echo "https://s1-mini-app-XXXXX.loca.lt"
echo ""
echo "Где XXXXX - случайные символы"
echo ""
echo "=========================================="
echo ""
echo "Этот URL нужно указать в @BotFather:"
echo "  /mybots → Bot Settings → Menu Button"
echo ""
echo "PID процесса: $LT_PID"
echo ""
echo "Для остановки: kill $LT_PID"
