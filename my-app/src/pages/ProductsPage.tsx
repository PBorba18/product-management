// src/pages/ProductsPage.tsx
import { useEffect, useState } from 'react';
import { ProductsService } from '../api/services/ProductsService';
import type { ProductOutput } from '../api/models/ProductOutput';
import ProductForm from '../components/ProductForm';
import { FaTrash, FaEdit, FaDollarSign } from 'react-icons/fa';
import { toast } from 'react-toastify';

export default function ProductsPage() {
  const [products, setProducts] = useState<ProductOutput[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [editingProduct, setEditingProduct] = useState<ProductOutput | undefined>(undefined);

  const fetchProducts = async () => {
    try {
      const response = await ProductsService.listProducts();
      setProducts(response.data || []);
    } catch (error) {
      console.error('Erro ao buscar produtos:', error);
      toast.error('Erro ao carregar produtos');
    }
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  const handleDelete = async (id: number) => {
    if (confirm('Deseja apagar este produto?')) {
      try {
        await ProductsService.deleteProduct(id);
        toast.success('Produto apagado com sucesso!');
        fetchProducts();
      } catch (error) {
        console.error('Erro ao apagar produto:', error);
        toast.error('Erro ao apagar produto');
      }
    }
  };

  const handleApplyCoupon = async (id: number) => {
    const couponCode = prompt('Digite o código do cupom:');
    if (couponCode) {
      try {
        await ProductsService.applyCouponDiscount(id, { code: couponCode });
        toast.success('Cupom aplicado com sucesso!');
        fetchProducts();
      } catch (error) {
        toast.error('Erro ao aplicar cupom');
        console.error(error);
      }
    }
  };

  return (
    <div className="page-container max-w-6xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-4">Produtos</h2>

      <button
        onClick={() => {
          setEditingProduct(undefined);
          setShowForm(true);
        }}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition mb-6"
      >
        + Novo Produto
      </button>

      {showForm && (
        <ProductForm
          initialData={editingProduct}
          onSuccess={() => {
            setShowForm(false);
            setEditingProduct(undefined);
            fetchProducts();
          }}
        />
      )}

      <table className="w-full border-collapse border border-gray-300">
        <thead>
          <tr className="bg-gray-200">
            <th className="border border-gray-300 p-2 text-left">Nome</th>
            <th className="border border-gray-300 p-2 text-left">Descrição</th>
            <th className="border border-gray-300 p-2 text-right">Preço</th>
            <th className="border border-gray-300 p-2 text-right">Preço Final</th>
            <th className="border border-gray-300 p-2 text-right">Estoque</th>
            <th className="border border-gray-300 p-2 text-center">Ações</th>
          </tr>
        </thead>
        <tbody>
          {products.map((p) => (
            <tr key={p.id} className="even:bg-gray-50">
              <td className="border border-gray-300 p-2">{p.name}</td>
              <td className="border border-gray-300 p-2">{p.description}</td>
              <td className="border border-gray-300 p-2 text-right">
                R$ {p.price?.toFixed(2)}
              </td>
              <td className="border border-gray-300 p-2 text-right">
                {p.finalPrice && p.finalPrice !== p.price
                  ? `R$ ${p.finalPrice?.toFixed(2)}`
                  : '—'}
              </td>
              <td className="border border-gray-300 p-2 text-right">{p.stock}</td>
              <td className="border border-gray-300 p-2 text-center space-x-2">
                <button
                  onClick={() => {
                    setEditingProduct(p);
                    setShowForm(true);
                  }}
                  title="Editar"
                  className="text-blue-600 hover:text-blue-800"
                >
                  <FaEdit />
                </button>

                <button
                  onClick={() => handleApplyCoupon(p.id!)}
                  title="Aplicar Cupom"
                  className="text-green-600 hover:text-green-800"
                >
                  <FaDollarSign />
                </button>

                <button
                  onClick={() => handleDelete(p.id!)}
                  title="Excluir"
                  className="text-red-600 hover:text-red-800"
                >
                  <FaTrash />
                </button>
              </td>
            </tr>
          ))}
          {products.length === 0 && (
            <tr>
              <td colSpan={6} className="text-center p-4">
                Nenhum produto encontrado.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
