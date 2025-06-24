import React from 'react';
import { RefreshCw } from 'lucide-react';

const LoadingSpinner: React.FC = () => (
  <div className="flex justify-center items-center py-8">
    <RefreshCw className="animate-spin h-8 w-8 text-blue-500" />
  </div>
);

export default LoadingSpinner;