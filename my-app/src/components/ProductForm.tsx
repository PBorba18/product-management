// src/components/ProductForm.tsx
import { useState, useEffect } from 'react';
import { ProductsService } from '../api/services/ProductsService';
import type { ProductInput } from '../api/models/ProductInput';
import type { ProductOutput } from '../api/models/ProductOutput';
import { toast } from 'react-toastify';

type ProductFormProps = {
  initialData?: ProductOutput;  // opcional para edição
  onSuccess: () => void;
};

export default function ProductForm({ initialData, onSuccess }: ProductFormProps) {
  const [form, setForm] = useState<ProductInput>({
    name: '',
    description: '',
    price: 0.01,
    stock: 0,
  });

  useEffect(() => {
    if (initialData) {
      setForm({
        name: initialData.name || '',
        description: initialData.description || '',
        price: initialData.price || 0.01,
        stock: initialData.stock || 0,
      });
    }
  }, [initialData]);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: name === 'price' || name === 'stock' ? Number(value) : value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (form.price < 0.01) {
      toast.error('O preço deve ser no mínimo R$ 0,01');
      return;
    }

    try {
      if (initialData?.id) {
        await ProductsService.updateProduct(initialData.id, form);
        toast.success('Produto atualizado com sucesso!');
      } else {
        await ProductsService.createProduct(form);
        toast.success('Produto criado com sucesso!');
      }
      onSuccess();
      // Limpar formulário só se criar novo, se editar mantemos
      if (!initialData) {
        setForm({
          name: '',
          description: '',
          price: 0.01,
          stock: 0,
        });
      }
    } catch (err: unknown) {
      console.error(err);
      toast.error('Erro ao salvar produto');
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-white p-6 rounded shadow-md max-w-md mx-auto mb-8"
    >
      <h3 className="text-xl font-semibold mb-4">
        {initialData ? 'Editar Produto' : 'Novo Produto'}
      </h3>

      <label className="block mb-1 font-medium">Nome</label>
      <input
        name="name"
        value={form.name}
        onChange={handleChange}
        placeholder="Nome do produto"
        required
        className="w-full p-2 border border-gray-300 rounded mb-4"
      />

      <label className="block mb-1 font-medium">Descrição</label>
      <textarea
        name="description"
        value={form.description}
        onChange={handleChange}
        placeholder="Descrição"
        className="w-full p-2 border border-gray-300 rounded mb-4"
      />

      <label className="block mb-1 font-medium">Preço</label>
      <input
        name="price"
        type="number"
        step="0.01"
        min="0.01"
        value={form.price}
        onChange={handleChange}
        required
        className="w-full p-2 border border-gray-300 rounded mb-4"
      />

      <label className="block mb-1 font-medium">Estoque</label>
      <input
        name="stock"
        type="number"
        min="0"
        value={form.stock}
        onChange={handleChange}
        required
        className="w-full p-2 border border-gray-300 rounded mb-6"
      />

      <button
        type="submit"
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
      >
        {initialData ? 'Atualizar Produto' : 'Criar Produto'}
      </button>
    </form>
  );
}
