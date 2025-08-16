// src/api/productService.js
import apiClient from './apiClient';

const productService = {
  /**
   * Fetches all available products from the marketplace.
   */
  getAllProducts: async () => {
    const response = await apiClient.get('/marketplace/');
    return response.data;
  },

  /**
   * Fetches the details for a single product by its ID.
   */
  getProductById: async (productId) => {
    const response = await apiClient.get(`/marketplace/${productId}`);
    return response.data;
  },

  /**
   * --- NEW FUNCTION ---
   * Fetches all product listings for the current authenticated upcycler.
   */
  getMyListings: async () => {
    const response = await apiClient.get('/products/my-listings');
    return response.data;
  },

  /**
   * --- UPDATED FUNCTION ---
   * Creates a new product listing, now with image upload support.
   */
  createProduct: async (productData) => {
    const formData = new FormData();
    formData.append('name', productData.name);
    formData.append('description', productData.description);
    formData.append('price_points', productData.price_points);
    formData.append('imageFile', productData.imageFile); // 'imageFile' should match backend field name

    const response = await apiClient.post('/products/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  /**
   * Purchases a product.
   */
  buyProduct: async (productId) => {
    const response = await apiClient.post(`/marketplace/buy/${productId}`);
    return response.data;
  },
};

export default productService;