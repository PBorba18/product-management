import { useEffect, useState } from 'react';
import { ProductsService } from '../api/services/ProductsService';
import type { ProductOutput } from '../api/models/ProductOutput';
import { toast } from 'react-toastify';

export default function ProductList() {
  const [products, setProducts] = useState<ProductOutput[]>([]);

  const loadProducts = async () => {
    try {
      const response = await ProductsService.listProducts();
      const data = response.data || []; // ✅ protege contra undefined
      setProducts(data);
    } catch (err) {
      console.error('Erro ao carregar produtos:', err);
      toast.error('Erro ao carregar produtos');
    }
  };

  useEffect(() => {
    loadProducts();
  }, []);

  return (
    <div className="max-w-6xl mx-auto bg-white p-6 rounded shadow">
      <h3 className="text-xl font-semibold mb-4">Produtos Cadastrados</h3>

      {products.length === 0 ? (
        <p className="text-gray-500">Nenhum produto encontrado.</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full border border-gray-200 text-sm">
            <thead className="bg-gray-100 text-left">
              <tr>
                <th className="p-2 border-b">Nome</th>
                <th className="p-2 border-b">Descrição</th>
                <th className="p-2 border-b">Preço</th>
                <th className="p-2 border-b">Preço Final</th>
                <th className="p-2 border-b">Estoque</th>
                <th className="p-2 border-b">Ações</th>
              </tr>
            </thead>
            <tbody>
              {products.map((p) => (
                <tr key={p.id} className="hover:bg-gray-50">
                  <td className="p-2 border-b">{p.name}</td>
                  <td className="p-2 border-b">{p.description}</td>
                  <td className="p-2 border-b">R$ {p.price?.toFixed(2)}</td>
                  <td className="p-2 border-b">
                    {p.finalPrice && p.finalPrice < p.price!
                      ? `R$ ${p.finalPrice.toFixed(2)}`
                      : '—'}
                  </td>
                  <td className="p-2 border-b">{p.stock}</td>
                  <td className="p-2 border-b">
                    <button className="text-blue-600 hover:underline mr-3">Editar</button>
                    <button className="text-red-600 hover:underline">Excluir</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
