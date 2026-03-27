import { ChevronLeft } from 'lucide-react';

interface HeaderProps {
  title?: string;
  showBackButton?: boolean;
  onBackClick?: () => void;
  rightElement?: React.ReactNode;
}

/**
 * Базовый компонент Header с поддержкой Telegram BackButton
 */
export function Header({ 
  title = 'S1 Shop', 
  showBackButton = false, 
  onBackClick,
  rightElement 
}: HeaderProps) {
  return (
    <header className="sticky top-0 z-50 bg-[var(--tg-theme-bg-color)] border-b border-[var(--tg-theme-secondary-bg-color)]">
      <div className="flex items-center justify-between px-4 py-3">
        {/* Левая часть: BackButton или пустое место */}
        <div className="w-10">
          {showBackButton && (
            <button
              onClick={onBackClick}
              className="p-2 -ml-2 rounded-full hover:bg-[var(--tg-theme-secondary-bg-color)] transition-colors"
              aria-label="Назад"
            >
              <ChevronLeft 
                size={24} 
                className="text-[var(--tg-theme-text-color)]"
              />
            </button>
          )}
        </div>
        
        {/* Центральная часть: Заголовок */}
        <h1 className="text-lg font-semibold text-[var(--tg-theme-text-color)] flex-1 text-center">
          {title}
        </h1>
        
        {/* Правая часть: Дополнительные элементы */}
        <div className="w-10 flex justify-end">
          {rightElement}
        </div>
      </div>
    </header>
  );
}
