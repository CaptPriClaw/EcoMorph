// src/api/wasteService.js
import apiClient from './apiClient';

const wasteService = {
  /**
   * Submits a new waste item, including an image file. (Requires authentication)
   * @param {object} wasteData - Contains material_type, description, and the image file.
   * @returns {Promise<object>} The newly created waste submission object.
   */
  submitWaste: async (wasteData) => {
    // File uploads must be sent as 'multipart/form-data'
    const formData = new FormData();

    // Append the text fields to the form data
    formData.append('material_type', wasteData.material_type);
    formData.append('description', wasteData.description);

    // Append the image file. 'image' should match the name of the File field in the backend.
    formData.append('image', wasteData.imageFile);

    const response = await apiClient.post('/waste/', formData, {
      headers: {
        // Axios will automatically set the correct 'Content-Type' for FormData,
        // so we don't need to specify it here.
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  /**
   * Fetches all waste submissions for the current authenticated user.
   * @returns {Promise<Array<object>>} A list of the user's waste submissions.
   */
  getMySubmissions: async () => {
    const response = await apiClient.get('/waste/my-submissions');
    return response.data;
  },
};

export default wasteService;