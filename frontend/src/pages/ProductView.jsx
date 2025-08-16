// src/pages/ProductView.jsx
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import productService from '../api/productService';
import { useAuth } from '../hooks/useAuth';
import { usePoints } from '../contexts/PointContext';
import Button from '../components/common/Button';
import './ProductView.css';

function ProductView() {
  const { id } = useParams(); // Gets the product ID from the URL (e.g., /product/123)
  const navigate = useNavigate();
  const { user, isAuthenticated } = useAuth();
  const { refreshPoints } = usePoints();

  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [purchaseStatus, setPurchaseStatus] = useState('');

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        setLoading(true);
        const fetchedProduct = await productService.getProductById(id);
        setProduct(fetchedProduct);
      } catch (err) {
        setError('Could not find the requested product.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchProduct();
  }, [id]); // Re-fetch if the ID in the URL changes

  const handleBuy = async () => {
    if (!isAuthenticated) {
      navigate('/login'); // Redirect to login if not authenticated
      return;
    }

    try {
      setPurchaseStatus('Processing...');
      await productService.buyProduct(id);
      setPurchaseStatus('Purchase successful! Thank you.');
      await refreshPoints(); // Update the user's point balance in the navbar
    } catch (err) {
      setPurchaseStatus(err.response?.data?.detail || 'Purchase failed. Please try again.');
      console.error(err);
    }
  };

  if (loading) {
    return <div className="page-container"><p>Loading product...</p></div>;
  }

  if (error) {
    return <div className="page-container"><p className="error-message">{error}</p></div>;
  }

  if (!product) {
    return null; // Should not happen if loading and error are handled
  }

  // Check if the current user is the seller of the product
  const isSeller = user && user.id === product.upcycler_id;

  return (
    <div className="page-container product-view-page">
      <div className="product-view-layout">
        <div className="product-view-image-container">
          <img src={product.image_url} alt={product.name} className="product-view-image" />
        </div>
        <div className="product-view-details">
          <h1 className="product-view-title">{product.name}</h1>
          <p className="product-view-price">{product.price_points} EcoPoints</p>
          <p className="product-view-description">{product.description}</p>

          <div className="product-view-actions">
            {product.status === 'available' && !isSeller && (
              <Button onClick={handleBuy} disabled={!isAuthenticated || purchaseStatus}>
                {purchaseStatus ? purchaseStatus : 'Buy Now'}
              </Button>
            )}
            {product.status === 'sold' && (
              <p className="status-sold">This item has been sold.</p>
            )}
            {isSeller && (
              <p className="status-seller">This is your own listing.</p>
            )}
            {!isAuthenticated && (
                <p>Please <a href="/login">log in</a> to purchase.</p>
            )}
          </div>
          {purchaseStatus && <p className="purchase-status-message">{purchaseStatus}</p>}
        </div>
      </div>
    </div>
  );
}

export default ProductView;