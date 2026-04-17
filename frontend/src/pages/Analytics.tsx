import { Link } from 'react-router-dom';
import { BarChart3, ArrowLeft } from 'lucide-react';
import './ModulePage.css';

const Analytics = () => {
  return (
    <div className="module-page-container">
      <div className="module-header">
        <Link to="/dashboard" className="back-button">
          <ArrowLeft size={20} />
          Back to Dashboard
        </Link>
        <div className="module-icon-large">
          <BarChart3 size={64} />
        </div>
        <h1>Progress Analytics</h1>
        <p className="module-subtitle">
          Track your preparation progress with detailed insights, charts, and performance metrics.
        </p>
      </div>
      
      <div className="module-content">
        <div className="coming-soon">
          <h2>📊 Coming Soon</h2>
          <p>We're building comprehensive analytics with:</p>
          <ul>
            <li>Performance trends and insights</li>
            <li>Skill-wise proficiency charts</li>
            <li>Time spent analysis</li>
            <li>Comparative performance metrics</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Analytics;
