/**
 * API сервис для работы с избранным
 */
import api from './api';
import { Favorite, ApiResponse } from '../types';

/**
 * Получить список избранного
 */
export async function getFavorites(): Promise<Favorite[]> {
  const response = await api.get<ApiResponse<Favorite[]>>('/favorites');
  return response.data.data || [];
}

/**
 * Добавить товар в избранное
 */
export async function addToFavorites(productId: number): Promise<Favorite> {
  const response = await api.post<ApiResponse<Favorite>>('/favorites', { product_id: productId });
  return response.data.data!;
}

/**
 * Удалить товар из избранного
 */
export async function removeFromFavorites(productId: number): Promise<void> {
  await api.delete(`/favorites/${productId}`);
}

/**
 * Проверить, есть ли товар в избранном
 */
export async function checkIfFavorite(productId: number): Promise<boolean> {
  try {
    // Получаем все избранные и проверяем наличие
    const favorites = await getFavorites();
    return favorites.some(fav => fav.product_id === productId);
  } catch {
    return false;
  }
}
