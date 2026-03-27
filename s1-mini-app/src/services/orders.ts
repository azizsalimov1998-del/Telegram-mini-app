/**
 * API сервис для работы с заказами
 */
import api from './api';
import { Order, ApiResponse } from '../types';

/**
 * Создать новый заказ
 */
export async function createOrder(orderData: {
  delivery_address: string;
  payment_method: string;
  promo_code?: string;
}): Promise<Order> {
  const response = await api.post<ApiResponse<Order>>('/orders', orderData);
  return response.data.data!;
}

/**
 * Получить заказы пользователя
 */
export async function getUserOrders(): Promise<Order[]> {
  const response = await api.get<ApiResponse<Order[]>>('/orders');
  return response.data.data || [];
}

/**
 * Получить заказ по ID
 */
export async function getOrderById(id: number): Promise<Order> {
  const response = await api.get<ApiResponse<Order>>(`/orders/${id}`);
  return response.data.data!;
}

/**
 * Отменить заказ (если еще не отправлен)
 */
export async function cancelOrder(orderId: number): Promise<void> {
  await api.post(`/orders/${orderId}/cancel`);
}
