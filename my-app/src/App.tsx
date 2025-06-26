import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ProductsPage from './pages/ProductsPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/produtos" element={<ProductsPage />} />
      </Routes>
    </Router>
  );
}

export default App;
