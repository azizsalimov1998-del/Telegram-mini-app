/**
 * API сервис для работы с категориями
 */
import api from './api';
import { Category, Subcategory, ApiResponse } from '../types';

/**
 * Получить все активные категории
 */
export async function getCategories(): Promise<Category[]> {
  const response = await api.get<ApiResponse<Category[]>>('/categories');
  return response.data.data || [];
}

/**
 * Получить категорию по ID
 */
export async function getCategoryById(id: number): Promise<Category> {
  const response = await api.get<ApiResponse<Category>>(`/categories/${id}`);
  return response.data.data!;
}

/**
 * Получить подкатегории категории
 */
export async function getSubcategories(categoryId: number): Promise<Subcategory[]> {
  const response = await api.get<ApiResponse<Subcategory[]>>(`/categories/${categoryId}/subcategories`);
  return response.data.data || [];
}
