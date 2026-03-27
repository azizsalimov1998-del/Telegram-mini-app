import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Heart } from 'lucide-react';
import { Header } from '../components/Header';
import { EmptyState } from '../components/EmptyState';
import { ProductCard } from '../components/ProductCard';
import { useCartStore } from '../store/cartStore';

/**
 * Страница избранного
 */
export function Favorites() {
  const navigate = useNavigate();
  const { addToCart } = useCartStore();
  
  // Заглушка для демонстрации (в реальности загружать с API)
  const [favorites, setFavorites] = useState([
    { id: 1, name: 'Товар 1', price: 50000, image_url: '', stock: 10 },
    { id: 2, name: 'Товар 2', price: 75000, image_url: '', stock: 5 },
    { id: 3, name: 'Товар 3', price: 120000, image_url: '', stock: 0 },
  ]);

  // Удаление из избранного
  function handleRemoveFromFavorites(productId: number) {
    if (confirm('Удалить товар из избранного?')) {
      setFavorites(favorites.filter(p => p.id !== productId));
    }
  }

  if (favorites.length === 0) {
    return (
      <div className="min-h-screen bg-[var(--tg-theme-bg-color)]">
        <Header title="Избранное" showBackButton />
        <EmptyState
          type="favorites"
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
      <Header title={`Избранное (${favorites.length})`} showBackButton />

      <main className="p-4">
        {/* Сетка товаров */}
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4">
          {favorites.map((product) => (
            <div key={product.id}>
              <ProductCard
                product={product as any}
                onAddToCart={(p) => addToCart(p, 1)}
                onToggleFavorite={() => handleRemoveFromFavorites(product.id)}
                isFavorite={true}
              />
            </div>
          ))}
        </div>

        {/* Информация */}
        <div className="mt-6 p-4 bg-[var(--tg-theme-secondary-bg-color)] rounded-lg">
          <div className="flex items-center gap-2 text-[var(--tg-theme-hint-color)] text-sm">
            <Heart size={16} />
            <span>Сохраняйте понравившиеся товары, чтобы быстро найти их позже</span>
          </div>
        </div>
      </main>
    </div>
  );
}
