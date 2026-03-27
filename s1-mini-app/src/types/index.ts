/**
 * Основные типы данных для S1 Mini App
 */

// Пользователь Telegram
export interface User {
  id: number;
  telegram_id: number;
  name: string;
  phone?: string;
  email?: string;
  language: 'ru' | 'uz';
  is_admin: boolean;
  created_at: string;
  acquisition_channel?: string;
}

// Категория товаров
export interface Category {
  id: number;
  name: string;
  description?: string;
  emoji?: string;
  is_active: boolean;
  created_at: string;
}

// Подкатегория
export interface Subcategory {
  id: number;
  name: string;
  category_id: number;
  description?: string;
  is_active: boolean;
}

// Товар
export interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  cost_price?: number;
  original_price?: number;
  category_id: number;
  subcategory_id?: number;
  brand?: string;
  image_url?: string;
  images?: ProductImage[];
  stock: number;
  views: number;
  sales_count: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  discount_percent?: number; // Вычисляется на бэкенде
}

// Изображение товара
export interface ProductImage {
  id: number;
  product_id: number;
  image_url: string;
  sort_order: number;
}

// Элемент корзины
export interface CartItem {
  id?: number;
  user_id: number;
  product_id: number;
  quantity: number;
  product?: Product; // Данные товара (при получении с бэкенда)
}

// Корзина пользователя
export interface Cart {
  items: CartItem[];
  total_amount: number;
  total_items: number;
}

// Заказ
export interface Order {
  id: number;
  user_id: number;
  total_amount: number;
  status: OrderStatus;
  delivery_address: string;
  payment_method: string;
  payment_status: PaymentStatus;
  promo_discount: number;
  delivery_cost: number;
  created_at: string;
  items?: OrderItem[]; // Детали заказа
  user?: User; // Данные пользователя (для админа)
}

// Товар в заказе
export interface OrderItem {
  id: number;
  order_id: number;
  product_id: number;
  quantity: number;
  price: number;
  product?: Product; // Данные товара
}

// Статус заказа
export type OrderStatus = 
  | 'pending'      // Ожидает подтверждения
  | 'confirmed'    // Подтвержден
  | 'processing'   // В обработке
  | 'shipped'      // Отправлен
  | 'delivered'    // Доставлен
  | 'cancelled'    // Отменен
  | 'refunded';    // Возвращен

// Статус оплаты
export type PaymentStatus = 
  | 'pending'      // Ожидает оплаты
  | 'paid'         // Оплачен
  | 'failed'       // Ошибка оплаты
  | 'refunded';    // Возвращен

// Отзыв
export interface Review {
  id: number;
  user_id: number;
  product_id: number;
  rating: number; // 1-5
  comment: string;
  created_at: string;
  user?: User;
}

// Избранное
export interface Favorite {
  id: number;
  user_id: number;
  product_id: number;
  created_at: string;
  product?: Product;
}

// Параметры для API запросов
export interface ProductsQueryParams {
  category_id?: number;
  subcategory_id?: number;
  search?: string;
  min_price?: number;
  max_price?: number;
  brand?: string;
  sort_by?: 'price_asc' | 'price_desc' | 'name' | 'popular' | 'newest';
  page?: number;
  limit?: number;
}

// Ответ API с пагинацией
export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  limit: number;
  has_more: boolean;
}

// Универсальный ответ API
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}
