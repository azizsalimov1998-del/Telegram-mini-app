import { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { MapPin, CreditCard, Truck } from 'lucide-react';
import { Header } from '../components/Header';
import { createOrder } from '../services/orders';
import { useCartStore } from '../store/cartStore';
import { TelegramButtons } from '../lib/telegram';

/**
 * Страница оформления заказа
 */
export function Checkout() {
  const navigate = useNavigate();
  const location = useLocation();
  const { clearCart } = useCartStore();
  
  const { totalAmount, items } = location.state || { totalAmount: 0, items: [] };
  
  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    address: '',
    payment_method: 'cash',
    comment: '',
  });
  
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Если корзина пуста, возвращаемся назад
  if (items.length === 0) {
    navigate('/cart');
    return null;
  }

  // Обработчик отправки формы
  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      // Создаем заказ
      await createOrder({
        delivery_address: formData.address,
        payment_method: formData.payment_method,
      });

      // Очищаем корзину
      clearCart();

      // Показываем успех и переходим к заказам
      alert('✅ Заказ успешно оформлен!');
      navigate('/orders');
    } catch (error) {
      console.error('Ошибка оформления заказа:', error);
      alert('❌ Ошибка при оформлении заказа. Попробуйте еще раз.');
    } finally {
      setIsSubmitting(false);
    }
  }

  // Скрываем главную кнопку при загрузке
  TelegramButtons.hideMainButton();

  // Форматирование цены
  function formatPrice(price: number): string {
    return price.toLocaleString('ru-RU');
  }

  return (
    <div className="min-h-screen bg-[var(--tg-theme-bg-color)] pb-40">
      <Header title="Оформление заказа" showBackButton />

      <form onSubmit={handleSubmit} className="p-4 space-y-6">
        {/* Контактная информация */}
        <section>
          <h2 className="text-lg font-semibold text-[var(--tg-theme-text-color)] mb-4 flex items-center gap-2">
            <MapPin size={20} />
            Контактная информация
          </h2>
          
          <div className="space-y-3">
            <div>
              <label className="block text-sm font-medium text-[var(--tg-theme-text-color)] mb-1">
                Имя *
              </label>
              <input
                type="text"
                required
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className="w-full bg-[var(--tg-theme-secondary-bg-color)] text-[var(--tg-theme-text-color)] px-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-[var(--tg-theme-button-color)]"
                placeholder="Ваше имя"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-[var(--tg-theme-text-color)] mb-1">
                Телефон *
              </label>
              <input
                type="tel"
                required
                value={formData.phone}
                onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                className="w-full bg-[var(--tg-theme-secondary-bg-color)] text-[var(--tg-theme-text-color)] px-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-[var(--tg-theme-button-color)]"
                placeholder="+998 90 123 45 67"
              />
            </div>
          </div>
        </section>

        {/* Адрес доставки */}
        <section>
          <h2 className="text-lg font-semibold text-[var(--tg-theme-text-color)] mb-4 flex items-center gap-2">
            <Truck size={20} />
            Адрес доставки
          </h2>
          
          <div>
            <label className="block text-sm font-medium text-[var(--tg-theme-text-color)] mb-1">
              Полный адрес *
            </label>
            <textarea
              required
              value={formData.address}
              onChange={(e) => setFormData({ ...formData, address: e.target.value })}
              className="w-full bg-[var(--tg-theme-secondary-bg-color)] text-[var(--tg-theme-text-color)] px-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-[var(--tg-theme-button-color)] resize-none"
              rows={3}
              placeholder="Город, улица, дом, квартира"
            />
          </div>
        </section>

        {/* Способ оплаты */}
        <section>
          <h2 className="text-lg font-semibold text-[var(--tg-theme-text-color)] mb-4 flex items-center gap-2">
            <CreditCard size={20} />
            Способ оплаты
          </h2>
          
          <div className="space-y-2">
            {[
              { value: 'cash', label: 'Наличными при получении' },
              { value: 'payme', label: 'Payme' },
              { value: 'click', label: 'Click' },
              { value: 'card', label: 'Банковской картой' },
            ].map((method) => (
              <label
                key={method.value}
                className="flex items-center gap-3 p-3 bg-[var(--tg-theme-secondary-bg-color)] rounded-lg cursor-pointer hover:bg-[var(--tg-theme-hint-color)]/20 transition-colors"
              >
                <input
                  type="radio"
                  name="payment_method"
                  value={method.value}
                  checked={formData.payment_method === method.value}
                  onChange={(e) => setFormData({ ...formData, payment_method: e.target.value })}
                  className="w-4 h-4 text-[var(--tg-theme-button-color)]"
                />
                <span className="text-[var(--tg-theme-text-color)]">{method.label}</span>
              </label>
            ))}
          </div>
        </section>

        {/* Комментарий к заказу */}
        <section>
          <h2 className="text-lg font-semibold text-[var(--tg-theme-text-color)] mb-4">
            Комментарий к заказу
          </h2>
          
          <div>
            <textarea
              value={formData.comment}
              onChange={(e) => setFormData({ ...formData, comment: e.target.value })}
              className="w-full bg-[var(--tg-theme-secondary-bg-color)] text-[var(--tg-theme-text-color)] px-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-[var(--tg-theme-button-color)] resize-none"
              rows={3}
              placeholder="Дополнительная информация для курьера"
            />
          </div>
        </section>

        {/* Итоговая информация */}
        <div className="bg-[var(--tg-theme-secondary-bg-color)] rounded-lg p-4 space-y-2">
          <div className="flex items-center justify-between text-sm">
            <span className="text-[var(--tg-theme-hint-color)]">Товары ({items.length}):</span>
            <span className="text-[var(--tg-theme-text-color)]">{formatPrice(totalAmount)} сум</span>
          </div>
          <div className="flex items-center justify-between text-sm">
            <span className="text-[var(--tg-theme-hint-color)]">Доставка:</span>
            <span className="text-green-600">Бесплатно</span>
          </div>
          <div className="pt-2 border-t border-[var(--tg-theme-hint-color)]/20">
            <div className="flex items-center justify-between">
              <span className="font-semibold text-[var(--tg-theme-text-color)]">Итого к оплате:</span>
              <span className="text-xl font-bold text-[var(--tg-theme-button-color)]">
                {formatPrice(totalAmount)} сум
              </span>
            </div>
          </div>
        </div>

        {/* Кнопка подтверждения */}
        <button
          type="submit"
          disabled={isSubmitting}
          className={`w-full py-4 rounded-lg font-semibold text-lg transition-opacity ${
            isSubmitting
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-[var(--tg-theme-button-color)] text-[var(--tg-theme-button-text-color)] hover:opacity-90'
          }`}
        >
          {isSubmitting ? 'Оформление...' : `Подтвердить заказ • ${formatPrice(totalAmount)} сум`}
        </button>
      </form>
    </div>
  );
}
