// sneakerhead/frontend-service/src/pages/Home.jsx
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import productService from '../services/productService';
import ProductCard from '../components/ProductCard';

const BRANDS = [
  { name: 'Nike', logo: '✓' },
  { name: 'Adidas', logo: '⊞' },
  { name: 'Jordan', logo: '🏀' },
  { name: 'New Balance', logo: 'NB' },
  { name: 'Puma', logo: '🐆' },
  { name: 'Asics', logo: 'ᴬ' },
  { name: 'Reebok', logo: 'Ⓡ' },
  { name: 'Converse', logo: '★' },
];

const CATEGORIES = [
  { name: 'Running', emoji: '🏃', color: '#e8ff00' },
  { name: 'Basketball', emoji: '🏀', color: '#ff6b35' },
  { name: 'Lifestyle', emoji: '🔥', color: '#a855f7' },
  { name: 'Skate', emoji: '🛹', color: '#06b6d4' },
  { name: 'Training', emoji: '💪', color: '#22c55e' },
];

export default function Home() {
  const [featured, setFeatured] = useState([]);
  const [trending, setTrending] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const [featuredRes, trendingRes] = await Promise.all([
          productService.getFeatured(4),
          productService.getProducts({ sort_by: 'popular', limit: 8 }),
        ]);
        setFeatured(featuredRes.data);
        setTrending(trendingRes.data.products || []);
      } catch (err) {
        console.error('Failed to load home data:', err);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  return (
    <div className="home-page">
      {/* Hero Section */}
      <section className="hero">
        <div className="hero-content">
          <h1 className="hero-title">
            STEP INTO<br />THE <span className="accent">CULTURE</span>
          </h1>
          <p className="hero-subtitle">
            Discover the latest drops from the world's most iconic sneaker brands. 
            Authentic. Premium. Delivered to your door.
          </p>
          <Link to="/products" className="hero-cta">
            Shop Now
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M5 12h14M12 5l7 7-7 7" />
            </svg>
          </Link>
        </div>
        <div className="hero-visual">
          <div className="hero-shoe-animation">
            <div className="floating-shoe">👟</div>
            <div className="glow-ring"></div>
          </div>
        </div>
      </section>

      {/* Brand Carousel */}
      <section className="brand-carousel">
        <div className="carousel-track">
          {[...BRANDS, ...BRANDS].map((brand, i) => (
            <Link
              key={i}
              to={`/products?brand=${brand.name}`}
              className="brand-item"
            >
              <span className="brand-logo">{brand.logo}</span>
              <span className="brand-name">{brand.name}</span>
            </Link>
          ))}
        </div>
      </section>

      {/* Latest Drops */}
      <section className="section">
        <div className="section-header">
          <h2 className="section-title">Latest <span className="accent">Drops</span></h2>
          <Link to="/products?sort_by=newest" className="section-link">View All →</Link>
        </div>
        <div className="product-grid-4">
          {loading
            ? Array(4).fill(0).map((_, i) => <div key={i} className="product-skeleton" />)
            : featured.map((p) => <ProductCard key={p.id} product={p} />)}
        </div>
      </section>

      {/* Category Tiles */}
      <section className="section">
        <h2 className="section-title">Shop by <span className="accent">Category</span></h2>
        <div className="category-tiles">
          {CATEGORIES.map((cat) => (
            <Link
              key={cat.name}
              to={`/products?category=${cat.name}`}
              className="category-tile"
              style={{ '--tile-color': cat.color }}
            >
              <span className="cat-emoji">{cat.emoji}</span>
              <span className="cat-name">{cat.name}</span>
            </Link>
          ))}
        </div>
      </section>

      {/* Trending Now */}
      <section className="section">
        <div className="section-header">
          <h2 className="section-title">Trending <span className="accent">Now</span></h2>
          <Link to="/products?sort_by=popular" className="section-link">See More →</Link>
        </div>
        <div className="trending-scroll">
          {trending.map((p) => (
            <div key={p.id} className="trending-item">
              <ProductCard product={p} />
            </div>
          ))}
        </div>
      </section>

      {/* Trust Banner */}
      <section className="trust-banner">
        <div className="trust-item">
          <span className="trust-icon">✓</span>
          <span>100% Authentic</span>
        </div>
        <div className="trust-item">
          <span className="trust-icon">↩</span>
          <span>Free Returns</span>
        </div>
        <div className="trust-item">
          <span className="trust-icon">🔒</span>
          <span>Secure Checkout</span>
        </div>
      </section>
    </div>
  );
}
