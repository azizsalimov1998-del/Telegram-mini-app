import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ShoppingCart, Heart, Share2, } from 'lucide-react';
import { Header } from '../components/Header';
import { ProductCard } from '../components/ProductCard';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { useCartStore } from '../store/cartStore';
import { getProductById, getRelatedProducts } from '../services/products';
import { Product } from '../types';
import { TelegramButtons } from '../lib/telegram';

/**
 * Страница детальной информации о товаре
 */
export function ProductDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { addToCart } = useCartStore();
  
  const [product, setProduct] = useState<Product | null>(null);
  const [relatedProducts, setRelatedProducts] = useState<Product[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [quantity, setQuantity] = useState(1);

  // Загрузка данных
  useEffect(() => {
    if (id) {
      loadData(id);
    }
  }, [id]);

  async function loadData(productId: string) {
    setIsLoading(true);
    try {
      const [productData, relatedData] = await Promise.all([
        getProductById(parseInt(productId)),
        getRelatedProducts(parseInt(productId), 4),
      ]);
      setProduct(productData);
      setRelatedProducts(relatedData);
    } catch (error) {
      console.error('Ошибка загрузки:', error);
    } finally {
      setIsLoading(false);
    }
  }

  // Обработчик добавления в корзину
  function handleAddToCart() {
    if (product) {
      addToCart(product, quantity);
      
      // Показать главную кнопку Telegram
      TelegramButtons.showMainButton(
        `Добавлено ${quantity} шт. • ${formatPrice(product.price * quantity)} сум`,
        () => navigate('/cart')
      );
    }
  }

  // Форматирование цены
  function formatPrice(price: number): string {
    return price.toLocaleString('ru-RU');
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-[var(--tg-theme-bg-color)]">
        <Header title="Загрузка..." showBackButton />
        <LoadingSpinner />
      </div>
    );
  }

  if (!product) {
    return (
      <div className="min-h-screen bg-[var(--tg-theme-bg-color)]">
        <Header title="Товар" showBackButton />
        <div className="text-center text-[var(--tg-theme-hint-color)] mt-20">
          <p className="text-lg">😕 Товар не найден</p>
        </div>
      </div>
    );
  }

  const hasDiscount = product.original_price && product.original_price > product.price;

  return (
    <div className="min-h-screen bg-[var(--tg-theme-bg-color)] pb-20">
      <Header title="Товар" showBackButton />

      <main>
        {/* Изображение */}
        <div className="aspect-square bg-[var(--tg-theme-secondary-bg-color)]">
          {product.image_url ? (
            <img
              src={product.image_url}
              alt={product.name}
              className="w-full h-full object-cover"
            />
          ) : (
            <div className="flex items-center justify-center h-full text-[var(--tg-theme-hint-color)]">
              <span className="text-6xl">📦</span>
            </div>
          )}
        </div>

        {/* Информация о товаре */}
        <div className="p-4 space-y-4">
          {/* Название и бренд */}
          <div>
            <h1 className="text-xl font-bold text-[var(--tg-theme-text-color)] mb-1">
              {product.name}
            </h1>
            {product.brand && (
              <p className="text-sm text-[var(--tg-theme-hint-color)]">
                {product.brand}
              </p>
            )}
          </div>

          {/* Цена */}
          <div className="flex items-baseline gap-3">
            <span className="text-2xl font-bold text-[var(--tg-theme-text-color)]">
              {formatPrice(product.price)} сум
            </span>
            {hasDiscount && (
              <>
                <span className="text-lg text-[var(--tg-theme-hint-color)] line-through">
                  {formatPrice(product.original_price!)}
                </span>
                <span className="bg-red-500 text-white text-xs font-bold px-2 py-1 rounded">
                  -{Math.round(((product.original_price! - product.price) / product.original_price!) * 100)}%
                </span>
              </>
            )}
          </div>

          {/* Описание */}
          {product.description && (
            <div>
              <h2 className="text-sm font-semibold text-[var(--tg-theme-text-color)] mb-2">
                Описание
              </h2>
              <p className="text-sm text-[var(--tg-theme-text-color)] leading-relaxed whitespace-pre-line">
                {product.description}
              </p>
            </div>
          )}

          {/* Наличие на складе */}
          <div className="flex items-center justify-between">
            <span className={`text-sm ${product.stock > 0 ? 'text-green-600' : 'text-red-600'}`}>
              {product.stock > 0 ? `✓ В наличии: ${product.stock} шт.` : '✗ Нет в наличии'}
            </span>
            <span className="text-sm text-[var(--tg-theme-hint-color)]">
              👁 {product.views} просмотров
            </span>
          </div>

          {/* Количество */}
          {product.stock > 0 && (
            <div className="flex items-center justify-between bg-[var(--tg-theme-secondary-bg-color)] rounded-lg p-4">
              <span className="text-sm font-medium text-[var(--tg-theme-text-color)]">
                Количество
              </span>
              <div className="flex items-center gap-3">
                <button
                  onClick={() => setQuantity(Math.max(1, quantity - 1))}
                  className="w-10 h-10 rounded-full bg-[var(--tg-theme-bg-color)] flex items-center justify-center text-[var(--tg-theme-text-color)] hover:bg-[var(--tg-theme-hint-color)]/20"
                >
                  −
                </button>
                <span className="w-8 text-center font-semibold text-[var(--tg-theme-text-color)]">
                  {quantity}
                </span>
                <button
                  onClick={() => setQuantity(Math.min(product.stock, quantity + 1))}
                  className="w-10 h-10 rounded-full bg-[var(--tg-theme-bg-color)] flex items-center justify-center text-[var(--tg-theme-text-color)] hover:bg-[var(--tg-theme-hint-color)]/20"
                >
                  +
                </button>
              </div>
            </div>
          )}

          {/* Кнопки действий */}
          {product.stock > 0 && (
            <button
              onClick={handleAddToCart}
              className="w-full bg-[var(--tg-theme-button-color)] text-[var(--tg-theme-button-text-color)] py-4 rounded-lg font-semibold text-lg hover:opacity-90 transition-opacity flex items-center justify-center gap-2"
            >
              <ShoppingCart size={24} />
              Добавить в корзину • {formatPrice(product.price * quantity)} сум
            </button>
          )}

          {product.stock === 0 && (
            <button
              disabled
              className="w-full bg-[var(--tg-theme-secondary-bg-color)] text-[var(--tg-theme-hint-color)] py-4 rounded-lg font-semibold cursor-not-allowed"
            >
              Нет в наличии
            </button>
          )}

          {/* Дополнительные кнопки */}
          <div className="flex gap-2">
            <button className="flex-1 bg-[var(--tg-theme-secondary-bg-color)] text-[var(--tg-theme-text-color)] py-3 rounded-lg font-medium hover:bg-[var(--tg-theme-hint-color)]/20 transition-colors flex items-center justify-center gap-2">
              <Heart size={20} />
              В избранное
            </button>
            <button className="flex-1 bg-[var(--tg-theme-secondary-bg-color)] text-[var(--tg-theme-text-color)] py-3 rounded-lg font-medium hover:bg-[var(--tg-theme-hint-color)]/20 transition-colors flex items-center justify-center gap-2">
              <Share2 size={20} />
              Поделиться
            </button>
          </div>
        </div>

        {/* Похожие товары */}
        {relatedProducts.length > 0 && (
          <div className="mt-6 p-4 border-t border-[var(--tg-theme-secondary-bg-color)]">
            <h2 className="text-lg font-semibold text-[var(--tg-theme-text-color)] mb-4">
              Похожие товары
            </h2>
            <div className="grid grid-cols-2 gap-3">
              {relatedProducts.map((p) => (
                <div key={p.id} onClick={() => navigate(`/product/${p.id}`)}>
                  <ProductCard product={p} onAddToCart={(prod) => addToCart(prod, 1)} />
                </div>
              ))}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
