// src/pages/DashboardUpcycler.jsx
import React, { useState, useEffect } from 'react';
import productService from '../api/productService';
import { useAuth } from '../hooks/useAuth';
import Button from '../components/common/Button';
import './Dashboard.css'; // Reusing the same stylesheet

function DashboardUpcycler() {
  // Form state
  const [formData, setFormData] = useState({ name: '', description: '', price_points: '', imageFile: null });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitMessage, setSubmitMessage] = useState('');

  // List state
  const [myProducts, setMyProducts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  const { user } = useAuth();

  const fetchMyProducts = async () => {
    try {
      setIsLoading(true);
      const data = await productService.getMyListings();
      setMyProducts(data);
    } catch (error) {
      console.error("Failed to fetch products:", error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchMyProducts();
  }, []);

  const handleChange = (e) => {
    const { name, value, files } = e.target;
    if (name === 'imageFile') {
      setFormData(prev => ({ ...prev, imageFile: files[0] }));
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.imageFile) {
      setSubmitMessage('Please select an image for your product.');
      return;
    }

    setIsSubmitting(true);
    setSubmitMessage('Listing product...');

    try {
      await productService.createProduct(formData);
      setSubmitMessage('Product listed successfully!');

      // Clear form and refresh list
      setFormData({ name: '', description: '', price_points: '', imageFile: null });
      e.target.reset();
      await fetchMyProducts();

    } catch (error) {
      setSubmitMessage('Failed to list product. Please try again.');
      console.error(error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="page-container dashboard">
      <h1 className="dashboard-title">Upcycler Dashboard</h1>
      <p>Welcome, {user?.full_name || user?.email}! Create new product listings for the marketplace here.</p>

      <div className="dashboard-layout">
        <div className="dashboard-section">
          <h2>Create New Product Listing</h2>
          <form onSubmit={handleSubmit} className="dashboard-form">
            <div className="form-group">
              <label htmlFor="name">Product Name</label>
              <input id="name" name="name" type="text" value={formData.name} onChange={handleChange} required />
            </div>
            <div className="form-group">
              <label htmlFor="description">Description</label>
              <textarea id="description" name="description" value={formData.description} onChange={handleChange} rows="3" required></textarea>
            </div>
            <div className="form-group">
              <label htmlFor="price_points">Price (in EcoPoints)</label>
              <input id="price_points" name="price_points" type="number" value={formData.price_points} onChange={handleChange} required />
            </div>
            <div className="form-group">
              <label htmlFor="imageFile">Product Image</label>
              <input id="imageFile" name="imageFile" type="file" onChange={handleChange} accept="image/*" required />
            </div>
            <Button type="submit" disabled={isSubmitting}>
              {isSubmitting ? 'Listing...' : 'List Product'}
            </Button>
            {submitMessage && <p className="submit-message">{submitMessage}</p>}
          </form>
        </div>

        <div className="dashboard-section">
          <h2>My Product Listings</h2>
          <div className="submission-list">
            {isLoading ? (
              <p>Loading products...</p>
            ) : myProducts.length === 0 ? (
              <p>You haven't listed any products yet.</p>
            ) : (
              <table>
                <thead>
                  <tr>
                    <th>Product Name</th>
                    <th>Price</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {myProducts.map((product) => (
                    <tr key={product.id}>
                      <td>{product.name}</td>
                      <td>{product.price_points} EcoPoints</td>
                      <td className={`status status-${product.status.toLowerCase()}`}>{product.status}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default DashboardUpcycler;