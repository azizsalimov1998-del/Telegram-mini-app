/**
 * Компонент загрузки (спиннер)
 */
export function LoadingSpinner() {
  return (
    <div className="flex items-center justify-center p-8">
      <div className="relative">
        <div className="w-12 h-12 rounded-full border-4 border-[var(--tg-theme-secondary-bg-color)]"></div>
        <div className="absolute top-0 left-0 w-12 h-12 rounded-full border-4 border-[var(--tg-theme-button-color)] border-t-transparent animate-spin"></div>
      </div>
    </div>
  );
}

/**
 * Skeleton для карточки товара
 */
export function ProductSkeleton() {
  return (
    <div className="bg-[var(--tg-theme-bg-color)] rounded-lg shadow-sm border border-[var(--tg-theme-secondary-bg-color)] overflow-hidden animate-pulse">
      <div className="aspect-square bg-[var(--tg-theme-secondary-bg-color)]"></div>
      <div className="p-3 space-y-2">
        <div className="h-4 bg-[var(--tg-theme-secondary-bg-color)] rounded w-3/4"></div>
        <div className="h-3 bg-[var(--tg-theme-secondary-bg-color)] rounded w-1/2"></div>
        <div className="h-6 bg-[var(--tg-theme-secondary-bg-color)] rounded w-1/3 mt-2"></div>
        <div className="h-8 bg-[var(--tg-theme-secondary-bg-color)] rounded w-full mt-3"></div>
      </div>
    </div>
  );
}

/**
 * Skeleton списка товаров
 */
export function ProductsGridSkeleton() {
  return (
    <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4">
      {Array.from({ length: 8 }).map((_, i) => (
        <ProductSkeleton key={i} />
      ))}
    </div>
  );
}
