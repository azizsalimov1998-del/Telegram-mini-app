import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Trash2, Plus, Minus, ChevronRight } from 'lucide-react';
import { Header } from '../components/Header';
import { EmptyState } from '../components/EmptyState';
import { useCartStore } from '../store/cartStore';
import { TelegramButtons } from '../lib/telegram';

/**
 * Страница корзины
 */
export function Cart() {
  const navigate = useNavigate();
  const { items, totalAmount, totalItems, updateQuantity, removeFromCart, clearCart } = useCartStore();
  const [isEditing, setIsEditing] = useState(false);

  // Форматирование цены
  function formatPrice(price: number): string {
    return price.toLocaleString('ru-RU');
  }

  // Обработчик оформления заказа
  function handleCheckout() {
    navigate('/checkout', { 
      state: { 
        totalAmount, 
        items 
      } 
    });
  }

  // Показываем кнопку очистки если товаров много
  if (items.length > 3 && !isEditing) {
    TelegramButtons.showMainButton(
      `Оформить заказ • ${formatPrice(totalAmount)} сум`,
      handleCheckout
    );
  } else {
    TelegramButtons.hideMainButton();
  }

  if (items.length === 0) {
    return (
      <div className="min-h-screen bg-[var(--tg-theme-bg-color)]">
        <Header title="Корзина" />
        <EmptyState
          type="cart"
          action={
            <button
              onClick={() => navigate('/')}
              className="bg-[var(--tg-theme-button-color)] text-[var(--tg-theme-button-text-color)] px-6 py-3 rounded-lg font-medium hover:opacity-90 transition-opacity"
            >
              Перейти в каталог
            </button>
          }
        />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[var(--tg-theme-bg-color)] pb-40">
      <Header 
        title={`Корзина (${totalItems})`}
        rightElement={
          items.length > 0 && (
            <button
              onClick={() => setIsEditing(!isEditing)}
              className={`px-3 py-2 rounded-lg text-sm font-medium ${
                isEditing
                  ? 'bg-[var(--tg-theme-button-color)] text-[var(--tg-theme-button-text-color)]'
                  : 'bg-[var(--tg-theme-secondary-bg-color)] text-[var(--tg-theme-text-color)]'
              }`}
            >
              {isEditing ? 'Готово' : 'Изменить'}
            </button>
          )
        }
      />

      <main className="p-4 space-y-3">
        {/* Список товаров */}
        {items.map((item) => (
          <div
            key={item.id}
            className="flex gap-3 bg-[var(--tg-theme-secondary-bg-color)] rounded-lg p-3"
          >
            {/* Изображение товара */}
            <div className="w-24 h-24 bg-[var(--tg-theme-bg-color)] rounded-md flex-shrink-0 overflow-hidden">
              {item.product?.image_url ? (
                <img
                  src={item.product.image_url}
                  alt={item.product.name}
                  className="w-full h-full object-cover"
                />
              ) : (
                <div className="flex items-center justify-center h-full text-2xl">
                  📦
                </div>
              )}
            </div>

            {/* Информация о товаре */}
            <div className="flex-1 min-w-0 flex flex-col">
              <h3 className="font-medium text-[var(--tg-theme-text-color)] truncate mb-1">
                {item.product?.name || 'Товар'}
              </h3>
              <p className="text-sm text-[var(--tg-theme-hint-color)] mb-2">
                {formatPrice(item.product?.price || 0)} сум/шт
              </p>

              {/* Количество и цена */}
              <div className="flex items-center justify-between mt-auto">
                {isEditing ? (
                  <button
                    onClick={() => removeFromCart(item.id!)}
                    className="flex items-center gap-1 text-red-500 text-sm font-medium"
                  >
                    <Trash2 size={16} />
                    Удалить
                  </button>
                ) : (
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => updateQuantity(item.id!, item.quantity - 1)}
                      className="w-8 h-8 rounded-full bg-[var(--tg-theme-bg-color)] flex items-center justify-center text-[var(--tg-theme-text-color)] hover:bg-[var(--tg-theme-hint-color)]/20"
                    >
                      <Minus size={16} />
                    </button>
                    <span className="w-8 text-center font-semibold text-[var(--tg-theme-text-color)]">
                      {item.quantity}
                    </span>
                    <button
                      onClick={() => updateQuantity(item.id!, item.quantity + 1)}
                      className="w-8 h-8 rounded-full bg-[var(--tg-theme-bg-color)] flex items-center justify-center text-[var(--tg-theme-text-color)] hover:bg-[var(--tg-theme-hint-color)]/20"
                    >
                      <Plus size={16} />
                    </button>
                  </div>
                )}

                <span className="font-bold text-[var(--tg-theme-text-color)]">
                  {formatPrice((item.product?.price || 0) * item.quantity)} сум
                </span>
              </div>
            </div>
          </div>
        ))}

        {/* Кнопка очистки всей корзины */}
        {isEditing && (
          <button
            onClick={() => {
              if (confirm('Вы уверены, что хотите очистить корзину?')) {
                clearCart();
                setIsEditing(false);
              }
            }}
            className="w-full border-2 border-red-500 text-red-500 py-3 rounded-lg font-medium hover:bg-red-500/10 transition-colors"
          >
            Очистить всю корзину
          </button>
        )}
      </main>

      {/* Итоговая панель */}
      <div className="fixed bottom-0 left-0 right-0 bg-[var(--tg-theme-bg-color)] border-t border-[var(--tg-theme-secondary-bg-color)] p-4 pb-6">
        <div className="max-w-lg mx-auto space-y-3">
          {/* Детали суммы */}
          <div className="flex items-center justify-between text-sm">
            <span className="text-[var(--tg-theme-hint-color)]">Товары ({totalItems}):</span>
            <span className="text-[var(--tg-theme-text-color)]">{formatPrice(totalAmount)} сум</span>
          </div>
          <div className="flex items-center justify-between text-sm">
            <span className="text-[var(--tg-theme-hint-color)]">Доставка:</span>
            <span className="text-green-600">Бесплатно</span>
          </div>
          
          {/* Общая сумма */}
          <div className="flex items-center justify-between pt-3 border-t border-[var(--tg-theme-secondary-bg-color)]">
            <span className="text-lg font-semibold text-[var(--tg-theme-text-color)]">Итого:</span>
            <span className="text-2xl font-bold text-[var(--tg-theme-text-color)]">
              {formatPrice(totalAmount)} сум
            </span>
          </div>

          {/* Кнопка оформления */}
          <button
            onClick={handleCheckout}
            className="w-full bg-[var(--tg-theme-button-color)] text-[var(--tg-theme-button-text-color)] py-4 rounded-lg font-semibold text-lg hover:opacity-90 transition-opacity flex items-center justify-between px-6"
          >
            <span>Оформить заказ</span>
            <ChevronRight size={24} />
          </button>
        </div>
      </div>
    </div>
  );
}
