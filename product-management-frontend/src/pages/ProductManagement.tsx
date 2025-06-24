import React, { useState, useEffect } from 'react';
import { Search, Plus, Edit, Trash2, Percent, Tag, X } from 'lucide-react';

// Componentes
import Modal from '../components/common/Modal';
import LoadingSpinner from '../components/common/LoadingSpinner';
import ProductForm from '../components/forms/ProductForm';
import DiscountModal from '../components/modals/DiscountModal';
import CouponModal from '../components/modals/CouponModal';

// Types e Services
// Types e Services
import type { Product, Coupon, ProductFilters, ProductFormData } from '../types';
import { productApi, couponApi } from '../services/api';
import { formatPrice } from '../utils/formatters';

const ProductManagement: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [coupons, setCoupons] = useState<Coupon[]>([]);
  const [loading, setLoading] = useState(false);
  const [actionLoading, setActionLoading] = useState(false);

  const [filters, setFilters] = useState<ProductFilters>({});
  const [minPrice, setMinPrice] = useState('');
  const [maxPrice, setMaxPrice] = useState('');
  const [searchName, setSearchName] = useState('');

  const [productModal, setProductModal] = useState<{ isOpen: boolean; product?: Product }>({ isOpen: false });
  const [discountModal, setDiscountModal] = useState<{ isOpen: boolean; productId?: number }>({ isOpen: false });
  const [couponModal, setCouponModal] = useState<{ isOpen: boolean; productId?: number }>({ isOpen: false });

  const [message, setMessage] = useState<{ text: string; type: 'success' | 'error' } | null>(null);

  useEffect(() => {
    loadProducts();
    loadCoupons();
  }, []);

  useEffect(() => {
    loadProducts();
  }, [filters]);

  const loadProducts = async () => {
    setLoading(true);
    try {
      const data = await productApi.getProducts(filters);
      setProducts(data);
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    } catch (error) {
      showMessage('Erro ao carregar produtos', 'error');
    } finally {
      setLoading(false);
    }
  };

  const loadCoupons = async () => {
    try {
      const data = await couponApi.getCoupons();
      setCoupons(data);
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    } catch (error) {
      showMessage('Erro ao carregar cupons', 'error');
    }
  };

  const showMessage = (text: string, type: 'success' | 'error') => {
    setMessage({ text, type });
    setTimeout(() => setMessage(null), 3000);
  };

  const handleAddProduct = () => {
    setProductModal({ isOpen: true });
  };

  const handleEditProduct = (product: Product) => {
    setProductModal({ isOpen: true, product });
  };

  const handleDeleteProduct = async (id: number) => {
    if (!confirm('Deseja realmente excluir este produto?')) return;
    setActionLoading(true);
    try {
      await productApi.deleteProduct(id);
      showMessage('Produto excluído com sucesso', 'success');
      loadProducts();
    } catch {
      showMessage('Erro ao excluir produto', 'error');
    } finally {
      setActionLoading(false);
    }
  };

  const handleFormSubmit = async (data: ProductFormData) => {
    setActionLoading(true);
    try {
      if (productModal.product) {
        await productApi.updateProduct(productModal.product.id, data);
        showMessage('Produto atualizado com sucesso', 'success');
      } else {
        await productApi.createProduct(data);
        showMessage('Produto criado com sucesso', 'success');
      }
      setProductModal({ isOpen: false });
      loadProducts();
    } catch {
      showMessage('Erro ao salvar produto', 'error');
    } finally {
      setActionLoading(false);
    }
  };

  const handleApplyDiscount = (productId: number) => {
    setDiscountModal({ isOpen: true, productId });
  };

  const handleApplyCoupon = (productId: number) => {
    setCouponModal({ isOpen: true, productId });
  };

  const handleFilterChange = () => {
    const f: ProductFilters = {};
    if (searchName) f.name = searchName;
    if (minPrice) f.min_price = Number(minPrice);
    if (maxPrice) f.max_price = Number(maxPrice);
    setFilters(f);
  };

  const handleClearFilters = () => {
    setSearchName('');
    setMinPrice('');
    setMaxPrice('');
    setFilters({});
  };

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Gerenciamento de Produtos</h1>

      {/* Filtros */}
      <div className="flex gap-2 flex-wrap mb-4">
        <input
          type="text"
          placeholder="Buscar por nome"
          className="border rounded p-2"
          value={searchName}
          onChange={(e) => setSearchName(e.target.value)}
        />
        <input
          type="number"
          placeholder="Preço mínimo"
          className="border rounded p-2"
          value={minPrice}
          onChange={(e) => setMinPrice(e.target.value)}
        />
        <input
          type="number"
          placeholder="Preço máximo"
          className="border rounded p-2"
          value={maxPrice}
          onChange={(e) => setMaxPrice(e.target.value)}
        />
        <button onClick={handleFilterChange} className="flex items-center gap-1 px-3 py-2 bg-blue-600 text-white rounded">
          <Search size={16} /> Filtrar
        </button>
        <button onClick={handleClearFilters} className="flex items-center gap-1 px-3 py-2 bg-gray-400 text-white rounded">
          <X size={16} /> Limpar
        </button>
        <button onClick={handleAddProduct} className="ml-auto flex items-center gap-1 px-3 py-2 bg-green-600 text-white rounded">
          <Plus size={16} /> Adicionar Produto
        </button>
      </div>

      {/* Feedback */}
      {message && (
        <div className={`mb-4 p-2 rounded ${message.type === 'success' ? 'bg-green-200' : 'bg-red-200'}`}>
          {message.text}
        </div>
      )}

      {/* Carregando */}
      {loading ? (
        <LoadingSpinner />
      ) : (
        <table className="w-full border">
          <thead>
            <tr className="bg-gray-100">
              <th className="p-2 text-left">ID</th>
              <th className="p-2 text-left">Nome</th>
              <th className="p-2 text-left">Preço</th>
              <th className="p-2 text-left">Ações</th>
            </tr>
          </thead>
          <tbody>
            {products.map((p) => (
              <tr key={p.id} className="border-t">
                <td className="p-2">{p.id}</td>
                <td className="p-2">{p.name}</td>
                <td className="p-2">{formatPrice(p.price)}</td>
                <td className="p-2 flex gap-2 flex-wrap">
                  <button onClick={() => handleEditProduct(p)} className="text-blue-600"><Edit size={16} /></button>
                  <button onClick={() => handleDeleteProduct(p.id)} className="text-red-600"><Trash2 size={16} /></button>
                  <button onClick={() => handleApplyDiscount(p.id)} className="text-green-600"><Percent size={16} /></button>
                  <button onClick={() => handleApplyCoupon(p.id)} className="text-purple-600"><Tag size={16} /></button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {/* Modais */}
      {productModal.isOpen && (
       <Modal
  isOpen={productModal.isOpen}
  title={productModal.product ? 'Editar Produto' : 'Novo Produto'}
  onClose={() => setProductModal({ isOpen: false })}
>
  <ProductForm
  product={productModal.product}
  onSubmit={handleFormSubmit}
  onCancel={() => setProductModal({ isOpen: false })}
  isLoading={actionLoading}
/>

</Modal>

      )}

      {discountModal.isOpen && discountModal.productId && (
        <DiscountModal
  isOpen={discountModal.isOpen}
  productId={discountModal.productId!}
  isLoading={actionLoading}
  onClose={() => setDiscountModal({ isOpen: false })}
  onApply={handleApplyDiscount} // Use essa prop para disparar ação após aplicar o desconto
/>

      )}

      {couponModal.isOpen && couponModal.productId && (
        <CouponModal
          productId={couponModal.productId}
          coupons={coupons}
          onClose={() => setCouponModal({ isOpen: false })}
          onSuccess={() => {
            loadProducts();
            showMessage('Cupom aplicado com sucesso', 'success');
          }}
        />
      )}
    </div>
  );
};

export default ProductManagement;
