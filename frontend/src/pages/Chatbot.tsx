import { Link } from 'react-router-dom';
import { MessageSquare, ArrowLeft } from 'lucide-react';
import './ModulePage.css';

const Chatbot = () => {
  return (
    <div className="module-page-container">
      <div className="module-header">
        <Link to="/dashboard" className="back-button">
          <ArrowLeft size={20} />
          Back to Dashboard
        </Link>
        <div className="module-icon-large">
          <MessageSquare size={64} />
        </div>
        <h1>AI Chatbot Assistance</h1>
        <p className="module-subtitle">
          Get instant answers to your questions. 24/7 AI-powered assistance for all your interview prep needs.
        </p>
      </div>
      
      <div className="module-content">
        <div className="coming-soon">
          <h2>💬 Coming Soon</h2>
          <p>We're creating an intelligent chatbot assistant with:</p>
          <ul>
            <li>Instant answers to interview questions</li>
            <li>Personalized study recommendations</li>
            <li>Career guidance and tips</li>
            <li>24/7 availability for your queries</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Chatbot;
