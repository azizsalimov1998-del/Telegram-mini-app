import { ShoppingCart, Heart } from 'lucide-react';
import { Product } from '../types';

interface ProductCardProps {
  product: Product;
  onAddToCart?: (product: Product) => void;
  onToggleFavorite?: (product: Product) => void;
  isFavorite?: boolean;
}

/**
 * Карточка товара
 */
export function ProductCard({ 
  product, 
  onAddToCart,
  onToggleFavorite,
  isFavorite = false 
}: ProductCardProps) {
  const hasDiscount = product.original_price !== undefined && product.original_price > product.price;
  const discountPercent = hasDiscount && product.original_price !== undefined
    ? Math.round(((product.original_price - product.price) / product.original_price) * 100)
    : 0;

  return (
    <div className="bg-[var(--tg-theme-bg-color)] rounded-lg shadow-sm border border-[var(--tg-theme-secondary-bg-color)] overflow-hidden hover:shadow-md transition-shadow">
      {/* Изображение */}
      <div className="relative aspect-square bg-[var(--tg-theme-secondary-bg-color)]">
        {product.image_url ? (
          <img
            src={product.image_url}
            alt={product.name}
            className="w-full h-full object-cover"
            loading="lazy"
          />
        ) : (
          <div className="flex items-center justify-center h-full text-[var(--tg-theme-hint-color)]">
            <span className="text-4xl">📦</span>
          </div>
        )}

        {/* Скидка */}
        {hasDiscount && (
          <span className="absolute top-2 left-2 bg-red-500 text-white text-xs font-bold px-2 py-1 rounded">
            -{discountPercent}%
          </span>
        )}

        {/* Избранное */}
        {onToggleFavorite && (
          <button
            onClick={(e) => {
              e.preventDefault();
              onToggleFavorite(product);
            }}
            className="absolute top-2 right-2 p-2 bg-white/90 rounded-full hover:bg-white transition-colors"
          >
            <Heart
              size={18}
              className={isFavorite ? 'fill-red-500 text-red-500' : 'text-[var(--tg-theme-text-color)]'}
            />
          </button>
        )}
      </div>

      {/* Информация о товаре */}
      <div className="p-3">
        {/* Название */}
        <h3 className="font-medium text-[var(--tg-theme-text-color)] mb-1 line-clamp-2 min-h-[2.5rem]">
          {product.name}
        </h3>

        {/* Бренд (если есть) */}
        {product.brand && (
          <p className="text-xs text-[var(--tg-theme-hint-color)] mb-2">
            {product.brand}
          </p>
        )}

        {/* Цена */}
        <div className="flex items-center gap-2 mb-3">
          <span className="text-lg font-bold text-[var(--tg-theme-text-color)]">
            {product.price.toLocaleString('ru-RU')} сум
          </span>
          
          {hasDiscount && (
            <span className="text-sm text-[var(--tg-theme-hint-color)] line-through">
              {product.original_price?.toLocaleString('ru-RU')}
            </span>
          )}
        </div>

        {/* Остаток на складе */}
        {product.stock > 0 ? (
          <p className="text-xs text-green-600 mb-3">
            В наличии: {product.stock} шт.
          </p>
        ) : (
          <p className="text-xs text-red-600 mb-3">
            Нет в наличии
          </p>
        )}

        {/* Кнопка "В корзину" */}
        {onAddToCart && product.stock > 0 && (
          <button
            onClick={() => onAddToCart(product)}
            className="w-full bg-[var(--tg-theme-button-color)] text-[var(--tg-theme-button-text-color)] py-2 px-4 rounded-lg font-medium hover:opacity-90 transition-opacity flex items-center justify-center gap-2"
          >
            <ShoppingCart size={18} />
            В корзину
          </button>
        )}

        {product.stock === 0 && (
          <button
            disabled
            className="w-full bg-[var(--tg-theme-secondary-bg-color)] text-[var(--tg-theme-hint-color)] py-2 px-4 rounded-lg font-medium cursor-not-allowed"
          >
            Нет в наличии
          </button>
        )}
      </div>
    </div>
  );
}
