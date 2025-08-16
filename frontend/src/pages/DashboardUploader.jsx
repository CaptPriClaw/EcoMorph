// src/pages/DashboardUploader.jsx
import React, { useState, useEffect } from 'react';
import wasteService from '../api/wasteService';
import { useAuth } from '../hooks/useAuth';
import Button from '../components/common/Button';
import './Dashboard.css';

function DashboardUploader() {
  // Form state
  const [materialType, setMaterialType] = useState('');
  const [description, setDescription] = useState('');
  const [imageFile, setImageFile] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitMessage, setSubmitMessage] = useState('');

  // List state
  const [mySubmissions, setMySubmissions] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  const { user } = useAuth();

  // Function to fetch the user's submissions
  const fetchSubmissions = async () => {
    try {
      setIsLoading(true);
      const data = await wasteService.getMySubmissions();
      setMySubmissions(data);
    } catch (error) {
      console.error("Failed to fetch submissions:", error);
    } finally {
      setIsLoading(false);
    }
  };

  // Fetch submissions when the component mounts
  useEffect(() => {
    fetchSubmissions();
  }, []);

  const handleFileChange = (e) => {
    setImageFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!imageFile) {
      setSubmitMessage('Please select an image to upload.');
      return;
    }

    setIsSubmitting(true);
    setSubmitMessage('Submitting...');

    try {
      const wasteData = {
        material_type: materialType,
        description: description,
        imageFile: imageFile,
      };
      await wasteService.submitWaste(wasteData);
      setSubmitMessage('Submission successful!');

      // Clear the form and refresh the list
      setMaterialType('');
      setDescription('');
      setImageFile(null);
      e.target.reset(); // Resets the file input
      await fetchSubmissions();

    } catch (error) {
      setSubmitMessage('Submission failed. Please try again.');
      console.error(error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="page-container dashboard">
      <h1 className="dashboard-title">Uploader Dashboard</h1>
      <p>Welcome, {user?.full_name || user?.email}! Submit your waste materials here to earn EcoPoints.</p>

      <div className="dashboard-layout">
        {/* Left side: Submission Form */}
        <div className="dashboard-section">
          <h2>Submit New Waste</h2>
          <form onSubmit={handleSubmit} className="dashboard-form">
            <div className="form-group">
              <label htmlFor="materialType">Material Type (e.g., Plastic Bottle, T-Shirt)</label>
              <input id="materialType" type="text" value={materialType} onChange={(e) => setMaterialType(e.target.value)} required />
            </div>
            <div className="form-group">
              <label htmlFor="description">Brief Description</label>
              <textarea id="description" value={description} onChange={(e) => setDescription(e.target.value)} rows="3"></textarea>
            </div>
            <div className="form-group">
              <label htmlFor="imageFile">Upload Image</label>
              <input id="imageFile" type="file" onChange={handleFileChange} accept="image/*" required />
            </div>
            <Button type="submit" disabled={isSubmitting}>
              {isSubmitting ? 'Submitting...' : 'Submit Waste'}
            </Button>
            {submitMessage && <p className="submit-message">{submitMessage}</p>}
          </form>
        </div>

        {/* Right side: Submissions List */}
        <div className="dashboard-section">
          <h2>My Submissions</h2>
          <div className="submission-list">
            {isLoading ? (
              <p>Loading submissions...</p>
            ) : mySubmissions.length === 0 ? (
              <p>You haven't submitted any items yet.</p>
            ) : (
              <table>
                <thead>
                  <tr>
                    <th>Material</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {mySubmissions.map((item) => (
                    <tr key={item.id}>
                      <td>{item.material_type}</td>
                      <td className={`status status-${item.status.toLowerCase()}`}>{item.status.replace('_', ' ')}</td>
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

export default DashboardUploader;