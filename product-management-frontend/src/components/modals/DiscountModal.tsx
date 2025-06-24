import React, { useState } from 'react';
import Modal from '../common/Modal';

interface DiscountModalProps {
  isOpen: boolean;
  productId: number;
  onClose: () => void;
  onApply: (percent: number) => void;
  isLoading: boolean;
}

const DiscountModal: React.FC<DiscountModalProps> = ({ 
  isOpen, 
  
  onClose, 
  onApply, 
  isLoading 
}) => {
  const [percent, setPercent] = useState<string>('');
  const [error, setError] = useState<string>('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    const percentValue = parseFloat(percent);
    
    if (!percent.trim()) {
      setError('Percentual é obrigatório');
      return;
    }
    
    if (isNaN(percentValue)) {
      setError('Percentual deve ser um número válido');
      return;
    }
    
    if (percentValue <= 0) {
      setError('Percentual deve ser maior que zero');
      return;
    }
    
    if (percentValue > 100) {
      setError('Percentual não pode ser maior que 100%');
      return;
    }

    setError('');
    onApply(percentValue);
  };

  const handleClose = () => {
    setPercent('');
    setError('');
    onClose();
  };

  const handlePercentChange = (value: string) => {
    setPercent(value);
    if (error) setError('');
  };

  const quickDiscounts = [5, 10, 15, 20, 25, 30];

  return (
    <Modal isOpen={isOpen} onClose={handleClose} title="Aplicar Desconto Percentual">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Percentual de Desconto (%)
          </label>
          <input
            type="number"
            step="0.01"
            min="0.01"
            max="100"
            value={percent}
            onChange={(e) => handlePercentChange(e.target.value)}
            className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 ${
              error ? 'border-red-500' : 'border-gray-300'
            }`}
            placeholder="Ex: 10, 15, 20..."
            disabled={isLoading}
            autoFocus
          />
          {error && (
            <p className="mt-1 text-sm text-red-600">{error}</p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Sugestões rápidas:
          </label>
          <div className="flex flex-wrap gap-2">
            {quickDiscounts.map((discount) => (
              <button
                key={discount}
                type="button"
                onClick={() => handlePercentChange(discount.toString())}
                className="px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 transition-colors"
                disabled={isLoading}
              >
                {discount}%
              </button>
            ))}
          </div>
        </div>

        {percent && !error && !isNaN(parseFloat(percent)) && (
          <div className="bg-green-50 border border-green-200 rounded-md p-3">
            <p className="text-sm text-green-700">
              <strong>Preview:</strong> Desconto de {percent}% será aplicado ao produto
            </p>
          </div>
        )}
        
        <div className="flex gap-3 pt-4 border-t">
          <button
            type="submit"
            disabled={isLoading || !percent.trim()}
            className="flex-1 bg-green-500 text-white py-2 px-4 rounded-md hover:bg-green-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <span className="flex items-center justify-center">
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Aplicando...
              </span>
            ) : (
              'Aplicar Desconto'
            )}
          </button>
          <button
            type="button"
            onClick={handleClose}
            disabled={isLoading}
            className="flex-1 bg-gray-300 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-400 transition-colors disabled:opacity-50"
          >
            Cancelar
          </button>
        </div>
      </form>
    </Modal>
  );
};

export default DiscountModal;
