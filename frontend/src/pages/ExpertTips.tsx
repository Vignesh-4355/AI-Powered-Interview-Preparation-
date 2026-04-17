import { Link } from 'react-router-dom';
import { Lightbulb, ArrowLeft } from 'lucide-react';
import './ModulePage.css';

const ExpertTips = () => {
  return (
    <div className="module-page-container">
      <div className="module-header">
        <Link to="/dashboard" className="back-button">
          <ArrowLeft size={20} />
          Back to Dashboard
        </Link>
        <div className="module-icon-large">
          <Lightbulb size={64} />
        </div>
        <h1>Expert Tips</h1>
        <p className="module-subtitle">
          Learn from industry experts with curated tips, tricks, and strategies for interview success.
        </p>
      </div>
      
      <div className="module-content">
        <div className="coming-soon">
          <h2>💡 Coming Soon</h2>
          <p>We're curating expert content with:</p>
          <ul>
            <li>Tips from FAANG engineers</li>
            <li>Interview strategies that work</li>
            <li>Common mistakes to avoid</li>
            <li>Success stories and best practices</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default ExpertTips;
