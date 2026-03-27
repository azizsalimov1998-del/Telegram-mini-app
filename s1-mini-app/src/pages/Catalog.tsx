import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, ShoppingCart } from 'lucide-react';
import { Header } from '../components/Header';
import { CategoryList } from '../components/CategoryList';
import { ProductCard } from '../components/ProductCard';
import { ProductsGridSkeleton } from '../components/LoadingSpinner';
import { useCartStore } from '../store/cartStore';
import { getCategories } from '../services/categories';
import { getProducts } from '../services/products';
import { Category, Product } from '../types';

/**
 * Страница каталога товаров
 */
export function Catalog() {
  const navigate = useNavigate();
  const { addToCart } = useCartStore();
  
  const [categories, setCategories] = useState<Category[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<number | undefined>();
  const [isLoading, setIsLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');

  // Загрузка данных
  useEffect(() => {
    loadData();
  }, [selectedCategory]);

  async function loadData() {
    setIsLoading(true);
    try {
      // Загружаем категории
      const categoriesData = await getCategories();
      setCategories(categoriesData);
      console.log('✅ Категории загружены:', categoriesData);

      // Загружаем товары с фильтром по категории
      const productsData = await getProducts({
        category_id: selectedCategory,
        limit: 50,
      });
      console.log('✅ Товары загружены:', productsData);
      console.log(`📦 Найдено товаров: ${productsData.data?.length || 0}`);
      setProducts(productsData.data || []);
    } catch (error) {
      console.error('❌ Ошибка загрузки:', error);
    } finally {
      setIsLoading(false);
    }
  }

  // Обработчик добавления в корзину
  function handleAddToCart(product: Product) {
    addToCart(product);
    // Можно показать toast уведомление
  }

  // Обработчик клика на товар
  function handleProductClick(productId: number) {
    navigate(`/product/${productId}`);
  }

  // Фильтрация по поиску
  const filteredProducts = searchQuery
    ? products.filter(p => 
        p.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        p.description?.toLowerCase().includes(searchQuery.toLowerCase())
      )
    : products;

  return (
    <div className="min-h-screen bg-[var(--tg-theme-bg-color)]">
      <Header 
        title="S1 Shop" 
        rightElement={
          <button 
            onClick={() => navigate('/cart')}
            className="relative p-2 hover:bg-[var(--tg-theme-secondary-bg-color)] rounded-full transition-colors"
          >
            <ShoppingCart size={24} className="text-[var(--tg-theme-text-color)]" />
            {/* Бейдж с количеством товаров в корзине можно добавить позже */}
          </button>
        }
      />

      <main className="p-4 pb-20">
        {/* Поиск */}
        <div className="relative mb-4">
          <input
            type="text"
            placeholder="Поиск товаров..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full bg-[var(--tg-theme-secondary-bg-color)] text-[var(--tg-theme-text-color)] pl-10 pr-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-[var(--tg-theme-button-color)]"
          />
          <Search 
            size={20} 
            className="absolute left-3 top-1/2 -translate-y-1/2 text-[var(--tg-theme-hint-color)]"
          />
        </div>

        {/* Категории */}
        <CategoryList
          categories={categories}
          selectedCategory={selectedCategory}
          onSelectCategory={setSelectedCategory}
        />

        {/* Товары */}
        {isLoading ? (
          <ProductsGridSkeleton />
        ) : filteredProducts.length > 0 ? (
          <>
            <h2 className="text-lg font-semibold text-[var(--tg-theme-text-color)] mb-3">
              {selectedCategory 
                ? categories.find(c => c.id === selectedCategory)?.name || 'Товары'
                : 'Все товары'}
              {searchQuery && ` • Поиск: "${searchQuery}"`}
            </h2>
            
            <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4">
              {filteredProducts.map((product) => (
                <div key={product.id} onClick={() => handleProductClick(product.id)}>
                  <ProductCard
                    product={product}
                    onAddToCart={handleAddToCart}
                  />
                </div>
              ))}
            </div>
          </>
        ) : (
          <div className="text-center text-[var(--tg-theme-hint-color)] mt-20">
            <p className="text-lg mb-2">🔍 Товары не найдены</p>
            <p className="text-sm">
              {searchQuery 
                ? 'Попробуйте изменить запрос' 
                : 'В этой категории пока нет товаров'}
            </p>
          </div>
        )}
      </main>
    </div>
  );
}
