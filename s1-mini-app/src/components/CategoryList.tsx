import { Category } from '../types';

interface CategoryListProps {
  categories: Category[];
  selectedCategory?: number;
  onSelectCategory?: (categoryId: number | undefined) => void;
}

/**
 * Список категорий
 */
export function CategoryList({ 
  categories, 
  selectedCategory,
  onSelectCategory 
}: CategoryListProps) {
  return (
    <div className="flex gap-2 overflow-x-auto pb-2 mb-4 scrollbar-hide">
      {/* Кнопка "Все" */}
      <button
        onClick={() => onSelectCategory?.(undefined)}
        className={`flex-shrink-0 px-4 py-2 rounded-full font-medium transition-colors ${
          selectedCategory === undefined
            ? 'bg-[var(--tg-theme-button-color)] text-[var(--tg-theme-button-text-color)]'
            : 'bg-[var(--tg-theme-secondary-bg-color)] text-[var(--tg-theme-text-color)] hover:bg-[var(--tg-theme-hint-color)]/20'
        }`}
      >
        Все
      </button>

      {/* Категории */}
      {categories.map((category) => (
        <button
          key={category.id}
          onClick={() => onSelectCategory?.(category.id)}
          className={`flex-shrink-0 px-4 py-2 rounded-full font-medium transition-colors flex items-center gap-2 ${
            selectedCategory === category.id
              ? 'bg-[var(--tg-theme-button-color)] text-[var(--tg-theme-button-text-color)]'
              : 'bg-[var(--tg-theme-secondary-bg-color)] text-[var(--tg-theme-text-color)] hover:bg-[var(--tg-theme-hint-color)]/20'
          }`}
        >
          {category.emoji && <span>{category.emoji}</span>}
          {category.name}
        </button>
      ))}
    </div>
  );
}
