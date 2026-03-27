/**
 * API сервис для работы с товарами
 */
import api from './api';
import { Product, ProductsQueryParams, PaginatedResponse, ApiResponse } from '../types';

/**
 * Получить товары с фильтрами и пагинацией
 */
export async function getProducts(params?: ProductsQueryParams): Promise<PaginatedResponse<Product>> {
  const response = await api.get<ApiResponse<PaginatedResponse<Product>>>('/products', { params });
  return response.data.data!;
}

/**
 * Получить товар по ID
 */
export async function getProductById(id: number): Promise<Product> {
  const response = await api.get<ApiResponse<Product>>(`/products/${id}`);
  return response.data.data!;
}

/**
 * Поиск товаров
 */
export async function searchProducts(query: string, limit = 20): Promise<Product[]> {
  const response = await api.get<ApiResponse<Product[]>>('/products/search', { 
    params: { q: query, limit } 
  });
  return response.data.data || [];
}

/**
 * Добавить просмотр товара
 */
export async function incrementProductViews(productId: number): Promise<void> {
  await api.post(`/products/${productId}/views`);
}

/**
 * Похожие товары
 */
export async function getRelatedProducts(productId: number, limit = 4): Promise<Product[]> {
  const response = await api.get<ApiResponse<Product[]>>(`/products/${productId}/related`, {
    params: { limit }
  });
  return response.data.data || [];
}
