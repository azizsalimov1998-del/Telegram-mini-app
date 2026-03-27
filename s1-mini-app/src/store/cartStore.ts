/**
 * Zustand store для корзины
 */
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { CartItem, Product } from '../types';
import * as cartAPI from '../services/cart';

interface CartStoreState {
  items: CartItem[];
  totalAmount: number;
  totalItems: number;
  isLoading: boolean;
  error: string | null;
  
  // Actions
  fetchCart: () => Promise<void>;
  addToCart: (product: Product, quantity?: number) => Promise<void>;
  removeFromCart: (itemId: number) => Promise<void>;
  updateQuantity: (itemId: number, quantity: number) => Promise<void>;
  clearCart: () => Promise<void>;
  resetCart: () => void;
}

const initialState = {
  items: [],
  totalAmount: 0,
  totalItems: 0,
  isLoading: false,
  error: null,
};

export const useCartStore = create<CartStoreState>()(
  persist(
    (set, get) => ({
      ...initialState,

      // Загрузка корзины с бэкенда
      fetchCart: async () => {
        set({ isLoading: true, error: null });
        try {
          const cart = await cartAPI.getCart();
          set({ 
            items: cart.items, 
            totalAmount: cart.total_amount, 
            totalItems: cart.total_items,
            isLoading: false 
          });
        } catch (error) {
          set({ 
            error: error instanceof Error ? error.message : 'Ошибка загрузки корзины',
            isLoading: false 
          });
        }
      },

      // Добавление товара
      addToCart: async (product: Product, quantity = 1) => {
        set({ isLoading: true, error: null });
        try {
          const newItem = await cartAPI.addToCart(product.id, quantity);
          const currentItems = get().items;
          const existingItem = currentItems.find(item => item.product_id === product.id);
          
          let newItems: CartItem[];
          if (existingItem) {
            newItems = currentItems.map(item =>
              item.product_id === product.id
                ? { ...item, quantity: item.quantity + quantity }
                : item
            );
          } else {
            newItems = [...currentItems, { ...newItem, product }];
          }
          
          const newTotalAmount = newItems.reduce(
            (sum, item) => sum + (item.product?.price || 0) * item.quantity,
            0
          );
          
          set({
            items: newItems,
            totalAmount: newTotalAmount,
            totalItems: newItems.reduce((sum, item) => sum + item.quantity, 0),
            isLoading: false,
          });
        } catch (error) {
          set({ 
            error: error instanceof Error ? error.message : 'Ошибка добавления в корзину',
            isLoading: false 
          });
        }
      },

      // Удаление товара
      removeFromCart: async (itemId: number) => {
        set({ isLoading: true, error: null });
        try {
          await cartAPI.removeFromCart(itemId);
          const newItems = get().items.filter(item => item.id !== itemId);
          set({
            items: newItems,
            totalAmount: newItems.reduce(
              (sum, item) => sum + (item.product?.price || 0) * item.quantity,
              0
            ),
            totalItems: newItems.reduce((sum, item) => sum + item.quantity, 0),
            isLoading: false,
          });
        } catch (error) {
          set({ 
            error: error instanceof Error ? error.message : 'Ошибка удаления из корзины',
            isLoading: false 
          });
        }
      },

      // Обновление количества
      updateQuantity: async (itemId: number, quantity: number) => {
        if (quantity < 1) {
          get().removeFromCart(itemId);
          return;
        }

        set({ isLoading: true, error: null });
        try {
          await cartAPI.updateCartItem(itemId, quantity);
          const newItems = get().items.map(item =>
            item.id === itemId ? { ...item, quantity } : item
          );
          set({
            items: newItems,
            totalAmount: newItems.reduce(
              (sum, item) => sum + (item.product?.price || 0) * item.quantity,
              0
            ),
            totalItems: newItems.reduce((sum, item) => sum + item.quantity, 0),
            isLoading: false,
          });
        } catch (error) {
          set({ 
            error: error instanceof Error ? error.message : 'Ошибка обновления количества',
            isLoading: false 
          });
        }
      },

      // Очистка корзины
      clearCart: async () => {
        set({ isLoading: true, error: null });
        try {
          await cartAPI.clearCart();
          set({
            items: [],
            totalAmount: 0,
            totalItems: 0,
            isLoading: false,
          });
        } catch (error) {
          set({ 
            error: error instanceof Error ? error.message : 'Ошибка очистки корзины',
            isLoading: false 
          });
        }
      },

      // Сброс состояния (при выходе)
      resetCart: () => {
        set(initialState);
      },
    }),
    {
      name: 'cart-storage', // ключ для localStorage
      partialize: (state) => ({ 
        items: state.items,
        totalAmount: state.totalAmount,
        totalItems: state.totalItems,
      }), // сохраняем только эти поля
    }
  )
);
