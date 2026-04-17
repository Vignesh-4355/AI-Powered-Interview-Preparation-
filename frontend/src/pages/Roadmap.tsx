import { Link } from 'react-router-dom';
import { Map, ArrowLeft } from 'lucide-react';
import './ModulePage.css';

const Roadmap = () => {
  return (
    <div className="module-page-container">
      <div className="module-header">
        <Link to="/dashboard" className="back-button">
          <ArrowLeft size={20} />
          Back to Dashboard
        </Link>
        <div className="module-icon-large">
          <Map size={64} />
        </div>
        <h1>Personalized Roadmap</h1>
        <p className="module-subtitle">
          Follow a customized learning path tailored to your target role and experience level.
        </p>
      </div>
      
      <div className="module-content">
        <div className="coming-soon">
          <h2>🗺️ Coming Soon</h2>
          <p>We're designing personalized roadmaps with:</p>
          <ul>
            <li>Role-specific learning paths</li>
            <li>Skill gap analysis</li>
            <li>Progress tracking and milestones</li>
            <li>Adaptive recommendations based on your goals</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Roadmap;
