// src/pages/HomePage.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import Button from '../components/common/Button';
import './HomePage.css';

function HomePage() {
  return (
    <div className="home-page">
      <header className="hero-section">
        <div className="hero-content">
          <h1>Turn Waste Into Wonder</h1>
          <p className="subtitle">Join a community of creators and contribute to a sustainable future by upcycling everyday items.</p>
          <div className="hero-actions">
            <Link to="/marketplace">
              <Button variant="primary">Explore Marketplace</Button>
            </Link>
            <Link to="/register">
              <Button variant="secondary">Get Started</Button>
            </Link>
          </div>
        </div>
      </header>

      <section className="how-it-works">
        <h2>How It Works</h2>
        <div className="steps-container">
          <div className="step">
            <div className="step-icon">♻️</div>
            <h3>1. Submit Waste</h3>
            <p>Upload a photo of your usable waste materials like plastic bottles, glass jars, or old fabrics.</p>
          </div>
          <div className="step">
            <div className="step-icon">✨</div>
            <h3>2. Earn Points</h3>
            <p>Once your submission is approved, you earn EcoPoints that you can use as currency in our marketplace.</p>
          </div>
          <div className="step">
            <div className="step-icon">🛍️</div>
            <h3>3. Shop Products</h3>
            <p>Spend your EcoPoints on unique, handcrafted items made by talented upcyclers from our community.</p>
          </div>
        </div>
      </section>
    </div>
  );
}

export default HomePage;