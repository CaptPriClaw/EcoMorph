// src/components/ProductCard.jsx
import React from 'react';
import { Link } from 'react--router-dom';
import './ProductCard.css';

/**
 * A card component to display a summary of a single product.
 * @param {object} props
 * @param {object} props.product - The product object to display.
 */
function ProductCard({ product }) {
  if (!product) {
    return null;
  }

  return (
    <Link to={`/product/${product.id}`} className="product-card-link">
      <div className="product-card">
        <div className="product-card-image-container">
          <img
            src={product.image_url}
            alt={product.name}
            className="product-card-image"
          />
        </div>
        <div className="product-card-info">
          <h3 className="product-card-name">{product.name}</h3>
          <p className="product-card-price">{product.price_points} EcoPoints</p>
        </div>
      </div>
    </Link>
  );
}

export default ProductCard;