import { User, Phone, Mail, Calendar, Star, ShoppingBag, Heart, LogOut } from 'lucide-react';
import { Header } from '../components/Header';
import { useTelegramUser } from '../lib/telegram';
import { useNavigate } from 'react-router-dom';

/**
 * Страница профиля пользователя
 */
export function Profile() {
  const navigate = useNavigate();
  const { user: telegramUser } = useTelegramUser();

  // Заглушка для демонстрации
  const userProfile = {
    name: telegramUser?.first_name || 'Пользователь',
    phone: '+998 90 123 45 67',
    email: 'user@example.com',
    joinedDate: 'Январь 2024',
    totalOrders: 12,
    totalSpent: 1250000,
    loyaltyPoints: 350,
    level: 'Gold',
  };

  // Форматирование суммы
  function formatPrice(price: number): string {
    return price.toLocaleString('ru-RU');
  }

  const menuItems = [
    { icon: <ShoppingBag size={20} />, label: 'Мои заказы', count: userProfile.totalOrders, onClick: () => navigate('/orders') },
    { icon: <Heart size={20} />, label: 'Избранное', count: 5, onClick: () => navigate('/favorites') },
    { icon: <Star size={20} />, label: 'Бонусные баллы', value: `${userProfile.loyaltyPoints} баллов`, onClick: () => {} },
  ];

  return (
    <div className="min-h-screen bg-[var(--tg-theme-bg-color)]">
      <Header title="Профиль" />

      <main className="p-4 space-y-6">
        {/* Информация о пользователе */}
        <section className="bg-gradient-to-r from-[var(--tg-theme-button-color)] to-blue-600 text-white rounded-2xl p-6">
          <div className="flex items-center gap-4 mb-4">
            <div className="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center">
              <User size={32} />
            </div>
            <div>
              <h2 className="text-xl font-bold">{userProfile.name}</h2>
              <p className="text-white/80 text-sm">{userProfile.level} клиент</p>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4 pt-4 border-t border-white/20">
            <div>
              <p className="text-white/80 text-xs mb-1">Всего заказов</p>
              <p className="text-2xl font-bold">{userProfile.totalOrders}</p>
            </div>
            <div>
              <p className="text-white/80 text-xs mb-1">Потрачено</p>
              <p className="text-2xl font-bold">{formatPrice(userProfile.totalSpent)}</p>
            </div>
          </div>
        </section>

        {/* Контактная информация */}
        <section className="space-y-3">
          <h3 className="text-lg font-semibold text-[var(--tg-theme-text-color)]">Контактная информация</h3>
          
          <div className="bg-[var(--tg-theme-secondary-bg-color)] rounded-lg p-4 space-y-3">
            <div className="flex items-center gap-3">
              <Phone size={20} className="text-[var(--tg-theme-hint-color)]" />
              <div>
                <p className="text-xs text-[var(--tg-theme-hint-color)]">Телефон</p>
                <p className="text-[var(--tg-theme-text-color)]">{userProfile.phone}</p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <Mail size={20} className="text-[var(--tg-theme-hint-color)]" />
              <div>
                <p className="text-xs text-[var(--tg-theme-hint-color)]">Email</p>
                <p className="text-[var(--tg-theme-text-color)]">{userProfile.email}</p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <Calendar size={20} className="text-[var(--tg-theme-hint-color)]" />
              <div>
                <p className="text-xs text-[var(--tg-theme-hint-color)]">В клубе с</p>
                <p className="text-[var(--tg-theme-text-color)]">{userProfile.joinedDate}</p>
              </div>
            </div>
          </div>
        </section>

        {/* Меню профиля */}
        <section className="space-y-3">
          <h3 className="text-lg font-semibold text-[var(--tg-theme-text-color)]">Меню</h3>
          
          <div className="bg-[var(--tg-theme-secondary-bg-color)] rounded-lg overflow-hidden">
            {menuItems.map((item, index) => (
              <button
                key={index}
                onClick={item.onClick}
                className="w-full flex items-center justify-between p-4 hover:bg-[var(--tg-theme-hint-color)]/20 transition-colors border-b border-[var(--tg-theme-hint-color)]/10 last:border-0"
              >
                <div className="flex items-center gap-3">
                  <div className="text-[var(--tg-theme-button-color)]">{item.icon}</div>
                  <span className="text-[var(--tg-theme-text-color)]">{item.label}</span>
                </div>
                <div className="flex items-center gap-2">
                  {item.count !== undefined && (
                    <span className="bg-[var(--tg-theme-button-color)] text-white text-xs px-2 py-1 rounded-full">
                      {item.count}
                    </span>
                  )}
                  {item.value && (
                    <span className="text-[var(--tg-theme-hint-color)] text-sm">{item.value}</span>
                  )}
                </div>
              </button>
            ))}
          </div>
        </section>

        {/* Кнопка выхода */}
        <button className="w-full bg-red-500 text-white py-4 rounded-lg font-semibold flex items-center justify-center gap-2 hover:bg-red-600 transition-colors">
          <LogOut size={20} />
          Выйти
        </button>

        {/* Версия приложения */}
        <p className="text-center text-xs text-[var(--tg-theme-hint-color)]">
          S1 Mini App v1.0.0
        </p>
      </main>
    </div>
  );
}
