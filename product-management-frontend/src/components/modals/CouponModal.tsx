import React, { useState } from 'react';
import Modal from '../common/Modal';
import type { Coupon } from '../../types';
import { Tag } from 'lucide-react';

interface CouponModalProps {
  isOpen: boolean;
  onSuccess: () => void;
  onClose: () => void;
  onApply: (couponCode: string) => void;
  coupons: Coupon[];
  isLoading: boolean;
  productId: number;
}

const CouponModal: React.FC<CouponModalProps> = ({ 
  isOpen, 
  onClose, 
  onApply, 
  coupons, 
  isLoading 
}) => {
  const [selectedCoupon, setSelectedCoupon] = useState<string>('');
  const [error, setError] = useState<string>('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!selectedCoupon.trim()) {
      setError('Selecione um cupom');
      return;
    }

    // Verificar se o cupom está ativo
    const coupon = coupons.find(c => c.code === selectedCoupon);
    if (coupon && !coupon.is_active) {
      setError('Este cupom não está ativo');
      return;
    }

    setError('');
    onApply(selectedCoupon);
  };

  const handleClose = () => {
    setSelectedCoupon('');
    setError('');
    onClose();
  };

  const handleCouponChange = (value: string) => {
    setSelectedCoupon(value);
    if (error) setError(''); // Limpar erro ao selecionar
  };

  // Filtrar apenas cupons ativos
  const activeCoupons = coupons.filter(coupon => coupon.is_active);

  // Obter informações do cupom selecionado
  const selectedCouponInfo = activeCoupons.find(c => c.code === selectedCoupon);

  return (
    <Modal isOpen={isOpen} onClose={handleClose} title="Aplicar Cupom de Desconto">
      <form onSubmit={handleSubmit} className="space-y-4">
        {activeCoupons.length === 0 ? (
          <div className="text-center py-8">
            <Tag className="mx-auto h-12 w-12 text-gray-400 mb-4" />
            <p className="text-gray-500 mb-2">Nenhum cupom disponível</p>
            <p className="text-sm text-gray-400">
              Não há cupons ativos no momento
            </p>
          </div>
        ) : (
          <>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Selecionar Cupom
              </label>
              <select
                value={selectedCoupon}
                onChange={(e) => handleCouponChange(e.target.value)}
                className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 ${
                  error ? 'border-red-500' : 'border-gray-300'
                }`}
                disabled={isLoading}
              >
                <option value="">Selecione um cupom</option>
                {activeCoupons.map(coupon => (
                  <option key={coupon.code} value={coupon.code}>
                    {coupon.code} - {coupon.discount_percent}% de desconto
                  </option>
                ))}
              </select>
              {error && (
                <p className="mt-1 text-sm text-red-600">{error}</p>
              )}
            </div>

            {/* Lista visual dos cupons */}
            <div className="max-h-40 overflow-y-auto">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Cupons disponíveis:
              </label>
              <div className="space-y-2">
                {activeCoupons.map(coupon => (
                  <div
                    key={coupon.code}
                    onClick={() => handleCouponChange(coupon.code)}
                    className={`p-3 border rounded-md cursor-pointer transition-colors ${
                      selectedCoupon === coupon.code
                        ? 'border-purple-500 bg-purple-50'
                        : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                    }`}
                  >
                    <div className="flex justify-between items-center">
                      <div>
                        <div className="font-medium text-gray-900">
                          {coupon.code}
                        </div>
                        <div className="text-sm text-gray-500">
                          {coupon.discount_percent}% de desconto
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                          -{coupon.discount_percent}%
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Preview do cupom selecionado */}
            {selectedCouponInfo && (
              <div className="bg-purple-50 border border-purple-200 rounded-md p-3">
                <p className="text-sm text-purple-700">
                  <strong>Cupom selecionado:</strong> {selectedCouponInfo.code}
                </p>
                <p className="text-sm text-purple-600">
                  Desconto de {selectedCouponInfo.discount_percent}% será aplicado ao produto
                </p>
              </div>
            )}
          </>
        )}
        
        <div className="flex gap-3 pt-4 border-t">
          <button
            type="submit"
            disabled={isLoading || !selectedCoupon.trim() || activeCoupons.length === 0}
            className="flex-1 bg-purple-500 text-white py-2 px-4 rounded-md hover:bg-purple-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
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
              'Aplicar Cupom'
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

export default CouponModal;