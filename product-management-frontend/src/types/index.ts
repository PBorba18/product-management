export interface Product {
  id: number;
  name: string;
  description: string;
  category: string;
  price: number;
  stock: number;
  discount_percent?: number;
  coupon_code?: string;
  final_price?: number;
  is_active: boolean;
}

export interface Coupon {
  code: string;
  discount_percent: number;
  is_active: boolean;
}

export interface ProductFilters {
  min_price?: number;
  max_price?: number;
  name?: string;
}

export interface ProductFormData {
  name: string;
  description: string;
  category: string;
  price: number;
  stock: number;
}

export interface ApiResponse<T> {
  data: T;
  message?: string;
  success: boolean;
}