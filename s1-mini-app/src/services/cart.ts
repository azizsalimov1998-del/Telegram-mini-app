/**
 * API сервис для работы с корзиной
 */
import api from './api';
import { Cart, CartItem, ApiResponse } from '../types';

/**
 * Получить корзину пользователя
 */
export async function getCart(): Promise<Cart> {
  const response = await api.get<ApiResponse<Cart>>('/cart');
  return response.data.data!;
}

/**
 * Добавить товар в корзину
 */
export async function addToCart(productId: number, quantity = 1): Promise<CartItem> {
  const response = await api.post<ApiResponse<CartItem>>('/cart', { 
    product_id: productId, 
    quantity 
  });
  return response.data.data!;
}

/**
 * Обновить количество товара в корзине
 */
export async function updateCartItem(itemId: number, quantity: number): Promise<CartItem> {
  const response = await api.patch<ApiResponse<CartItem>>(`/cart/${itemId}`, { quantity });
  return response.data.data!;
}

/**
 * Удалить товар из корзины
 */
export async function removeFromCart(itemId: number): Promise<void> {
  await api.delete(`/cart/${itemId}`);
}

/**
 * Очистить корзину
 */
export async function clearCart(): Promise<void> {
  await api.delete('/cart/clear');
}
