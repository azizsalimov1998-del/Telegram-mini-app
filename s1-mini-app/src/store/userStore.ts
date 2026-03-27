/**
 * Zustand store для пользователя
 */
import { create } from 'zustand';
import { User } from '../types';
import { useTelegramUser } from '../lib/telegram';

interface UserStoreState {
  user: User | null;
  telegramId: number | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  
  // Actions
  setUser: (user: User) => void;
  setTelegramId: (id: number) => void;
  logout: () => void;
}

export const useUserStore = create<UserStoreState>((set) => ({
  user: null,
  telegramId: null,
  isAuthenticated: false,
  isLoading: true,

  setUser: (user) => {
    set({ user, isAuthenticated: true, isLoading: false });
  },

  setTelegramId: (id) => {
    set({ telegramId: id });
  },

  logout: () => {
    set({ 
      user: null, 
      telegramId: null, 
      isAuthenticated: false,
      isLoading: false 
    });
  },
}));

// Хук для инициализации пользователя при старте приложения
export function useInitializeUser() {
  const { user: telegramUser, loading } = useTelegramUser();
  const { setTelegramId } = useUserStore.getState();

  // При изменении Telegram данных обновляем store
  if (telegramUser && telegramUser.id) {
    setTelegramId(telegramUser.id);
    
    // Здесь можно добавить запрос к бэкенду для получения полного профиля
    // fetchUserProfile(telegramUser.id).then(setUser);
  }

  return {
    telegramUser,
    loading,
  };
}
