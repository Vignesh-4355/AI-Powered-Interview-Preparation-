import { Link } from 'react-router-dom';
import { Users, ArrowLeft } from 'lucide-react';
import './ModulePage.css';

const HRDiscussion = () => {
  return (
    <div className="module-page-container">
      <div className="module-header">
        <Link to="/dashboard" className="back-button">
          <ArrowLeft size={20} />
          Back to Dashboard
        </Link>
        <div className="module-icon-large">
          <Users size={64} />
        </div>
        <h1>HR & Group Discussion</h1>
        <p className="module-subtitle">
          Master behavioral interviews, group discussions, and HR rounds with expert guidance and practice scenarios.
        </p>
      </div>
      
      <div className="module-content">
        <div className="coming-soon">
          <h2>👥 Coming Soon</h2>
          <p>We're developing comprehensive HR and GD preparation with:</p>
          <ul>
            <li>Common HR interview questions</li>
            <li>Behavioral interview techniques</li>
            <li>Group discussion topics and practice</li>
            <li>Communication skills improvement</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default HRDiscussion;
