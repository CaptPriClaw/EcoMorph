// src/pages/Marketplace.jsx
import React, { useState, useEffect } from 'react';
import productService from '../api/productService';
import ProductCard from '../components/ProductCard';
import './Marketplace.css';

function Marketplace() {
  // State to hold the list of products
  const [products, setProducts] = useState([]);
  // State to handle loading status
  const [loading, setLoading] = useState(true);
  // State to handle any errors during data fetching
  const [error, setError] = useState(null);

  // useEffect hook to fetch data when the component mounts
  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setLoading(true);
        const fetchedProducts = await productService.getAllProducts();
        setProducts(fetchedProducts);
      } catch (err) {
        setError('Failed to load products. Please try again later.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []); // The empty dependency array means this runs once on mount

  // Conditional rendering based on the state
  if (loading) {
    return <div className="page-container"><p>Loading products...</p></div>;
  }

  if (error) {
    return <div className="page-container"><p className="error-message">{error}</p></div>;
  }

  return (
    <div className="page-container marketplace-page">
      <h1 className="page-title">Marketplace</h1>
      <p className="page-subtitle">Discover unique items handcrafted from upcycled materials.</p>

      {products.length === 0 ? (
        <p>No products are available at the moment. Check back soon!</p>
      ) : (
        <div className="product-grid">
          {products.map(product => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      )}
    </div>
  );
}

export default Marketplace;