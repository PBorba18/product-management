// apiService.js - Versão com Axios
import axios from 'axios';

// Configurar instância do axios
const api = axios.create({
  baseURL: 'http://localhost:5000/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para requisições
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para respostas
api.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

const ApiService = {
  // PRODUTOS
  products: {
    getAll: () => api.get('/products/'),
    getById: (id) => api.get(`/products/${id}`),
    create: (data) => api.post('/products/', data),
    update: (id, data) => api.put(`/products/${id}`, data),
    delete: (id) => api.delete(`/products/${id}`),
  },

  // CUPONS
  coupons: {
    getAll: () => api.get('/coupons/'),
    getById: (id) => api.get(`/coupons/${id}`),
    create: (data) => api.post('/coupons/', data),
    update: (id, data) => api.put(`/coupons/${id}`, data),
    delete: (id) => api.delete(`/coupons/${id}`),
  },

  // HEALTH CHECK
  healthCheck: () => api.get('/health/'),
};

export default ApiService;