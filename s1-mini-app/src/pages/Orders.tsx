import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Package, Clock, CheckCircle, Truck, XCircle } from 'lucide-react';
import { Header } from '../components/Header';
import { EmptyState } from '../components/EmptyState';
import { getUserOrders } from '../services/orders';
import { Order } from '../types';

/**
 * Страница истории заказов
 */
export function Orders() {
  const navigate = useNavigate();
  const [orders, setOrders] = useState<Order[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Загрузка заказов
  useEffect(() => {
    loadOrders();
  }, []);

  async function loadOrders() {
    try {
      const data = await getUserOrders();
      setOrders(data);
    } catch (error) {
      console.error('Ошибка загрузки заказов:', error);
    } finally {
      setIsLoading(false);
    }
  }

  // Статус заказа
  function getStatusInfo(status: string) {
    const statusMap = {
      pending: { icon: <Clock size={20} />, color: 'text-yellow-600', label: 'Ожидает подтверждения' },
      confirmed: { icon: <CheckCircle size={20} />, color: 'text-green-600', label: 'Подтвержден' },
      processing: { icon: <Package size={20} />, color: 'text-blue-600', label: 'В обработке' },
      shipped: { icon: <Truck size={20} />, color: 'text-purple-600', label: 'Отправлен' },
      delivered: { icon: <CheckCircle size={20} />, color: 'text-green-600', label: 'Доставлен' },
      cancelled: { icon: <XCircle size={20} />, color: 'text-red-600', label: 'Отменен' },
      refunded: { icon: <XCircle size={20} />, color: 'text-orange-600', label: 'Возвращен' },
    };
    return statusMap[status as keyof typeof statusMap] || statusMap.pending;
  }

  // Форматирование даты
  function formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString('ru-RU', {
      day: 'numeric',
      month: 'long',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  }

  // Форматирование цены
  function formatPrice(price: number): string {
    return price.toLocaleString('ru-RU');
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-[var(--tg-theme-bg-color)]">
        <Header title="Мои заказы" />
        <div className="flex items-center justify-center py-20">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[var(--tg-theme-button-color)]"></div>
        </div>
      </div>
    );
  }

  if (orders.length === 0) {
    return (
      <div className="min-h-screen bg-[var(--tg-theme-bg-color)]">
        <Header title="Мои заказы" />
        <EmptyState
          type="orders"
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
    <div className="min-h-screen bg-[var(--tg-theme-bg-color)]">
      <Header title="Мои заказы" showBackButton />

      <main className="p-4 space-y-3">
        {orders.map((order) => {
          const statusInfo = getStatusInfo(order.status);
          
          return (
            <div
              key={order.id}
              onClick={() => navigate(`/order/${order.id}`)}
              className="bg-[var(--tg-theme-secondary-bg-color)] rounded-lg p-4 cursor-pointer hover:bg-[var(--tg-theme-hint-color)]/20 transition-colors"
            >
              {/* Заголовок заказа */}
              <div className="flex items-center justify-between mb-3">
                <div>
                  <h3 className="font-semibold text-[var(--tg-theme-text-color)]">
                    Заказ №{order.id}
                  </h3>
                  <p className="text-sm text-[var(--tg-theme-hint-color)]">
                    {formatDate(order.created_at)}
                  </p>
                </div>
                <div className={`flex items-center gap-1 ${statusInfo.color}`}>
                  {statusInfo.icon}
                  <span className="text-xs font-medium">{statusInfo.label}</span>
                </div>
              </div>

              {/* Детали заказа */}
              <div className="space-y-2">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-[var(--tg-theme-hint-color)]">Товаров:</span>
                  <span className="text-[var(--tg-theme-text-color)]">{order.items?.length || 0} шт.</span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-[var(--tg-theme-hint-color)]">Адрес:</span>
                  <span className="text-[var(--tg-theme-text-color)] truncate max-w-[200px]">
                    {order.delivery_address || 'Не указан'}
                  </span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-[var(--tg-theme-hint-color)]">Оплата:</span>
                  <span className="text-[var(--tg-theme-text-color)] capitalize">
                    {order.payment_method === 'cash' ? 'Наличными' : order.payment_method}
                  </span>
                </div>
              </div>

              {/* Итоговая сумма */}
              <div className="mt-3 pt-3 border-t border-[var(--tg-theme-hint-color)]/20 flex items-center justify-between">
                <span className="text-sm text-[var(--tg-theme-hint-color)]">Сумма заказа:</span>
                <span className="text-lg font-bold text-[var(--tg-theme-button-color)]">
                  {formatPrice(order.total_amount)} сум
                </span>
              </div>
            </div>
          );
        })}
      </main>
    </div>
  );
}
