import { Link } from 'react-router-dom';
import './Home.css';

const Home = () => {
  return (
    <div className="home-container">
      <header className="home-header">
        <nav className="navbar">
          <div className="logo">
            <h1>🎯 AI Interview Prep</h1>
          </div>
          <div className="nav-links">
            <Link to="/login" className="btn btn-outline">Login</Link>
            <Link to="/register" className="btn btn-primary">Get Started</Link>
          </div>
        </nav>
      </header>

      <main className="hero-section">
        <div className="hero-content">
          <h2 className="hero-title">
            Ace Your Next Tech Interview with AI-Powered Preparation
          </h2>
          <p className="hero-subtitle">
            Practice with mock interviews, get personalized roadmaps, and improve your skills 
            with our AI-driven interview preparation platform.
          </p>
          <div className="hero-buttons">
            <Link to="/register" className="btn btn-primary btn-large">
              Start Preparing Now
            </Link>
            <Link to="#features" className="btn btn-outline btn-large">
              Learn More
            </Link>
          </div>
        </div>

        <div className="features-section" id="features">
          <h3>Key Features</h3>
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">🤖</div>
              <h4>AI Mock Interviews</h4>
              <p>Practice with AI-powered mock interviews that simulate real interview scenarios</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">📋</div>
              <h4>Company Insights</h4>
              <p>Get detailed information about top tech companies and their interview processes</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🗺️</div>
              <h4>Personalized Roadmaps</h4>
              <p>Follow customized learning paths based on your target role and experience level</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">📊</div>
              <h4>Analytics & Progress</h4>
              <p>Track your improvement with detailed analytics and performance insights</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">💬</div>
              <h4>24/7 Chatbot Support</h4>
              <p>Get instant answers to your questions with our AI chatbot assistant</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">📄</div>
              <h4>Resume Review</h4>
              <p>Optimize your resume with AI-powered suggestions and feedback</p>
            </div>
          </div>
        </div>
      </main>

      <footer className="home-footer">
        <p>&copy; 2026 AI Powered Interview Preparation Portal. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default Home;
