import { ShoppingBag, Heart, FileText, Package } from 'lucide-react';

interface EmptyStateProps {
  type: 'cart' | 'favorites' | 'orders' | 'products';
  title?: string;
  subtitle?: string;
  action?: React.ReactNode;
}

/**
 * Универсальное пустое состояние
 */
export function EmptyState({ type, title, subtitle, action }: EmptyStateProps) {
  const config = {
    cart: {
      icon: <ShoppingBag size={64} className="opacity-50" />,
      defaultTitle: 'Корзина пуста',
      defaultSubtitle: 'Добавьте товары из каталога',
    },
    favorites: {
      icon: <Heart size={64} className="opacity-50" />,
      defaultTitle: 'Избранное пусто',
      defaultSubtitle: 'Сохраняйте понравившиеся товары',
    },
    orders: {
      icon: <FileText size={64} className="opacity-50" />,
      defaultTitle: 'Заказов пока нет',
      defaultSubtitle: 'Оформите первый заказ',
    },
    products: {
      icon: <Package size={64} className="opacity-50" />,
      defaultTitle: 'Товары не найдены',
      defaultSubtitle: 'Попробуйте изменить параметры поиска',
    },
  };

  const { icon, defaultTitle, defaultSubtitle } = config[type];

  return (
    <div className="flex flex-col items-center justify-center py-20 text-center">
      <div className="text-[var(--tg-theme-hint-color)] mb-4">
        {icon}
      </div>
      <h3 className="text-xl font-semibold text-[var(--tg-theme-text-color)] mb-2">
        {title || defaultTitle}
      </h3>
      <p className="text-[var(--tg-theme-hint-color)] mb-6 max-w-xs">
        {subtitle || defaultSubtitle}
      </p>
      {action && <div>{action}</div>}
    </div>
  );
}
