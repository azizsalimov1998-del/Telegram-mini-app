import { X, Plus, Minus, Trash2, ShoppingBag } from 'lucide-react';
import { useCartStore } from '../store/cartStore';
import { useEffect } from 'react';

interface CartDrawerProps {
  isOpen: boolean;
  onClose: () => void;
}

/**
 * Выезжающая корзина (шторка)
 */
export function CartDrawer({ isOpen, onClose }: CartDrawerProps) {
  const { items, totalAmount, totalItems, updateQuantity, removeFromCart, fetchCart } = useCartStore();

  // Загружаем корзину при открытии
  useEffect(() => {
    if (isOpen && items.length === 0) {
      fetchCart();
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <>
      {/* Затемнение фона */}
      <div
        className="fixed inset-0 bg-black/50 z-40"
        onClick={onClose}
      />

      {/* Шторка корзины */}
      <div className="fixed bottom-0 left-0 right-0 bg-[var(--tg-theme-bg-color)] rounded-t-2xl z-50 max-h-[80vh] flex flex-col animate-slide-up">
        {/* Заголовок */}
        <div className="flex items-center justify-between p-4 border-b border-[var(--tg-theme-secondary-bg-color)]">
          <h2 className="text-lg font-bold text-[var(--tg-theme-text-color)] flex items-center gap-2">
            <ShoppingBag size={24} />
            Корзина ({totalItems})
          </h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-[var(--tg-theme-secondary-bg-color)] rounded-full transition-colors"
          >
            <X size={24} className="text-[var(--tg-theme-text-color)]" />
          </button>
        </div>

        {/* Список товаров */}
        <div className="flex-1 overflow-y-auto p-4 space-y-3">
          {items.length > 0 ? (
            items.map((item) => (
              <div
                key={item.id}
                className="flex gap-3 bg-[var(--tg-theme-secondary-bg-color)] rounded-lg p-3"
              >
                {/* Изображение товара */}
                <div className="w-20 h-20 bg-[var(--tg-theme-bg-color)] rounded-md flex-shrink-0 overflow-hidden">
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
                <div className="flex-1 min-w-0">
                  <h3 className="font-medium text-[var(--tg-theme-text-color)] truncate mb-1">
                    {item.product?.name || 'Товар'}
                  </h3>
                  <p className="text-sm text-[var(--tg-theme-hint-color)] mb-2">
                    {item.product?.price.toLocaleString('ru-RU')} сум/шт
                  </p>

                  {/* Количество и удаление */}
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => updateQuantity(item.id!, item.quantity - 1)}
                        className="p-1 bg-[var(--tg-theme-bg-color)] rounded hover:bg-[var(--tg-theme-hint-color)]/20"
                      >
                        <Minus size={16} className="text-[var(--tg-theme-text-color)]" />
                      </button>
                      <span className="w-8 text-center font-medium text-[var(--tg-theme-text-color)]">
                        {item.quantity}
                      </span>
                      <button
                        onClick={() => updateQuantity(item.id!, item.quantity + 1)}
                        className="p-1 bg-[var(--tg-theme-bg-color)] rounded hover:bg-[var(--tg-theme-hint-color)]/20"
                      >
                        <Plus size={16} className="text-[var(--tg-theme-text-color)]" />
                      </button>
                    </div>

                    <button
                      onClick={() => removeFromCart(item.id!)}
                      className="p-2 text-red-500 hover:bg-red-500/10 rounded transition-colors"
                    >
                      <Trash2 size={18} />
                    </button>
                  </div>
                </div>
              </div>
            ))
          ) : (
            <div className="text-center text-[var(--tg-theme-hint-color)] py-12">
              <ShoppingBag size={48} className="mx-auto mb-3 opacity-50" />
              <p className="text-lg">Корзина пуста</p>
              <p className="text-sm mt-1">Добавьте товары из каталога</p>
            </div>
          )}
        </div>

        {/* Итого и кнопка оформления */}
        {items.length > 0 && (
          <div className="border-t border-[var(--tg-theme-secondary-bg-color)] p-4 space-y-3">
            {/* Сумма */}
            <div className="flex items-center justify-between">
              <span className="text-[var(--tg-theme-text-color)]">Итого:</span>
              <span className="text-xl font-bold text-[var(--tg-theme-text-color)]">
                {totalAmount.toLocaleString('ru-RU')} сум
              </span>
            </div>

            {/* Кнопка оформления */}
            <button
              onClick={() => {
                onClose();
                // Переход к оформлению будет добавлен позже
              }}
              className="w-full bg-[var(--tg-theme-button-color)] text-[var(--tg-theme-button-text-color)] py-4 rounded-lg font-semibold text-lg hover:opacity-90 transition-opacity"
            >
              Оформить заказ
            </button>
          </div>
        )}
      </div>
    </>
  );
}
